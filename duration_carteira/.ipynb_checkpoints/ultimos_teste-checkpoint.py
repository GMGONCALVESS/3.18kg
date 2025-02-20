from xbbg import blp
from datetime import datetime, timedelta
import pandas as pd
from sqlalchemy import create_engine, MetaData, Table
import time
from dias import cria_calendario

engine1 = create_engine(
    "postgresql://postgres:admin@192.168.88.61:5432/yield_debentures")

di_df = pd.read_sql(
    "SELECT * FROM curvas_juros ORDER BY data_referencia DESC", engine1)

dados_gerais = pd.read_sql("""select codigo_ativo, taxa_indicativa, data_referencia 
from dados_debenture 
where codigo_ativo = 'AEGE17' and data_referencia = '2025-02-18'""", engine1)

pre = di_df.iloc[0]['pre']
maturity = di_df.iloc[0]['maturity']

primeiro_nan = pd.Series(pre).isna().idxmax()

pre = pre[0:primeiro_nan]

maturity_days = [252*item for item in maturity]
maturity_days = maturity_days[0:primeiro_nan]

print(pre)
print(maturity_days)

engine2 = create_engine(
    "postgresql://postgres:admin@192.168.88.61:5432/posicoesdb")
data_atual = str(datetime.now()).split(" ")[0]
data_atual = "2025-02-18"
ano = datetime.strptime(data_atual, "%Y-%m-%d").year

# PUXAR O TIPO DE EVENTO

dados = pd.read_sql(
    "SELECT data_evento, percentual_taxa, pu, cdi, days, evento, valor_recebido, juros_pagos FROM eventos_debenture_cdi WHERE codigo_ticker = 'AEGE17' ORDER BY data_liquidacao DESC", engine2)

dia_evento = dados['data_evento'].tolist()
dia_evento = [str(d).split(" ")[0] for d in dia_evento]

pu = dados['pu'].tolist()
juros_pagos = dados['juros_pagos'].tolist()

ano_ult_event = datetime.strptime(dia_evento[0], "%Y-%m-%d").year

datas_uteis = []

for year in range(ano, ano_ult_event+1):
    datas = cria_calendario(year)
    datas = [d.strftime("%Y-%m-%d") for d in datas]
    datas_uteis = datas_uteis + datas

indice_atual = datas_uteis.index(data_atual)
dias_vencimento = list()
for item in dia_evento:
    try:
        indice_fim = datas_uteis.index(item)
        # print(indice_fim - indice_atual)
        dias_vencimento.append(indice_fim-indice_atual)
    except:
        datas = sorted([datetime.strptime(data, '%Y-%m-%d')
                       for data in datas_uteis])

        # Data alvo
        data_alvo = datetime.strptime(item, '%Y-%m-%d')

        # Encontrar a primeira data maior que a alvo
        proxima_data_util = next(
            (data for data in datas if data > data_alvo), None)

        # proxima_data_util.strftime('%Y-%m-%d')
        indice_fim = datas.index(proxima_data_util)  # UTILIZAR BUSY DATES
        # print(proxima_data_util)
        # print(indice_fim - indice_atual)
        dias_vencimento.append(indice_fim-indice_atual)

taxas_dias = list()
for item in dias_vencimento:
    for dias in maturity_days:
        if dias >= item:
            x2 = dias
            # print(x2)
            i1 = maturity_days.index(x2)
            x1 = maturity_days[i1-1]
            # print(x1)
            y2 = pre[i1]
            y1 = pre[i1-1]
            # print(y2)
            # print(y1)
            m = (y2-y1)/(x2-x1)
            b = y1-m*x1
            taxas_dias.append(m*item+b)
            break

print(taxas_dias)
print(dias_vencimento)

taxa_atual = float(dados_gerais.loc[0]['taxa_indicativa'])

di_ano_atual = 13.15
spread = 3.4  # taxa_atual
PV_CF = list()
for i in range(0, len(taxas_dias)):
    spread_diario = (1+spread/100)**(1/252)
    di_diario = (1+taxas_dias[i]/100)**(1/252)
    D = spread_diario*di_diario
    # print(D)
    # D = ((1+spread/100)*(1+taxas_dias[i]/100))**(dias_vencimento[i]/252)
    PV_CF.append(juros_pagos[i]/(D**dias_vencimento[i]))
print(PV_CF)

soma_num = 0
for i in range(0, len(taxas_dias)):
    soma_num = soma_num + PV_CF[i]*dias_vencimento[i]

print(soma_num/sum(PV_CF))
