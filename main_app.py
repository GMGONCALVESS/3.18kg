from tratamento_dados import tratar
from sqlalchemy import create_engine, text
from api_connect import conexao
from dias_uteis import cria_calendario
import time
import random
import csv
import json


# Cria conexão com o banco de dados
engine = create_engine(
    'postgresql://postgres:admin@192.168.88.61:5432/yield_debentures')


anos = list(range(2020, 2025))

# Tratando datas a serem enviadas para a API
# Escolhendo somente dias úteis
# ano = 2018
# data = cria_calendario(ano)

# print(data)

# data_apenas = [d.strftime("%Y-%m-%d") for d in data]

# print(data_apenas)

for ano in anos:
    print(ano)
    print(type(ano))

    data = cria_calendario(ano)

    data_apenas = [d.strftime("%Y-%m-%d") for d in data]

    print(data)
    print(data_apenas)

    for data in data_apenas:
        # Conexão com a API, passar datas de dias úteis
        dados = conexao(data)

        # Inserção de dados
        for item in dados:

            resultado = tratar(item)

            with engine.connect() as conexao:
                conexao.execute(resultado[0], resultado[1])
                conexao.commit()

        numero_aleatorio = random.randint(1, 10)
        time.sleep(numero_aleatorio)
    numero_aleatorio = random.randint(1, 10)
    time.sleep(numero_aleatorio)
