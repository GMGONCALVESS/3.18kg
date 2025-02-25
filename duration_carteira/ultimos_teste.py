# from xbbg import blp
from datetime import datetime, timedelta, date
import pandas as pd
import time
import xlrd
import requests
import csv
import bisect
from sqlalchemy import create_engine, MetaData, Table
from dias import cria_calendario
from urllib.request import urlretrieve
from pandas.tseries.holiday import AbstractHolidayCalendar, Holiday
from pandas.tseries.offsets import CustomBusinessDay
from openpyxl import Workbook


# Pega feriados nacionais pelo calendário da Anbima
def holidays(url=None, path=None):
    if not url:
        url = 'http://www.anbima.com.br/feriados/arqs/feriados_nacionais.xls'
    if not path:
        path = 'feriados_nacionais.xls'
    try:
        wb = xlrd.open_workbook(path)
    except:
        response = urlretrieve(url, filename=path)
        wb = xlrd.open_workbook(path)
    ws = wb.sheet_by_index(0)
    i = 1
    dates = []
    while ws.cell_type(i, 0) == 3:
        y, m, d, _, _, _ = xlrd.xldate_as_tuple(
            ws.cell_value(i, 0), wb.datemode)
        dates.append(date(y, m, d))
        i += 1
    return dates

# Cria calendário de feriados nacionais


class CustomBusinessCalendar(AbstractHolidayCalendar):
    rules = [Holiday('Brazil Holiday', month=date.month,
                     day=date.day, year=date.year) for date in holidays()]


def get_busdays(start_date, end_date):
    # Cria calendário de dias úteis
    custom_business_day = CustomBusinessDay(calendar=CustomBusinessCalendar())
    dates = pd.bdate_range(start=start_date, end=end_date,
                           freq=custom_business_day)
    return len(dates)


engine1 = create_engine(
    "postgresql://postgres:admin@192.168.88.61:5432/yield_debentures")

# di_df = pd.read_sql(
#     "SELECT * FROM curvas_juros ORDER BY data_referencia DESC", engine1)

di_df = pd.read_excel('curvadi_1902.xlsx')
maturity = di_df['tenor'].tolist()
pre = di_df['bid_yield'].tolist()
# print(maturity)
# print(pre)
codigo_ticker = 'AEGE17'
quantidade = 5000
dados_gerais = pd.read_sql(f"""select codigo_ativo, taxa_indicativa, data_referencia 
from dados_debenture 
where codigo_ativo = '{codigo_ticker}' and data_referencia = '2025-02-20'""", engine1)

# pre = di_df.iloc[0]['pre']
# maturity = di_df.iloc[0]['maturity']

# primeiro_nan = pd.Series(pre).isna().idxmax()

# pre = pre[0:primeiro_nan]

# maturity_days = [252*item for item in maturity]
# maturity_days = maturity_days[0:primeiro_nan]

# print(pre)
# print(maturity_days)

engine2 = create_engine(
    "postgresql://postgres:admin@192.168.88.61:5432/posicoesdb")
data_atual = str(datetime.now()).split(" ")[0]
data_atual = "2025-02-20"
ano = datetime.strptime(data_atual, "%Y-%m-%d").year

# PUXAR O TIPO DE EVENTO

dados = pd.read_sql(
    f"SELECT data_evento, percentual_taxa, pu, cdi, days, evento, valor_recebido, juros_pagos FROM cp_eventos_debenture_di WHERE codigo_ticker = '{codigo_ticker}' ORDER BY data_liquidacao DESC", engine2)

dia_evento = dados['data_evento'].tolist()
dia_evento = [str(d).split(" ")[0] for d in dia_evento]

# pu = dados['pu'].tolist()
juros_pagos = dados['valor_recebido'].tolist()

juros_pagos = [x/quantidade for x in juros_pagos]

ano_ult_event = datetime.strptime(dia_evento[0], "%Y-%m-%d").year

datas_uteis = []

for year in range(ano, ano_ult_event+1):
    datas = cria_calendario(year)
    datas = [d.strftime("%Y-%m-%d") for d in datas]
    datas_uteis = datas_uteis + datas


indice_atual = datas_uteis.index(data_atual)
dias_vencimento = list()
for item in dia_evento:
    # try:
    #     indice_fim = datas_uteis.index(item)
    # except:
    #     indice_fim = bisect.bisect_right(datas_uteis, item)  # Find the right position
    #     if indice_fim == len(datas_uteis):  # If it's past the last business day
    #         raise ValueError("No future business day available")

    data_alvo = datetime.strptime(item, '%Y-%m-%d')
    # print(indice_fim - indice_atual)
    retorno = get_busdays(data_atual, data_alvo)
    if retorno > 0:
        # print(retorno)
        dias_vencimento.append(retorno)

print(dias_vencimento)

taxas_dias = list()
for item in dias_vencimento:
    for dias in maturity:
        if dias >= item:
            x2 = dias
            i1 = maturity.index(x2)
            x1 = maturity[i1-1]
            try:
                xp = maturity[i1+1]
            except:
                xp = x2
            y2 = pre[i1]
            y1 = pre[i1-1]
            m = (y2-y1)/(x2-x1)
            b = y1-m*x1

            part1 = (1 + y1 / 100)
            part2 = (1 + y2 / 100) / (1 + y1 / 100)
            exponent = (x2 - x1) / (xp - x1)

            result = ((part1 * (part2 ** exponent)) - 1) * 100

            # taxas_dias.append(m*item+b)
            taxas_dias.append(result)
            break

# print(taxas_dias)
# print(dias_vencimento)

taxa_atual = float(dados_gerais.loc[0]['taxa_indicativa'])

di_ano_atual = 13.15
spread = 1.6  # taxa_atual
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
