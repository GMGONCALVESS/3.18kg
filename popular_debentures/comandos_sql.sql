 -- SELECT * FROM dados_debenture --ORDER BY data_referencia DESC-- WHERE taxa_indicativa IS NULL ORDER BY codigo_ativo COUNT UNIQUE codigo_ativo --WHERE codigo_ativo = 'VNTT11' ORDER BY data_referencia ASC --ORDER BY data_referencia, codigo_ativo DESC
-- DELETE FROM dados_debenture
-- SELECT DISTINCT codigo_ativo 
-- FROM dados_debenture 
-- WHERE taxa_indicativa IS NULL;

CREATE TABLE copia_dados_debenture AS SELECT * FROM dados_debenture;