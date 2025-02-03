import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from datetime import datetime
from sqlalchemy import create_engine, text
import time
import csv
import json
import pandas as pd


# # escolher data específica, ativo especifico, pegar maturidades

# data = input("Insira a data (YYYY-MM-DD): ")

# ativo = input("Insira o código do ativo: ")

# # Cria conexão com o banco de dados
# engine = create_engine(
#     'postgresql://postgres:admin@192.168.88.61:5432/yield_debentures')

# df = pd.read_sql(f"SELECT codigo_ativo, data_vencimento, taxa_indicativa, emissor FROM copia_dados_debenture WHERE codigo_ativo = '{ativo}' AND data_referencia = '{data}';", engine)

# print(df)

# Get user input
# data = input("Insira a data (YYYY-MM-DD): ")
data = '2024-01-10'
# ativo = input("Insira o código da empresa: ")
ativo = 'EGIE'

# Create a secure database connection
engine = create_engine(
    'postgresql://postgres:admin@192.168.88.61:5432/yield_debentures'
)

# Secure query using parameterized SQL
query = text(f"""SELECT grupo, indexador, taxa_emissao, codigo_ativo, data_vencimento, taxa_indicativa, emissor
             FROM copia_dados_debenture
             WHERE codigo_ativo LIKE '%{ativo}%'
             AND data_referencia = '{data}' ORDER BY data_vencimento ASC;""")
# print(query)
# Execute the query safely
with engine.connect() as connection:
    df = pd.read_sql(query, connection)
pd.set_option('display.max_rows', None)  # Show all rows
pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.width', None)
print(df)
# Display the results
if len(df) == 0:
    print('dataframe vazio')
else:
    print("plotando dados")
    dicionario = df.to_dict()
    ativos = list(dicionario['codigo_ativo'].values())
    taxa = list(dicionario['taxa_indicativa'].values())
    data_vencimento = list(dicionario['data_vencimento'].values())
    emissor = list(dicionario['emissor'].values())

    # print(data_vencimento)
    # print(taxa)

    plt.xlabel("Maturity", fontdict={'size':15})
    plt.ylabel("Taxa Indicativa", fontdict={'size':15})
    plt.title(",".join(set(emissor)), fontdict={'size':25})
    # print(emissor)
    plt.grid(True)
    plt.plot(data_vencimento, taxa, marker='o',linewidth = 5)#, linestyle='-', linewidth='3')
    plt.show()


