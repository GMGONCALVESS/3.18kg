import xlrd
from tratamento_dados import tratar
from datetime import datetime, date, timedelta
from urllib.request import urlretrieve
from pandas.tseries.holiday import AbstractHolidayCalendar, Holiday
from pandas.tseries.offsets import CustomBusinessDay
import pandas as pd
from openpyxl import Workbook
import csv
from sqlalchemy import create_engine, text
import time
import json
from api_connect import conexao

# Cria conexão com o banco de dados
engine = create_engine(
    'postgresql://postgres:admin@192.168.88.61:5432/yield_debentures')

# Conexão com a API, passar datas de dias úteis
dados = conexao()

# Inserção de dados
for item in dados:

    resultado = tratar(item)

    with engine.connect() as conexao:
        conexao.execute(resultado[0], resultado[1])
        conexao.commit()