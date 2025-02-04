# Verificar se já existe a data a ser inserida no bd
from sqlalchemy import create_engine, text
import pandas as pd


def verificar(engine, data_atual):

    # Realizar uma query para pegar a data mais recente
    data_query = text(""" 
    SELECT MAX(data_referencia) AS data_mais_recente FROM copia_dados_debenture;
""")

    with engine.connect() as conexao:
        resultado = conexao.execute(data_query).scalar()
        conexao.commit()
    # print(resultado)
    # print(type(resultado))
    ano_bd, mes_bd, dia_bd = tuple(resultado.split("-"))
    ano_bd = int(ano_bd)
    mes_bd = int(mes_bd)
    dia_bd = int(dia_bd)

    ano_atual, mes_atual, dia_atual = tuple(data_atual.split("-"))
    ano_atual = int(ano_atual)
    mes_atual = int(mes_atual)
    dia_atual = int(dia_atual)

    # if(dia_atual <= dia_bd):
    #     return False
    # else:
    #     return True
    if (ano_atual >= ano_bd and mes_atual >= mes_bd):
        if (dia_atual > dia_bd):
            return True
        else:
            if (ano_atual > ano_bd):
                return True
            elif (ano_atual == ano_bd):
                if (mes_atual > mes_bd):
                    return True
                else:
                    return False
            else:
                return False
    else:
        return False
