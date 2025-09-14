import pandas as pd
import matplotlib.pyplot as plt

# Leitura dos dados
df = pd.read_excel("df_t.xlsx")

# Converter colunas de hora
df["time_purchase"] = pd.to_datetime(df["time_purchase"], format="%H:%M:%S", errors="coerce").dt.hour

# Criar condição: faixa de horário
def faixa_horario(hora):
    if pd.isna(hora):
        return "Desconhecido"
    elif 6 <= hora < 12:
        return "Manhã"
    elif 12 <= hora < 18:
        return "Tarde"
    elif 18 <= hora < 24:
        return "Noite"
    else:
        return "Madrugada"

df["horario_tipo"] = df["time_purchase"].apply(faixa_horario)

# Contagem de compras/horário
compras_por_periodo = df["horario_tipo"].value_counts().sort_index()
print(compras_por_periodo)

# Visual do histograma
plt.figure(figsize=(10,5))
plt.bar(compras_por_periodo.index.astype(str), compras_por_periodo.values, color="darkviolet")

plt.title("Período de Compra")
plt.xlabel("Horário")
plt.ylabel("N° de Compras")
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()