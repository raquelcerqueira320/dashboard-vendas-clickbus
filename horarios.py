import pandas as pd
import matplotlib.pyplot as plt

# Leitura dos dados
df = pd.read_excel("df_t.xlsx")

# Converter colunas de hora
df["time_purchase"] = pd.to_datetime(df["time_purchase"], format="%H:%M:%S", errors="coerce").dt.hour

# Criar condição: horário comercial ou não
def horario_comercial(hora):
    if pd.isna(hora):
        return "Desconhecido"
    elif 9 <= hora < 18:
        return "Hora_Comercial"
    else:
        return "Fora_Comercial"

df["horario_tipo"] = df["time_purchase"].apply(horario_comercial)

# Contagem de compras/horário
compras_por_periodo = df["horario_tipo"].value_counts().sort_index()
print (compras_por_periodo)

# Visual do histograma
plt.figure(figsize=(10,5))
plt.bar(compras_por_periodo.index.astype(str), compras_por_periodo.values, color="darkviolet")

plt.title("Período de Compra")
plt.xlabel("Horário")
plt.ylabel("N° de Compras")
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()