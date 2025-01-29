from tratamento_dados import tratar
from sqlalchemy import create_engine, text
from api_connect import conexao_func
from dias_uteis import cria_calendario
import time
import random
import csv
import json
import pandas as pd

# Cria conexão com o banco de dados
engine = create_engine(
    'postgresql://postgres:admin@192.168.88.61:5432/yield_debentures')

anos = list(range(2019, 2020))
resultado = pd.DataFrame()

for ano in anos:
    data = cria_calendario(ano)

    # print(data)
    data_filtrada = data[(data >= "2019-09-01") & (data <= "2019-12-31")]

    # print(data_filtrada)

    data_apenas = [d.strftime("%Y-%m-%d") for d in data_filtrada]

    for data in data_apenas:
        print(data)
        # Conexão com a API, passar datas de dias úteis
        dados = conexao_func(data)

        # print(dados)

        # Inserção de dados
        for item in dados:
            # print(item)
            dataframe = tratar(item)

            resultado = pd.concat([resultado, dataframe], ignore_index=False)

    resultado.to_sql(name="dados_debenture", con=engine,
                     if_exists="append", index=False)

    numero_aleatorio = random.randint(1, 10)
    time.sleep(numero_aleatorio)
