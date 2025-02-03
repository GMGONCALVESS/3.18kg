from auto_tratamento_soberano import tratar
from sqlalchemy import create_engine, text
from auto_api_soberano import conexao_func
from auto_dias_soberano import cria_calendario
import time
import random
import csv
import json
import pandas as pd

# Cria conexão com o banco de dados
engine = create_engine(
    'postgresql://postgres:admin@192.168.88.61:5432/yield_debentures')

anos = list(range(2025, 2026))
resultado = pd.DataFrame()

for ano in anos:
    data = cria_calendario(ano)

    # print(data)
    # data[(data >= "2025-01-01") & (data <= "2025-01-28")]
    data_filtrada = data[data == "2025-01-29"]

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
    # print(resultado)
    resultado.to_sql(name="dados_debenture", con=engine,
                     if_exists="append", index=False)

    numero_aleatorio = random.randint(1, 10)
    time.sleep(numero_aleatorio)
