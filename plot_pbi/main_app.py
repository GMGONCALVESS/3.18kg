import os
import pickle
import time
import pandas as pd
from sqlalchemy import create_engine, text
from retrieve_data import retorna_dados

dados = retorna_dados()

engine = create_engine(
    "postgresql://postgres:admin@192.168.88.61:5432/yield_debentures")

for item in dados["data_vencimento"]:
    y = item.split("-")

    if y[0] >= '2500':
        dados.loc[dados["data_vencimento"] ==
                  "2924-04-15", "data_vencimento"] = "2032-11-13"
        dados.loc[dados["data_vencimento"] ==
                  "9999-12-31", "data_vencimento"] = "2036-09-15"

dados.to_sql(name="pbi_plot_debentures", con=engine,
             if_exists="replace", index=False)


# with engine.connect() as conexao:
#     for _, row in dados.iterrows():
#         query = text("""
#             INSERT INTO pbi_plot_debentures (grupo, codigo_ativo, data_referencia, data_vencimento,
#                                       duration, indexador, taxa_emissao, taxa_indicativa, emissor)
#             VALUES (:grupo, :codigo_ativo, :data_referencia, :data_vencimento,
#                     :duration, :indexador, :taxa_emissao, :taxa_indicativa, :emissor);
#         """)

#         conexao.execute(query, {
#             "grupo": row["grupo"],
#             "codigo_ativo": row["codigo_ativo"],
#             "data_referencia": row["data_referencia"],
#             "data_vencimento": row["data_vencimento"],
#             "duration": row["duration"],
#             "indexador": row["indexador"],
#             "taxa_emissao": row["taxa_emissao"],
#             "taxa_indicativa": row["taxa_indicativa"],
#             "emissor": row["emissor"]
#         })

#     conexao.commit()
