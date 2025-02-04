"""
O código a seguir realiza a requisição para a API de 30 em 30 minutos, feito via windows scheduler, ao receber os dados do dia atual
para de enviar requisições, e mantém-se em 'sleep' durante 24 horas, para iniciar novamente a leitura dos dados
para o próximo dia. Sobe os dados para bd, e considera feriados e finais de semana para não exaurir o processamento
"""

from auto_tratamento import tratar
from auto_verificar import verificar
from auto_api import conexao_func
from auto_dias import cria_calendario
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

datas = data = cria_calendario(ano_atual)

# print(datas)

datas_uteis = [d.strftime("%Y-%m-%d") for d in datas]

data_atual = "2025-01-31"

# print(datas_apenas)

# Se a data atual estiver na lista de dias uteis
if data_atual in datas_uteis:

    # verificar se já foi atualizado o dia
    dados = conexao_func(data_atual)  # data_atual
    # print(dados)

    if dados != None:

        print("Dados recebidos")
        inserir = verificar(engine, data_atual)

        if inserir:

            print("O dado será inserido")
            for item in dados:
                resultado = tratar(item)
            # with engine.connect() as conexao:
            #     # for _, row in dados.iterrows():
            #     for item in dados:
            #         query = text("""
            #             INSERT INTO pbi_plot_debentures (grupo, codigo_ativo, data_referencia, data_vencimento,
            #                                     duration, indexador, taxa_emissao, taxa_indicativa, emissor)
            #             VALUES (:grupo, :codigo_ativo, :data_referencia, :data_vencimento,
            #                     :duration, :indexador, :taxa_emissao, :taxa_indicativa, :emissor);
            #         """)

            #         conexao.execute(query, {
            #             "grupo": item["grupo"],
            #             "codigo_ativo": item["codigo_ativo"],
            #             "data_referencia": item["data_referencia"],
            #             "data_vencimento": item["data_vencimento"],
            #             "duration": item["duration"],
            #             "indexador": item["indexador"],
            #             "taxa_emissao": item["taxa_emissao"],
            #             "taxa_indicativa": item["taxa_indicativa"],
            #             "emissor": item["emissor"]
            #         })

            #     conexao.commit()
                resultado.to_sql(name="dados_debenture", con=engine, if_exists="append", index=False)
        else:
            print("O dado já foi inserido")
    else:
        print("Dados do dia não atualizados")
else:
    # se não estiver, pusa o código por 24 horas
    # ETAPA FEITA NO SCHEDULE
    # time.sleep(24*60*60)
    print("Não é dia útil")
