import pandas as pd
import streamlit as st
import plotly.express as px

# ================================
# Configuração inicial
# ================================
st.set_page_config(page_title="Dashboard de Vendas", layout="wide")
st.title("📊 Dashboard Interativo de Vendas")

# ================================
# Leitura dos dados
# ================================
file_id = "1bAdbZFSNx5nKwyPv1QEnbTXx-lHWWQDm"
url = f"https://drive.google.com/uc?id=1bAdbZFSNx5nKwyPv1QEnbTXx-lHWWQDm"

# Ler excel
df = pd.read_excel(url)

# ================================
# KPIs principais
# ================================
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total de Compras", df.shape[0])
with col2:
    st.metric("Destinos únicos", df["place_destination_departure"].nunique())
with col3:
    st.metric("Período analisado", f"{df['date_purchase'].min().date()} ➝ {df['date_purchase'].max().date()}")

# ================================
# 📈 Evolução diária (timeline)
# ================================
st.header("📈 Evolução das Compras ao Longo do Tempo")

df["date_purchase"] = pd.to_datetime(df["date_purchase"], errors="coerce")
compras_por_dia = df.groupby("date_purchase").size()

if compras_por_dia.empty:
    st.warning("⚠️ Nenhuma informação de data encontrada no dataset.")
else:
    fig0 = px.line(
        compras_por_dia,
        x=compras_por_dia.index,
        y=compras_por_dia.values,
        markers=True,
        labels={"x": "Data", "y": "N° de Compras"},
        title="Timeline de Compras"
    )
    st.plotly_chart(fig0, use_container_width=True)

# ================================
# 📍 Top Destinos
# ================================
st.header("📍 Destinos mais escolhidos")

substituicoes = {
    "6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b": "Destino A",
    "7688b6ef52555962d008fff894223582c484517cea7da49ee67800adc7fc8866": "Destino B",
    "2fca346db656187102ce806ac732e06a62df0dbb2829e511a770556d398e1a6e": "Destino C",
    "4e07408562bedb8b60ce05c1decfe3ad16b72230967de01f640b7e4729b49fce": "Destino D",
    "81b8a03f97e8787c53fe1a86bda042b6f0de9b0ec9c09357e107c99ba4d6948a": "Destino E"
}

top_destinos = df["place_destination_departure"].value_counts().head(5)
top_destinos.index = top_destinos.index.map(substituicoes)

col1, col2 = st.columns([2,1])
with col1:
    fig1 = px.bar(
        top_destinos,
        x=top_destinos.index,
        y=top_destinos.values,
        color=top_destinos.index,
        labels={"x": "Destino", "y": "N° de Compras"},
        title="Top 5 destinos"
    )
    st.plotly_chart(fig1, use_container_width=True)
with col2:
    st.dataframe(
        top_destinos.reset_index().rename(
            columns={"index": "Destino", "place_destination_departure": "N° de Compras"}
        )
    )

# ================================
# 🗓️ Compras por mês (Sazonalidade)
# ================================
st.header("🗓️ Sazonalidade de Compras")

# Extrair mês (número + nome)
df["mes_num"] = df["date_purchase"].dt.month
df["mes"] = df["date_purchase"].dt.month_name()

# Traduzir manualmente
traducao_meses = {
    "January": "Janeiro", "February": "Fevereiro", "March": "Março",
    "April": "Abril", "May": "Maio", "June": "Junho",
    "July": "Julho", "August": "Agosto", "September": "Setembro",
    "October": "Outubro", "November": "Novembro", "December": "Dezembro"
}
df["mes"] = df["mes"].map(traducao_meses)

# Contagem de compras por mês (ordenado corretamente)
compras_por_mes = df.groupby("mes_num")["mes"].count()
compras_por_mes.index = compras_por_mes.index.map({
    1:"Janeiro",2:"Fevereiro",3:"Março",4:"Abril",5:"Maio",6:"Junho",
    7:"Julho",8:"Agosto",9:"Setembro",10:"Outubro",11:"Novembro",12:"Dezembro"
})

if compras_por_mes.empty:
    st.warning("⚠️ Nenhuma informação de data encontrada no dataset.")
else:
    col1, col2 = st.columns([2,1])
    with col1:
        fig2 = px.line(
            compras_por_mes,
            x=compras_por_mes.index,
            y=compras_por_mes.values,
            markers=True,
            labels={"x": "Mês", "y": "N° de Compras"},
            title="Compras ao longo do ano"
        )
        st.plotly_chart(fig2, use_container_width=True)
    with col2:
        fig2b = px.pie(
            compras_por_mes,
            names=compras_por_mes.index,
            values=compras_por_mes.values,
            title="Distribuição por mês"
        )
        st.plotly_chart(fig2b, use_container_width=True)

# ================================
# ⏰ Horários de compra
# ================================
st.header("⏰ Horários de Compra")

df["time_purchase"] = pd.to_datetime(df["time_purchase"], format="%H:%M:%S", errors="coerce").dt.hour

def horario_comercial(hora):
    if pd.isna(hora):
        return "Desconhecido"
    elif 9 <= hora < 18:
        return "Hora Comercial"
    else:
        return "Fora Comercial"

df["horario_tipo"] = df["time_purchase"].apply(horario_comercial)
compras_por_periodo = df["horario_tipo"].value_counts().sort_index()

col1, col2 = st.columns([1,2])
with col1:
    st.dataframe(
        compras_por_periodo.reset_index().rename(
            columns={"index": "Período", "horario_tipo": "N° de Compras"}
        )
    )
with col2:
    fig3 = px.pie(
        compras_por_periodo,
        names=compras_por_periodo.index,
        values=compras_por_periodo.values,
        title="Distribuição de compras por período"
    )
    st.plotly_chart(fig3, use_container_width=True)
