import requests
import base64
from base64 import b64encode
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sqlalchemy import create_engine, text

client_id = 'uHpXjsZAi49A'
client_secret = '2tZrvxqLYZ1N'

auth_string = f"{client_id}:{client_secret}"
auth_bytes = auth_string.encode("ascii")
auth = base64.b64encode(auth_bytes).decode("ascii")

auth_headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': f'Basic {auth}'
}

# Corpo da requisição de autenticação
auth_data = {
    'grant_type': 'client_credentials'
}

auth_url = 'https://api.anbima.com.br/oauth/access-token'

auth_response = requests.post(auth_url, headers=auth_headers, data=auth_data)

access_token = auth_response.json().get('access_token')

headers = {
    'access_token': access_token,
    'client_id': client_id
}

parameters = {
    'data': '2025-01-20'
}

data_url = 'https://api.anbima.com.br/feed/precos-indices/v1/titulos-publicos/curvas-juros'

data_response = requests.get(data_url, headers=headers, params=parameters)

if data_response.status_code == 200:
    data = data_response.json()
else:
    print(f"Erro ao obter os dados: {
          data_response.status_code} - {data_response.text}")


print(data[0]['data_referencia'])
pd.set_option('display.max_rows', None)
dados = pd.DataFrame(data[0]['ettj'])

# print(dados)
maturity = []
pre = []
ipca = []
implicita = []
# dados_limpos = dados.dropna()
for index, row in dados.iterrows():
    maturity.append(row['vertice_du']/252)
    pre.append(row['taxa_prefixadas'])
    ipca.append(row['taxa_ipca'])
    implicita.append(row['taxa_implicita'])
    # print(row['vertice_du']/252, row['taxa_prefixadas'], row['taxa_ipca'], row['taxa_implicita'])

# print(maturity)
# print(pre)
# print(ipca)
# print(implicita)
# pre_np = np.array(pre)
# ipca_np = np.array(ipca)

# teste = 100*((1+pre_np/100)/(1+ipca_np/100) - 1)

# # teste = list(map(lambda a, b: a - b, pre, ipca))
# print(ipca_np)
# print(pre_np)
# print(teste)
# # print(implicita)

# plt.xlabel("Maturity", fontdict={'size':15})
# plt.ylabel("Taxas", fontdict={'size':15})
# # plt.title(",".join(set(emissor)), fontdict={'size':25})
# # print(emissor)
# plt.grid(True)
# plt.plot(maturity, pre, marker='o',linewidth = 5, color='b',label='Prefixada')#, linestyle='-', linewidth='3')
# plt.plot(maturity, ipca, marker='o',linewidth = 5, color='r',label='IPCA')#, linestyle='-', linewidth='3')
# plt.plot(maturity, implicita, marker='o',linewidth = 5, color='y',label='Implícita')#, linestyle='-', linewidth='3')
# plt.plot(maturity, teste, marker='o',linewidth = 5, color='k',label='Prefixada - IPCA')#, linestyle='-', linewidth='3')
# plt.legend()
# plt.show()
