# Municipios do Brasil: Projeto python


## Introdução

O objetivo deste projeto é realizar uma análise de dados com informações de municipios brasileiros.


## Dependências

Para executar os scripts deste projeto, você precisará das seguintes bibliotecas:

* python: `3.12`
* pandas: `2.2.3`
* xlrd: `2.0.1`
* requests: `2.32.3`
* pyyaml: `6.0.2`
* openpyxl: `3.1.5`
* loguru: `0.7.2`

Chaves API

* [OpenWeather](https://openweathermap.org/)


## Origem dos dados

1. estimativa_dou_2024.xls (Data de download: 04/10/2024): [Link - Pasta: Estimativas_2024 - Arquivo: estimativa_dou_2024.xls](https://www.ibge.gov.br/estatisticas/sociais/populacao/9103-estimativas-de-populacao.html?=&t=downloads)

2. AR_BR_RG_UF_RGINT_MES_MIC_MUN_2022.xls (Data de download: 16/10/2024): [Link - Arquivo: Área territorial - Brasil, Grandes Regiões, Unidades da Federação e Municípios](https://www.ibge.gov.br/geociencias/organizacao-do-territorio/estrutura-territorial/15761-areas-dos-municipios.html)


## Descrição do código

1) Lê arquivo: estimativa_dou_2024.xls;
2) Lê arquivo: AR_BR_RG_UF_RGINT_MES_MIC_MUN_2022.xls;
3) Calcula densidade populacional;
4) Soma população de cada estado;
5) Extrai informações climáticas dos 60 municípios de maior densidade; populacional (necessária chave API OpenWeather);