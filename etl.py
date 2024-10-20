import pandas as pd
from datetime import datetime
import requests
import yaml
import json
from decorator_log_time import time_log_decorator


#===========#
#  EXTRACT  #
#===========#

@time_log_decorator
def extrair_dados_populacao(pasta: str, arquivo: str, planilha: str) -> pd.DataFrame:
    df_populacao = pd.read_excel(pasta + '/' + arquivo,
                                 header=[1],
                                 skipfooter=2,
                                 sheet_name=planilha)
    return df_populacao

@time_log_decorator
def extrair_dados_area(pasta: str, arquivo: str, planilha: str) -> pd.DataFrame:
    df_area = pd.read_excel(pasta + '/' + arquivo,
                            skipfooter=3,
                            sheet_name=planilha,
                            usecols=['CD_MUN', 'AR_MUN_2022'])
    return df_area

@time_log_decorator
def extrair_dados_api(top_municipio_pop: list, api_key: str) -> pd.DataFrame:
    dados_clima = []
    for municipio in top_municipio_pop:
        url = f'https://api.openweathermap.org/data/2.5/weather?q={municipio},br&appid={api_key}&units=metric'
        resposta = requests.get(url)
        if resposta.status_code == 200:
            dados_clima.append(resposta.json())
        else:
            print(f'Error fetching weather data for {municipio}')    
    df_clima = pd.json_normalize(dados_clima)
    df_clima = df_clima.explode('weather')
    df_clima = pd.concat([df_clima.drop(columns=['weather']).reset_index(drop=True),
                          pd.json_normalize(df_clima['weather']).reset_index(drop=True)], axis=1)
    return df_clima

#===========#
# TRANSFORM #
#===========#

@time_log_decorator
def transformacao_renomear_colunas_populacao(df_populacao: pd.DataFrame) -> pd.DataFrame:
    df_populacao.rename(columns={
        'COD. UF': 'CD_UF',
        'COD. MUNIC': 'CD_MUNICIPIO',
        'NOME DO MUNICÍPIO': 'MUN',
        'POPULAÇÃO ESTIMADA': 'POP_EST'
    }, inplace=True)
    return df_populacao

@time_log_decorator
def transformacao_renomear_colunas_area(df_area: pd.DataFrame) -> pd.DataFrame:
    df_area.rename(columns={
        'AR_MUN_2022': 'AREA_MUN',
    }, inplace=True)
    return df_area

@time_log_decorator
def transformacao_densidade_populacional(df_populacao: pd.DataFrame, df_area: pd.DataFrame) -> pd.DataFrame:
    df_populacao['CD_MUN_IBGE'] = df_populacao['CD_UF']*(10**5) + df_populacao['CD_MUNICIPIO']
    df_dens_pop = pd.merge(df_populacao,
                           df_area,
                           left_on='CD_MUN_IBGE',
                           right_on='CD_MUN',
                           how='outer')
    df_dens_pop['DENS_POP'] = (df_dens_pop['POP_EST'] / df_dens_pop['AREA_MUN']).round(1)
    df_dens_pop = df_dens_pop.sort_values(by=['DENS_POP'], ascending=False).reset_index(drop = True)
    return df_dens_pop

@time_log_decorator
def transformacao_dados_estado(df_populacao: pd.DataFrame) -> pd.DataFrame:
    df_estado=df_populacao.groupby('UF').agg(
        QT_MUN=('UF', 'size'),
        POP_EST=('POP_EST', 'sum')
    ).sort_values(by=['POP_EST'],
                  ascending=False
                  ).reset_index()
    return df_estado

@time_log_decorator
def transformacao_converte_horario(df_clima: pd.DataFrame) -> pd.DataFrame:
    def converter_timestamp(timestamp, timezone):
        return datetime.fromtimestamp(timestamp + timezone).strftime('%d/%m/%Y %H:%M:%S')
    df_clima['dt'] = df_clima.apply(lambda row: converter_timestamp(row['dt'], row['timezone']), axis=1)
    df_clima['sys.sunrise'] = df_clima.apply(lambda row: converter_timestamp(row['sys.sunrise'], row['timezone']), axis=1)
    df_clima['sys.sunset'] = df_clima.apply(lambda row: converter_timestamp(row['sys.sunset'], row['timezone']), axis=1)
    return df_clima


#===========#
#   LOAD    #
#===========#

@time_log_decorator
def carregar_dados(output_dir: str,output_file: str, df_populacao: pd.DataFrame, formato: str = 'csv'):
    if formato == 'csv':
        df_populacao.to_csv(output_dir + '/' + output_file + '.csv',
                            index=False,
                            sep=';')
    elif  formato == 'xlsx':
        df_populacao.to_excel(output_dir + '/' + output_file + '.xlsx',
                              index=False)


#===========#
#   UTILS   #
#===========#

@time_log_decorator
def ler_chave_api() -> str:
    pasta_config = 'configs'
    arquivo_config = 'config.yaml'
    try:
        with open(pasta_config + '/' + arquivo_config, "r") as file:
            config = yaml.safe_load(file)
            return config['api_key']
    except FileNotFoundError:
        print("Config file not found. Please create a 'config.yaml' file.")
        return None
    except yaml.YAMLError as e:
        print(f"Error loading YAML file: {e}")
        return None
    

def pipeline():
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    pasta_input = 'data/raw'
    pasta_output = 'data/processed'
    populacao = 'estimativa_dou_2024.xls'
    planilha_populacao = 'MUNICÍPIOS'
    area = 'AR_BR_RG_UF_RGINT_MES_MIC_MUN_2022.xls'
    planilha_area = 'AR_BR_MUN_2022'
    quant_municipios_clima = 60
    arquivo_dados_municipio=f'dados_municipio_{timestamp}'
    arquivo_dados_estado=f'dados_estado_{timestamp}'
    arquivo_dados_clima=f'dados_clima_{timestamp}'
    df_populacao = extrair_dados_populacao(pasta_input, populacao, planilha_populacao)
    df_area = extrair_dados_area(pasta_input, area, planilha_area)
    df_populacao = transformacao_renomear_colunas_populacao(df_populacao)
    df_area = transformacao_renomear_colunas_area(df_area)
    df_dens_pop = transformacao_densidade_populacional(df_populacao, df_area)
    df_estado = transformacao_dados_estado(df_populacao)
    df_clima = extrair_dados_api(df_dens_pop['MUN'][:quant_municipios_clima].tolist(), ler_chave_api())
    df_clima = transformacao_converte_horario(df_clima)
    carregar_dados(pasta_output, arquivo_dados_municipio, df_dens_pop)
    carregar_dados(pasta_output, arquivo_dados_estado, df_estado)
    carregar_dados(pasta_output, arquivo_dados_clima, df_clima, 'xlsx')

if __name__ == '__main__':
    pipeline()