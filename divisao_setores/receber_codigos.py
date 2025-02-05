from sqlalchemy import text, create_engine
import pandas as pd
import numpy as np
def codigos():
        
    # conexões BD's
    engine = create_engine(
        "postgresql://postgres:admin@192.168.88.61:5432/yield_debentures")
    conex_db = create_engine(
        "postgresql://postgres:admin@192.168.88.61:5432/posicoesdb")

    # receber dados do banco posicoesdb.setor e colocá-los no banco yield_debentures.setores
    dados_originais = pd.read_sql(
        "SELECT empresa, setor, subsetor, segmento, ticker FROM setor where ticker is not null and ticker <> '' order by ticker", conex_db)

    # dados da tabela a ser criada, para impedir duplicatas
    dados_tabela_criada = pd.read_sql(
        "SELECT empresa, setor, subsetor, segmento, ticker FROM setores", engine)

    filtrados = dados_originais.drop_duplicates(subset=['ticker'], keep='first')
    # MATEUS

    # se tabela forem iguais nao faz nada, senão inserta
    if not dados_tabela_criada.equals(filtrados):
        filtrados.to_sql(name="setores", con=engine,
                        if_exists="replace", index=False)

    dados_pbi = pd.read_sql(
        "SELECT codigo_ativo, emissor FROM pbi_plot_debentures", engine)

    dados_pbi['codigo_ativo'] = dados_pbi['codigo_ativo'].str.replace(
        r'\d+', '', regex=True)

    dados_pbi_filtrado = dados_pbi.drop_duplicates(
        subset=['codigo_ativo'], keep='first')
    # GABRIEL


    lista_ativo = list()

    lista_ticker = list()

    # fazer um for que dá  append nas listas, e visualizar em lista
    for index, row in dados_pbi_filtrado.iterrows():
        lista_ativo.append(row['codigo_ativo'])

    for index, row in filtrados.iterrows():
        lista_ticker.append(row['ticker'])


    # print(filtrados)
    # print('\n\n\n')
    # print(dados_tabela_criada)
    # print('\n\n\n')
    # print(dados_pbi_filtrado)
    # print(len(lista_ativo))
    # print(len(lista_ticker))

    for item in lista_ticker:
        try:
            lista_ativo.remove(item)
        except:
            continue

    lista_ativo.sort()
    lista_ticker.sort()

    # print(lista_ativo)
    # print('\n\n\n')
    # print(lista_ticker)

    # com a lista de ativos prontas, pode-se 
    return lista_ativo