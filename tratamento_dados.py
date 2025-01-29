from sqlalchemy import create_engine, text


def tratar(item):
    try:
        grupo = item.get('grupo')
        codigo_ativo = item.get('codigo_ativo')
        data_referencia = item.get('data_referencia')
        data_vencimento = item.get('data_vencimento')
        percentual_taxa = item.get('percentual_taxa')
        taxa_compra = item.get('taxa_compra')
        taxa_venda = item.get('taxa_venda')
        taxa_indicativa = item.get('taxa_indicativa')
        desvio_padrao = item.get('desvio_padrao')
        val_min_intervalo = item.get('val_min_intervalo')
        val_max_intervalo = item.get('val_max_intervalo')
        pu = item.get('pu')
        percent_pu_par = item.get('percent_pu_par')
        duration = item.get('duration')
        percent_reune = item.get('percent_reune')
        data_finalizado = item.get('data_finalizado')
        emissor = item.get('emissor')
        referencia_ntnb = item.get('referencia_ntnb')

        if '+' in percentual_taxa:
            x = percentual_taxa.split('+')
            indexador = x[0]
            taxa_emissao = x[1]
        elif 'do' in percentual_taxa:
            x = percentual_taxa.split('do')
            indexador = x[1]
            taxa_emissao = x[0]
        else:
            indexador = percentual_taxa
            taxa_emissao = None
        try:
            y = data_finalizado.split('T')
            data_finalizado = y[0]
            hora_finalizado = y[1]
        except:
            data_finalizado = None
            hora_finalizado = None

        # Query para insertar dados na tabela
        insert_query = text("""
        INSERT INTO dados_debenture (
            grupo, codigo, data_referencia, data_vencimento, 
            indexador, taxa_emissao, taxa_compra, taxa_venda, taxa_indicativa, 
            desvio_padrao, val_min, val_max, pu, pu_par, 
            duration, percent_renue, data_fim, hora_fim, emissor, referencia_ntnb
        ) 
        VALUES (
            :grupo, :codigo_ativo, :data_referencia, :data_vencimento, 
            :indexador, :taxa_emissao, :taxa_compra, :taxa_venda, :taxa_indicativa, 
            :desvio_padrao, :val_min_intervalo, :val_max_intervalo, :pu, :percent_pu_par, 
            :duration, :percent_reune, :data_finalizado, :hora_finalizado, :emissor, :referencia_ntnb
        ) 
        ON CONFLICT (codigo, data_referencia) DO NOTHING;
    """)

        # print(insert_query)

        params = {"grupo": grupo,
                  "codigo_ativo": codigo_ativo,
                  "data_referencia": data_referencia,
                  "data_vencimento": data_vencimento,
                  "percentual_taxa": percentual_taxa,
                  "indexador": indexador,
                  "taxa_emissao": taxa_emissao,
                  "taxa_compra": taxa_compra,
                  "taxa_venda": taxa_venda,
                  "taxa_indicativa": taxa_indicativa,
                  "desvio_padrao": desvio_padrao,
                  "val_min_intervalo": val_min_intervalo,
                  "val_max_intervalo": val_max_intervalo,
                  "pu": pu,
                  "percent_pu_par": percent_pu_par,
                  "duration": duration,
                  "percent_reune": percent_reune,
                  "data_finalizado": data_finalizado,
                  "hora_finalizado": hora_finalizado,
                  "emissor": emissor,
                  "referencia_ntnb": referencia_ntnb}
    except Exception as e:
        print(item)
        raise e

    return insert_query, params
