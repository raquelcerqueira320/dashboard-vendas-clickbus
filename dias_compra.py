import pandas as pd
import matplotlib.pyplot as plt

# Leitura dos dados
df = pd.read_excel("df_t.xlsx")

# Coluna de data do arquivo em datetime
df["date_purchase"] = pd.to_datetime(df["date_purchase"], errors="coerce")

# Utilizar apenas a informação de mês
df["mes"] = df["date_purchase"].dt.month_name(locale="pt_BR.utf8") # 1 = Janeiro, 12 = Dezembro

# Contagem de compras/mês
compras_por_mes = df["mes"].value_counts().sort_index()
print (compras_por_mes)

# Visual do histograma
plt.figure(figsize=(10,5))
plt.bar(compras_por_mes.index.astype(str), compras_por_mes.values, color="darkviolet")

plt.title("Sazonalidade")
plt.xlabel("Período")
plt.ylabel("N° de Compras")
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()