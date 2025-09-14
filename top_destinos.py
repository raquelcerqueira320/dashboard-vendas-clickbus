import pandas as pd
import matplotlib.pyplot as plt

# Leitura dos dados
df = pd.read_excel("df_t.xlsx")

# Por conta dos dados criptografados, vamos utilizar um ''nome fantasia'' para melhor visualização.
substituicoes = {
    "6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b": "Destino A",
    "7688b6ef52555962d008fff894223582c484517cea7da49ee67800adc7fc8866": "Destino B",
    "2fca346db656187102ce806ac732e06a62df0dbb2829e511a770556d398e1a6e": "Destino C",
    "4e07408562bedb8b60ce05c1decfe3ad16b72230967de01f640b7e4729b49fce": "Destino D",
    "81b8a03f97e8787c53fe1a86bda042b6f0de9b0ec9c09357e107c99ba4d6948a": "Destino E"
}

# Contando quantas vezes cada cidade aparece no destino de ida
top_destinos = df["place_destination_departure"].value_counts().head(5)

# Substituir hashes pelas substituicoes
top_destinos.index = top_destinos.index.map(substituicoes)

print("📍 5 destinos mais procurados:")
print(top_destinos)

# Histograma
plt.figure(figsize=(8,5))
top_destinos.plot(kind="bar", color="slateblue")

plt.title("Cidades mais procuradas")
plt.xlabel("Cidade de Destino (ida)")
plt.ylabel("N° de Compras")
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()