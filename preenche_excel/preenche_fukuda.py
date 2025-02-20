import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine, text

engine = create_engine(
    'postgresql://postgres:admin@192.168.88.61:5432/yield_debentures')

data_atual = str(datetime.now()).split(" ")[0]
data_atual = "2025-02-11"

lista = pd.read_excel(
    "copia_teste.xlsx", sheet_name=1)

modificar = lista[["CodCustodia", "Duration", "VlMrc"]][160:193]
# print(modificar)

pega_duration = pd.read_sql(f"SELECT DISTINCT codigo_ativo, duration FROM dados_debenture WHERE data_referencia = '{data_atual}' ", engine)
# print(pega_duration)

# Merge the DataFrames on 'CodCustodia' and 'codigo_ativo'
merged = modificar.merge(pega_duration, left_on="CodCustodia", right_on="codigo_ativo", how="left")

# Drop duplicate column (codigo_ativo) if not needed
merged.drop(columns=["codigo_ativo"], inplace=True)
merged.drop(columns=["Duration"], inplace=True)

print(modificar)
print(merged)

# Print the merged DataFrame
# print(merged["CodCustodia"][0])
for ind, row in merged.iterrows():
    print(row.array[2])
    if row.array[2] == 'nan':
        continue
    else:
        modificar["Duration"][modificar.index[ind]] = row.array[2]
#     print(row.array[0])
#     print(row.array[1])
#     print(row.array[2])
    
print(modificar)
print(merged)
soma = 0
for ind, row in  