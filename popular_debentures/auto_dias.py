import xlrd
from openpyxl import Workbook
import time
from datetime import datetime, date, timedelta
from urllib.request import urlretrieve
from pandas.tseries.holiday import AbstractHolidayCalendar, Holiday
from pandas.tseries.offsets import CustomBusinessDay
import pandas as pd

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


def cria_calendario(ano):
    # Cria calendário de feriados nacionais
    # Aqui estão sendo puxadas somente as regras 
    class CustomBusinessCalendar(AbstractHolidayCalendar):
        rules = [Holiday('Brazil Holiday', month=date.month,
                         day=date.day, year=date.year) for date in holidays()]

    # Cria calendário de dias úteis
    custom_business_day = CustomBusinessDay(calendar=CustomBusinessCalendar())

    # Pega calendário do ano atual
    current_year = ano
    first_day = pd.Timestamp(year=current_year, month=1, day=1)
    last_day = pd.Timestamp(year=current_year, month=12, day=31)
    # last_day = pd.Timestamp(year=current_year, month=12, day=31)

    # Lista de dados com dias úteis
    dates = pd.bdate_range(start=first_day, end=last_day,
                           freq=custom_business_day)

    return dates
