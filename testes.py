import os
import requests
import pandas as pd
from datetime import date
from pandas.tseries.holiday import AbstractHolidayCalendar, Holiday
from pandas.tseries.offsets import CustomBusinessDay

# 📌 Função para obter feriados nacionais da ANBIMA


def holidays(url=None, path=None):
    if not url:
        url = 'https://www.anbima.com.br/feriados/arqs/feriados_nacionais.xls'
    if not path:
        path = 'feriados_nacionais.xls'

    # Baixa o arquivo apenas se não existir
    if not os.path.exists(path):
        response = requests.get(url)
        with open(path, 'wb') as f:
            f.write(response.content)

    # Lê o arquivo e tenta converter para datetime
    df = pd.read_excel(path)

    # Verifica o tipo da primeira coluna
    print(df.dtypes)

    # Converte apenas se não for datetime
    if not pd.api.types.is_datetime64_any_dtype(df.iloc[:, 0]):
        df.iloc[:, 0] = pd.to_datetime(df.iloc[:, 0], errors='coerce')

    # Remove valores inválidos
    df = df.dropna(subset=[df.columns[0]])

    # Aplica `.dt.date` apenas se for datetime
    if pd.api.types.is_datetime64_any_dtype(df.iloc[:, 0]):
        return df.iloc[:, 0].dt.date.tolist()
    else:
        return df.iloc[:, 0].tolist()


# 📌 Função para criar o calendário de dias úteis no ano especificado
def cria_calendario(ano):
    # 🔹 Criando uma classe personalizada de calendário com os feriados
    class CustomBusinessCalendar(AbstractHolidayCalendar):
        rules = [
            Holiday('Brazil Holiday', month=feriado.month, day=feriado.day)
            for feriado in holidays()
        ]

    # 🔹 Criando um CustomBusinessDay baseado nos feriados
    custom_business_day = CustomBusinessDay(calendar=CustomBusinessCalendar())

    # 🔹 Gerando um calendário de dias úteis para o ano especificado
    first_day = pd.Timestamp(year=ano, month=1, day=1)
    last_day = pd.Timestamp(year=ano, month=12, day=31)

    # 🔹 Lista com todos os dias úteis do ano
    dias_uteis = pd.bdate_range(
        start=first_day, end=last_day, freq=custom_business_day)

    return dias_uteis


# 📌 Exemplo: Criar calendário de dias úteis para 2025
calendario_2025 = cria_calendario(2025)
print(calendario_2025)
