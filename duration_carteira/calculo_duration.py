from sqlalchemy import create_engine, text
import pandas as pd
from dias import cria_calendario
from datetime import datetime

engine = create_engine(
    "postgresql://postgres:admin@192.168.88.61:5432/posicoesdb")

data_atual = str(datetime.now()).split(" ")[0]
data_atual = "2025-02-17"
ano = datetime.strptime(data_atual, "%Y-%m-%d").year

dados = pd.read_sql(
    "SELECT data_evento, percentual_taxa, pu, cdi, days FROM eventos_debenture_cdi WHERE codigo_ticker = 'AALM12' ORDER BY data_liquidacao DESC", engine)

dia_evento = dados['data_evento'].tolist()
dia_evento = [str(d).split(" ")[0] for d in dia_evento]

pu = dados['pu'].tolist()

ano_ult_event = datetime.strptime(dia_evento[0], "%Y-%m-%d").year

datas_uteis = []

for year in range(ano, ano_ult_event+1):
    datas = cria_calendario(year)
    datas = [d.strftime("%Y-%m-%d") for d in datas]
    datas_uteis = datas_uteis + datas
    # indice_ref = datas_uteis.index(data_atual)

print(datas_uteis)
indice_ref = datas_uteis.index(data_atual)
num=den=0
i = 0
for d in range(0, len(dia_evento)):
    if dia_evento[d] in datas_uteis:
        print(dia_evento[d])
        indice_final = datas_uteis.index(dia_evento[d]) 
        # print(indice_final-indice_ref, pu[i])
        num = num + pu[i]*(indice_final-indice_ref)
        den = den + pu[i]
        i+=1
    else:
        
        
print(num/den)









# pu = dados['pu'].tolist()
# dias = [str(d).split(" ")[0] for d in dias]

# # print(datas_uteis)

# num = den = 0

# for i in range(0, len(dias)):
#     # print(dias[i].split(" ")[0])
#     if dias[i] in datas_uteis:
#         indice_final = datas_uteis.index(dias[i].split(" ")[0])
#     try:
#         print(indice_final-indice_ref)
#         num = num + pu[i]*(indice_final-indice_ref)
#         den = den + pu[i]
#     except Exception as e:
#         continue

# print(num/den)
