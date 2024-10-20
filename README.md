# Municipios do Brasil: Projeto python

## Introdução

O objetivo deste projeto é realizar uma análise de dados com informações de municipios brasileiros.


## Dependências

Para executar os scripts deste projeto, você precisará das seguintes bibliotecas:

* pandas: `2.2.3`
* xlrd: `2.0.1`
* requests: `2.32.3`
* pyyaml: `6.0.2`

<O que está sendo feito>
## Resultados <Alterar>

Os testes foram realizados em um laptop equipado com um processador M1 da Apple e 8GB de RAM. As implementações utilizaram abordagens puramente Python, Pandas, Dask, Polars e DuckDB. Os resultados de tempo de execução para processar o arquivo de 1 bilhão de linhas são apresentados abaixo:

| Implementação | Tempo |
| --- | --- |
| Bash + awk | 25 minutos |
| Python | 20 minutos |
| Python + Pandas | 263 sec |
| Python + Dask | 155.62 sec  |
| Python + Polars | 33.86 sec |
| Python + Duckdb | 14.98 sec |

Obrigado por [Koen Vossen](https://github.com/koenvo) pela implementação em Polars e [Arthur Julião](https://github.com/ArthurJ) pela implementação em Python e Bash 

## Conclusão <Alterar>

Este desafio destacou claramente a eficácia de diversas bibliotecas Python na manipulação de grandes volumes de dados. Métodos tradicionais como Bash (25 minutos), Python puro (20 minutos) e até mesmo o Pandas (5 minutos) demandaram uma série de táticas para implementar o processamento em "lotes", enquanto bibliotecas como Dask, Polars e DuckDB provaram ser excepcionalmente eficazes, requerendo menos linhas de código devido à sua capacidade inerente de distribuir os dados em "lotes em streaming" de maneira mais eficiente. O DuckDB se sobressaiu, alcançando o menor tempo de execução graças à sua estratégia de execução e processamento de dados.

Esses resultados enfatizam a importância de selecionar a ferramenta adequada para análise de dados em larga escala, demonstrando que Python, com as bibliotecas certas, é uma escolha poderosa para enfrentar desafios de big data.

Duckdb vence tambem com 1 milhao de linhas, realmente é o melhor

## Como Executar <Alterar>

Para executar este projeto e reproduzir os resultados:

1. Clone esse repositório
2. Definir a versao do Python usando o `pyenv local 3.12.1`
2. `poetry env use 3.12.1`, `poetry install --no-root` e `poetry lock --no-update`
3. Execute o comando `python src/create_measurements.py` para gerar o arquivo de teste
4. Tenha paciência e vá fazer um café, vai demorar uns 10 minutos para gerar o arquivo
5. Certifique-se de instalar as versões especificadas das bibliotecas Dask, Polars e DuckDB
6. Execute os scripts `python src/using_python.py`, `python src/using_pandas.py`, `python src/using_dask.py`, `python src/using_polars.py` e `python src/using_duckdb.py` através de um terminal ou ambiente de desenvolvimento que suporte Python.

Este projeto destaca a versatilidade do ecossistema Python para tarefas de processamento de dados, oferecendo valiosas lições sobre escolha de ferramentas para análises em grande escala.

## Bonus <Alterar>

Para rodar o script Bash descrito, você precisa seguir alguns passos simples. Primeiro, assegure-se de que você tenha um ambiente Unix-like, como Linux ou macOS, que suporta scripts Bash nativamente. Além disso, verifique se as ferramentas utilizadas no script (`wc`, `head`, `pv`, `awk`, e `sort`) estão instaladas em seu sistema. A maioria dessas ferramentas vem pré-instalada em sistemas Unix-like, mas `pv` (Pipe Viewer) pode precisar ser instalado manualmente.

### Preparando o Script

1. Dê permissão de execução para o arquivo script. Abra um terminal e execute:
    
    ```bash
    chmod +x process_measurements.sh
    ```

2. Rode o script. Abra um terminal e execute:
   
   ```bash
   ./src/using_bash_and_awk.sh 1000
   ```

Neste exemplo, apenas as primeiras 1000 linhas serão processadas.

Ao executar o script, você verá a barra de progresso (se pv estiver instalado corretamente) e, eventualmente, a saída esperada no terminal ou em um arquivo de saída, se você decidir modificar o script para direcionar a saída.

## Origem dos dados

1. estimativa_dou_2024.xls (Data de download: 04/10/2024): [Link - Pasta: Estimativas_2024 - Arquivo: estimativa_dou_2024.xls](https://www.ibge.gov.br/estatisticas/sociais/populacao/9103-estimativas-de-populacao.html?=&t=downloads)

2. AR_BR_RG_UF_RGINT_MES_MIC_MUN_2022.xls (Data de download: 16/10/2024): [Link - Arquivo: Área territorial - Brasil, Grandes Regiões, Unidades da Federação e Municípios](https://www.ibge.gov.br/geociencias/organizacao-do-territorio/estrutura-territorial/15761-areas-dos-municipios.html)# municipios_brasil
