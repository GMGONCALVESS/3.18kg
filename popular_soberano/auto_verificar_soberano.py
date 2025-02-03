# Verificar se já existe a data a ser inserida no bd
from sqlalchemy import create_engine, text
import pandas as pd


def verificar(engine, data_atual):

    # Realizar uma query para pegar a data mais recente
    data_query = text(""" 
    SELECT MAX(data_referencia) AS data_mais_recente FROM curvas_juros;
""")

    with engine.connect() as conexao:
        resultado = conexao.execute(data_query).scalar()
        # print(resultado)
        conexao.commit()
    # print(resultado)
    # print(type(resultado))
    

    ano_atual, mes_atual, dia_atual = tuple(data_atual.split("-"))
    ano_atual = int(ano_atual)
    mes_atual = int(mes_atual)
    dia_atual = int(dia_atual)

    if resultado != None:
        ano_bd, mes_bd, dia_bd = tuple(resultado.split("-"))
        ano_bd = int(ano_bd)
        mes_bd = int(mes_bd)
        dia_bd = int(dia_bd)
    else:
        print("Primeira Inserção")
        return True

    if (dia_atual <= dia_bd):
        return False
    else:
        return True
