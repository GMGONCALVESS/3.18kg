from sqlalchemy import create_engine, text
import pandas as pd


def tratar(item, data_atual):
    try:
        pd.set_option('display.max_rows', None)
        dados = pd.DataFrame(item['ettj'])

        # print(dados)
        maturity = []
        pre = []
        ipca = []
        implicita = []
        # dados_limpos = dados.dropna()
        for index, row in dados.iterrows():
            maturity.append(float(row['vertice_du']/252))
            pre.append(float(row['taxa_prefixadas']))
            ipca.append(float(row['taxa_ipca']))
            implicita.append(float(row['taxa_implicita']))

        # print(insert_query)

        params = {"maturity": maturity,
                  "pre": pre,
                  "ipca": ipca,
                  "implicita": implicita,
                  "data_referencia": data_atual
                  }
        params = pd.DataFrame([params])

        # print(params)

    except Exception as e:
        print(item)
        raise e

    return params
