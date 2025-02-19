from sqlalchemy import text, create_engine
import pandas as pd
import numpy as np
from receber_codigos import codigos


nao_associados = codigos()

# print(nao_associados)

engine = create_engine(
    "postgresql://postgres:admin@192.168.88.61:5432/yield_debentures")

# print(len(nao_associados))
# fazer um select distinct like em cada um dos codigos, para pegar o emissor
ticker_empresa = dict()
for item in nao_associados:
    # print(item)
    query = text(f"""
    SELECT DISTINCT TRIM(REGEXP_REPLACE(emissor, '[^a-zA-Z0-9 ]', '', 'g')) AS emissor_clean
    FROM pbi_plot_debentures
    WHERE codigo_ativo IS NOT NULL and codigo_ativo like '%{item}%' """)
    emissor = pd.read_sql(query, engine)
    try:
        # if emissor["emissor_clean"].dropna().iloc[0] == "":
        #     continue
        empresa = emissor["emissor_clean"].dropna(
        ).loc[emissor["emissor_clean"] != ""].iloc[0]
        ticker_empresa[item] = empresa
        # print(type(emissor["emissor_clean"].dropna().iloc[0]))
    except:
        continue

print(ticker_empresa)
print(len(ticker_empresa))


# realizar um codigo que analisa se os ticker recebidos no pbi_plot
# nao está presente no banco de setores


# Setor: ["Bens Industriais",
# "Outros",
# "Materiais Básicos",
# "Títulos Públicos",
# "Tecnologia da Informação",
# "Consumo não Cíclico",
# "Consumo Cíclico",
# "Índice",
# "Comunicações",
# "Financeiro",
# "Petróleo, Gás e Biocombustíveis",
# "Saúde",
# "Utilidade Pública"]

# Subsetor
# "Agropecuária"
# "Água e Saneamento"
# "Exploração de Imóveis"
# "Transporte"
# "Outros"
# "Madeira e Papel"
# "Energia Elétrica"
# "Títulos Públicos"
# "Comércio Varejista"
# "Material de Transporte"
# "Equipamentos"
# "Diversos"
# "Mídia"
# "Químicos"
# "Outros Títulos"
# "Gás"
# "Alimentos Processados"
# "Tecidos, Vestuário e Calçados"
# "Holdings Diversificadas"
# "Programas e Serviços"
# "Serviços Diversos"
# "Serviços Financeiros Diversos"
# "Embalagens"
# "Automóveis e Motocicletas"
# "Siderurgia e Metalurgia"
# "Bebidas"
# "Intermediários Financeiros"
# "Computadores e Equipamentos"
# "Utilidades Domésticas"
# "Produtos de Cuidado Pessoal e de Limpeza"
# "Hoteis e Restaurantes"
# "Construção e Engenharia"
# "Mineração"
# "Medicamentos e Outros Produtos"
# "Previdência e Seguros"
# "Securitizadoras de Recebíveis"
# "Comércio"
# "Telecomunicações"
# "Viagens e Lazer"
# "Índice"
# "Serviços Médico - Hospitalares, Análises e Diagnósticos"
# "Mercado de Capitais"
# "Construção Civil"
# "Petróleo, Gás e Biocombustíveis"
# "Comércio e Distribuição"
# "Materiais Diversos"
# "Máquinas e Equipamentos"

# Segmento
# "Exploração de Imóveis"
# "Hotelaria"
# "Serviços Educacionais"
# "Energia Elétrica"
# "Açucar e Alcool"
# "Títulos Públicos"
# "Publicidade e Propaganda"
# "Fertilizantes e Defensivos"
# "Bancos"
# "Máq. e Equip. Construção e Agrícolas"
# "Material de Transporte"
# "Equipamentos"
# "Móveis"
# "Outros Títulos"
# "Químicos Diversos"
# "Holdings Diversificadas"
# "Armas e Munições"
# "Serviços Financeiros Diversos"
# "Embalagens"
# "Restaurante e Similares"
# "Automóveis e Motocicletas"
# "Construção Pesada"
# "Computadores e Equipamentos"
# "Exploração, Refino e Distribuição"
# "Siderurgia"
# "Soc. Arrendamento Mercantil"
# "Artefatos de Cobre"
# "Produtos de Cuidado Pessoal"
# "Carnes e Derivados"
# "Produtos para Construção"
# "Medicamentos e Outros Produtos"
# "Produção de Eventos e Shows"
# "Securitizadoras de Recebíveis"
# "Produtos de Limpeza"
# "Gestão de Recursos e Investimentos"
# "Máq. e Equip. Industriais"
# "Engenharia Consultiva"
# "Alimentos Diversos"
# "Petroquímicos"
# "Alimentos"
# "Corretoras de Seguros e Resseguros"
# "Motores, Compressores e Outros"
# "Transporte Hidroviário"
# "Minerais Metálicos"
# "Intermediação Imobiliária"
# "Exploração de Rodovias"
# "Água e Saneamento"
# "Madeira"
# "Bicicletas"
# "Outros"
# "Viagens e Turismo"
# "Equipamentos e Serviços"
# "Material Rodoviário"
# "Artefatos de Ferro e Aço"
# "Aluguel de carros"
# "Transporte Rodoviário"
# "Fios e Tecidos"
# "Gás"
# "Tecidos, Vestuário e Calçados"
# "Transporte Ferroviário"
# "Programas e Serviços"
# "Serviços Diversos"
# "Acessórios"
# "Eletrodomésticos"
# "Agricultura"
# "Utensílios Domésticos"
# "Calçados"
# "Serviços de Apoio e Armazenagem"
# "Soc. Crédito e Financiamento"
# "Papel e Celulose"
# "Material Aeronáutico e de Defesa"
# "Incorporação"
# "Programas de Fidelização"
# "Produtos Diversos"
# "Brinquedos e Jogos"
# "Telecomunicações"
# "Seguradoras"
# "Índice"
# "Atividades Esportivas"
# "Serviços Médico - Hospitalares, Análises e Diagnósticos"
# "Linhas Aéreas de Passageiros"
# "Vestuário"
# "Materiais Diversos"
# "Cervejas e Refrigerantes"
