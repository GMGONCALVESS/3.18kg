import xlrd
from tratamento_dados import tratar
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

try:
    data_response = requests.get(data_url, headers=headers)
except:
    print("Acesso negado à API")

if data_response.status_code == 200:
    data = data_response.json()
else:
    print(f"Erro ao obter os dados: {
          data_response.status_code} - {data_response.text}")

# print(data[0])

for item in data:

    resultado = tratar(item)

    with engine.connect() as conexao:
        conexao.execute(resultado[0], resultado[1])
        conexao.commit()
