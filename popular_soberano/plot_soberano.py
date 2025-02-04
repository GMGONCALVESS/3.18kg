import matplotlib.pyplot as plt
from sqlalchemy import create_engine, text
import time
import random
import csv
import json
import pandas as pd
import numpy as np


# Cria conexão com o banco de dados
engine = create_engine(
    'postgresql://postgres:admin@192.168.88.61:5432/yield_debentures')
data = "2025-01-28"
query = text(f"""SELECT maturity, pre, ipca, implicita FROM curvas_juros
             WHERE data_referencia = '{data}';""")

# Execute the query safely
with engine.connect() as connection:
    df = pd.read_sql(query, connection)

dados = df.to_dict()
maturity = dados['maturity'][0]
pre = dados['pre'][0]
ipca = dados['ipca'][0]
implicita = dados['implicita'][0]

pre_np = np.array(pre)
ipca_np = np.array(ipca)

teste = 100*((1+pre_np/100)/(1+ipca_np/100) - 1)


print(maturity)
print(pre)
print(ipca)
print(implicita)

plt.xlabel("Maturity", fontdict={'size': 15})
plt.ylabel("Taxas", fontdict={'size': 15})
plt.grid(True)
plt.plot(maturity, pre, marker='o', linewidth=2, color='b',
         label='Prefixada')  # , linestyle='-', linewidth='3')
plt.legend()
plt.show()
plt.grid(True)  

plt.plot(maturity, ipca, marker='o', linewidth=5, color='r',
         label='IPCA')  # , linestyle='-', linewidth='3')
plt.legend()
plt.show()
plt.grid(True)

plt.plot(maturity, implicita, marker='o', linewidth=5, color='y',
         label='Implícita')  # , linestyle='-', linewidth='3')
plt.plot(maturity, teste, linestyle='--', marker='o', linewidth=3, color='k',
         label='Prefixada - IPCA')  # , linestyle='-', linewidth='3')
plt.grid(True)
plt.legend()
plt.show()
