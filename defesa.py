import pandas as pd
#pip install lxml html5lib

import matplotlib.pyplot as plt
from datetime import datetime

url ='https://defesacivil.riodosul.sc.gov.br/index.php?r=externo/metragem'
try:
    tabelas = pd.read_html(url)
    #print(tabelas[0])
    df=tabelas[0]
    #print(df.tail())
    coluna_pluv='Ind.Pluv.'
    soma_pluv=pd.to_numeric(df[coluna_pluv],errors='coerce').sum()
    print("-"*50)
    print("🌧️Acumulado de chuva: ",soma_pluv)
    print("-"*50)
     # Renomear colunas para facilitar

    df.columns = ['Data_Hora', 'Nível', 'Diferença', 'Ind_Pluv', 'Tempo']


    # --- PRÉ-PROCESSAMENTO PARA CORRIGIR DATAS SEM ANO (A NOVA ETAPA) ---


    # Obtém o ano atual (usando 2025 conforme o contexto atual)

    # Para ser mais robusto, você pode usar datetime.now().year

    ano_atual = datetime.now().year


    # Função para corrigir datas curtas

    def corrigir_data(data_str):

        # Verifica se a string tem o formato curto (sem ano e com 'H' para hora)

        # Exemplo: '30/09 14H'

        if len(data_str) < 11 and 'H' in data_str:

            # Substitui 'H' por ':' e adiciona o ano atual.

            # Exemplo: '30/09 14H' -> '30/09/2025 14:00:00'

            data_corrigida = data_str.replace('H', ':00:00') + f'/{ano_atual}'

            return data_corrigida

        return data_str


    # Aplica a função de correção na coluna 'Data_Hora'

    df['Data_Hora'] = df['Data_Hora'].apply(corrigir_data)


    # --- CONVERSÃO E LIMPEZA DE DADOS ---


    # 1. Converter a coluna 'Data_Hora' de forma mista, pois agora todas têm o ano

    # O pandas ainda precisará de 'mixed' pois o formato (com ou sem segundos) pode variar.

    df['Data_Hora'] = pd.to_datetime(df['Data_Hora'], format='mixed', dayfirst=True)


    # 2. Converter a coluna 'Nível' para float, tratando erros

    df['Nível'] = pd.to_numeric(df['Nível'], errors='coerce')


    # 3. Remover linhas com valores NaN em 'Nível' e ordenar

    df.dropna(subset=['Nível'], inplace=True)

    df.sort_values(by='Data_Hora', inplace=True)

    #criando um gráfico de linhas do nível do rio
    plt.figure(figsize=(12, 6))
    plt.plot(df['Data_Hora'],df['Nível'],marker='o',linestyle='-',color='red',markersize=3)
    #rotúlos
    plt.title('Nível do Rio ao longo do tempo.',fontsize=16)
    plt.xlabel('Data e Hora',fontsize=12)
    plt.ylabel('Nível do Rio (Metros)',fontsize=12)
    plt.gcf().autofmt_xdate()
    plt.grid(True,linestyle='-',alpha=0.7)
    plt.show()
   
   
except Exception as e:
    print("Não foi possível encontrar o site")