from sqlalchemy import text, create_engine
import pandas as pd
import streamlit as st
from string_compare import comparar

pd.set_option('display.max_rows', None)  # Show all rows
pd.set_option('display.max_columns', None)

engine = create_engine(
    "postgresql://postgres:admin@192.168.88.61:5432/yield_debentures")

emissores = pd.read_sql("""select distinct trim(cleaned_column) as emissor_limpo from (SELECT REPLACE(REPLACE(emissor, '(*)', ''), '(**)', '') AS cleaned_column
FROM pbi_plot_debentures where emissor <> '--')""", engine)

# a = emissores.loc[1].loc["emissor_limpo"]
# print(a)

setores = pd.read_sql(""" select * from setores order by empresa""", engine)

# b = setores.loc[1].loc["empresa"]
# print(b)

# print(setores.loc[0:10])

dados = ["emissor", "setor", "subsetor", "segmento", "ticker"]
resultado = pd.DataFrame(columns=dados)

# print(resultado)
# print(len(resultado))

for i in range(0,  len(emissores)):  # 10):  #
    a = emissores.loc[i].loc["emissor_limpo"]
    # print(a)
    for j in range(0, len(setores)):
        b = setores.loc[j].loc["empresa"]
        c = setores.loc[j]
        if comparar(b, a):
            resultado.loc[len(resultado)] = [
                a, c.loc["setor"], c.loc["subsetor"], c.loc["segmento"], c.loc["ticker"]]
            # break
            # print(a)
            # print(b)
            break

resultado.to_sql("pbi_setores", con=engine, if_exists="replace", index=False)

# st.title("Dataframe Display")
# st.write(resultado)
# st.dataframe(resultado)
# streamlit run app.py
# print(resultado)
