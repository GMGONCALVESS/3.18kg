from sqlalchemy import text, create_engine
import pandas as pd
import numpy

# conexões BD's
engine = create_engine("postgressql://postgres:admin@192.168.88.61:5432/yield_debentures")
conex_db = create_engine("postgressql://postgres:admin@192.168.88.61:5432/posicoesdb")

# receber dados do banco posicoesdb.setor e colocá-los no banco yield_debentures.setores
dados_originais = pd.read_sql("SELECT setor, subsetor, segmento, ticker FROM setor", conex_db)
dados_originais.to_sql()

# dados da tabela a ser criada, para impedir duplicatas
dados_tabela_criada = pd.read_sql("SELECT setor, subsetor, segmento, ticker FROM setores", engine)

filtrados = dados_tabela_criada[~dados_tabela_criada["setor"]
                                ]