from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os, zipfile, time, xlrd, random, csv, requests
from datetime import date, timedelta
from urllib.request import urlretrieve
from pandas.tseries.holiday import AbstractHolidayCalendar, Holiday
from pandas.tseries.offsets import CustomBusinessDay
import pandas as pd
from openpyxl import Workbook
from sqlalchemy import create_engine


# Specify your desired download directory
download_dir = r"C:\Users\GabrielMariano\Documents\Projetos\3.18kg\scrap_di_futuro"


# Set up Chrome options
chrome_options = Options()
# Opens browser in maximized mode
chrome_options.add_argument("--start-maximized")
# chrome_options.add_argument("--headless")  # Uncomment for headless mode
# chrome_options.add_argument("--disable-gpu")  # Necessary for headless mode on Windows

# Configure download settings
prefs = {
    "download.default_directory": download_dir,  # Set default download directory
    "download.prompt_for_download": False,      # Disable download prompts
    # Automatically upgrade downloads to the specified directory
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True                # Enable safe browsing
}
chrome_options.add_experimental_option("prefs", prefs)

# Automatically download and set up the WebDriver
driver = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=chrome_options)

delay = 5

# Cria conexão com o banco de dados
engine = create_engine(
    'postgresql://postgres:admin@192.168.88.61:5432/yield_debentures')

# Function to fill text inputs


def fill_input(xpath, value):
    WebDriverWait(driver, delay).until(
        EC.presence_of_element_located((By.XPATH, xpath)))
    input_field = driver.find_element(By.XPATH, xpath)
    input_field.clear()
    input_field.send_keys(value)

# Function to click on a button


def click_button(xpath):
    WebDriverWait(driver, delay).until(
        EC.presence_of_element_located((By.XPATH, xpath)))
    driver.find_element(By.XPATH, xpath).click()

# Function to open a link


def open_link(link):
    driver.get(link)

# Function to get element


def get_element(xpath):
    WebDriverWait(driver, delay).until(
        EC.presence_of_element_located((By.XPATH, xpath)))
    element = driver.find_element(By.XPATH, xpath)
    return element

# Function to get text from an element


def get_text(xpath):
    WebDriverWait(driver, delay).until(
        EC.presence_of_element_located((By.XPATH, xpath)))
    element = driver.find_element(By.XPATH, xpath).text
    return element


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
    rules = [Holiday('Brazil Holiday', month=d.month,
                     day=d.day, year=d.year) for d in holidays()]


def get_latest_date():
    # Pega a última data inserida no bd e soma 1 dia
    latest_date = pd.read_sql_query(
        """SELECT MAX(data_referencia) FROM curvas_juros""", engine)
    latest_date = latest_date.iloc[0, 0]
    latest_date = pd.to_datetime(latest_date) + timedelta(days=1)

    # Pega calendário do ano atual
    current_year = pd.Timestamp.now().year
    # current_year = 2024
    first_day = pd.Timestamp(year=current_year, month=1, day=1)
    last_day = pd.Timestamp(year=current_year, month=12, day=31)

    dates = pd.bdate_range(start=first_day, end=last_day,
                           freq=custom_business_day)

    # Checka se a última data está no calendário de dias úteis
    # Se não tiver soma 1 até achar um dia útil
    while latest_date not in dates:
        latest_date = latest_date + timedelta(days=1)
        print(latest_date)

    # Pega dia útil anterior ao atual
    current_d1 = (date.today() - 1 * custom_business_day)

    if latest_date <= current_d1:
        return latest_date
    else:
        print('Dia não pode ser calculado ainda')


# Cria calendário de dias úteis
custom_business_day = CustomBusinessDay(calendar=CustomBusinessCalendar())

# Pega última data disponível
latest_date = pd.to_datetime('2025-02-18')  # get_latest_date()


# print(type(latest_date))

if latest_date != 'Dia não pode ser calculado ainda':
    # Abre o link da B3
    # open_link('https://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/consultas/mercado-de-derivativos/precos-referenciais/taxas-referenciais-bm-fbovespa/')
    
    open_link('https://www2.bmf.com.br/pages/portal/bmfbovespa/lumis/lum-taxas-referenciais-bmf-ptBR.asp')
    elemento = get_element('//*[@id="Data"]')
    print(elemento)
    fill_input('//*[@id="Data"]', '18/02/2025')

    click_button('//*[@id="divContainerIframeBmf"]/form/div/div/div[1]/div[2]/div/div[2]/button')

    elemento = get_text('//*[@id="tb_principal1"]/tbody')
    elemento = elemento.strip()
    linha = str()
    linhas = list()
    for item in elemento:
        if item == '\n':
            # print(linha)
            linhas.append(linha)
            linha = str()
            continue
        linha = linha + item
    # print(linhas)
    tenor = list()
    cdi = list()
    for dados in linhas:
        x = dados.split(" ")
        tenor.append(float(x[0].replace(",",".")))
        cdi.append(float(x[1].replace(",",".")))
          
    df = pd.DataFrame({'data_referencia': latest_date, "tenor": [tenor], "bid_yield":[cdi]})

    df.to_sql("di_futuro", con=engine, if_exists="append", index=False)
else:
    print('Dia não pode ser calculado ainda')
