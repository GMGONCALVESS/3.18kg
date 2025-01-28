import xlrd
from datetime import datetime, date, timedelta
from urllib.request import urlretrieve
from pandas.tseries.holiday import AbstractHolidayCalendar, Holiday
from pandas.tseries.offsets import CustomBusinessDay
import pandas as pd
import requests
from openpyxl import Workbook
import csv
from sqlalchemy import create_engine, text
import time
import base64
from base64 import b64encode
import json

# Cria conexão com o banco de dados
engine = create_engine(
    'postgresql://postgres:admin@192.168.88.61:5432/yield_debentures')

# # Query para criar a tabela
# create_table_query = """
# CREATE TABLE IF NOT EXISTS minha_tabela (
#     a INT,
#     b VARCHAR(255),
#     c FLOAT
# )
# """

# with engine.connect() as conexao:
#     conexao.execute(text(create_table_query))
#     conexao.commit()


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

data_url = 'https://api.anbima.com.br/feed/precos-indices/v1/debentures/mercado-secundario'

data_response = requests.get(data_url, headers=headers)

if data_response.status_code == 200:
    data = data_response.json()
else:
    print(f"Erro ao obter os dados: {
          data_response.status_code} - {data_response.text}")

# print(data)

for item in data:
    grupo = item['grupo']
    codigo_ativo = item['codigo_ativo']
    data_referencia = item['data_referencia']
    data_vencimento = item['data_vencimento']
    percentual_taxa = item['percentual_taxa']
    taxa_compra = item['taxa_compra']
    taxa_venda = item['taxa_venda']
    taxa_indicativa = item['taxa_indicativa']
    desvio_padrao = item['desvio_padrao']
    val_min_intervalo = item['val_min_intervalo']
    val_max_intervalo = item['val_max_intervalo']
    pu = item['pu']
    percent_pu_par = item['percent_pu_par']
    duration = item['duration']
    percent_reune = item['percent_reune']
    data_finalizado = item['data_finalizado']
    emissor = item['emissor']
    referencia_ntnb = item['referencia_ntnb']

    # Query para insertar dados na tabela
    insert_query = """
    INSERT INTO dados_debentures (grupo, codigo_ativo, data_referencia, data_vencimento, percentual_taxa, taxa_compra, taxa_venda, taxa_indicativa, desvio_padrao, val_min_intervalo, val_max_intervalo, pu, percent_pu_par, duration, percent_reune, data_finalizado, emissor, referencia_ntnb) 
    VALUES (:grupo, :codigo_ativo, :data_referencia, :data_vencimento, :percentual_taxa, :taxa_compra, :taxa_venda, :taxa_indicativa, :desvio_padrao, :val_min_intervalo, :val_max_intervalo, :pu, :percent_pu_par, :duration, :percent_reune, :data_finalizado, :emissor, :referencia_ntnb)
    """

    with engine.connect() as conexao:
        # conexao.execute(text(create_table_query))
        conexao.execute(text(insert_query), {"grupo": grupo,
                                             "codigo_ativo": codigo_ativo,
                                             "data_referencia": data_referencia,
                                             "data_vencimento": data_vencimento,
                                             "percentual_taxa": percentual_taxa,
                                             "taxa_compra": taxa_compra,
                                             "taxa_venda": taxa_venda,
                                             "taxa_indicativa": taxa_indicativa,
                                             "desvio_padrao": desvio_padrao,
                                             "val_min_intervalo": val_min_intervalo,
                                             "val_max_intervalo": val_max_intervalo,
                                             "pu": pu,
                                             "percent_pu_par": percent_pu_par,
                                             "duration": duration,
                                             "percent_reune": percent_reune,
                                             "data_finalizado": data_finalizado,
                                             "emissor": emissor,
                                             "referencia_ntnb": referencia_ntnb})
        conexao.commit()

        # Modificar o recebimento de dados com as colunas da tabela.
