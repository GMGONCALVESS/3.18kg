"""
O código a seguir realiza a requisição para a API de 30 em 30 minutos, feito via windows scheduler, ao receber os dados do dia atual
para de enviar requisições, e mantém-se em 'sleep' durante 24 horas, para iniciar novamente a leitura dos dados
para o próximo dia. Sobe os dados para bd, e considera feriados e finais de semana para não exaurir o processamento
"""

from auto_tratamento_soberano import tratar
from auto_verificar_soberano import verificar
from auto_api_soberano import conexao_func
from auto_dias_soberano import cria_calendario
from datetime import datetime
from sqlalchemy import create_engine, text
import time
import csv
import json
import pandas as pd


# Cria conexão com o banco de dados
engine = create_engine(
    'postgresql://postgres:admin@192.168.88.61:5432/yield_debentures')

data_atual = str(datetime.now()).split(" ")[0]

# print(data_atual)

ano_atual, mes_atual, dia_atual = tuple(data_atual.split("-"))
ano_atual = int(ano_atual)
mes_atual = int(mes_atual)
dia_atual = int(dia_atual)

# print(ano_atual, mes_atual, dia_atual)
# anos = list(range(2018, 2026))

# for ano in anos:
# ano_atual = ano

datas = data = cria_calendario(ano_atual)

datas_uteis = [d.strftime("%Y-%m-%d") for d in datas]
# data_atual = "2025-02-04"
# Se a data atual estiver na lista de dias uteis
if data_atual in datas_uteis:
    # for data_atual in datas_uteis:
    print(data_atual)
    # verificar se já foi atualizado o dia
    dados = conexao_func(data_atual)  # data_atual
    # print(dados)

    if dados != None:

        print("Dados recebidos")
        inserir = verificar(engine, data_atual)
        # inserir = True
        if inserir:

            print("O dado será inserido")
            for item in dados:
                resultado = tratar(item, data_atual)
                print(resultado)
                resultado.to_sql(name="curvas_juros", con=engine,
                                 if_exists="append", index=False)

        else:
            print("O dado já foi inserido")
    else:
        print("Dados do dia não atualizados")
else:
    # se não estiver, pusa o código por 24 horas
    # ETAPA FEITA NO SCHEDULE
    # time.sleep(24*60*60)
    print("Não é dia útil")
