# importar as bibliotecas
import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import timedelta

# criar as funções de carregamento de dados
    # Cotação do Itau - ITUB4 - 2010 a 2024

@st.cache_data
def carregar_dados(empresas):
    texto_tickers = " ".join(empresas)
    dados_acao = yf.Tickers(texto_tickers)
    cotacoes_acao = dados_acao.history(start = "2010-01-01", end = "2025-10-01", interval="1d", period=None)
    cotacoes_acao = cotacoes_acao["Close"]
    return cotacoes_acao

@st.cache_data
def carregar_tickests_acoes():
    base_tickests = pd.read_csv("IBOV.csv", sep=";")
    tickers = list(base_tickests["Código"])
    tickers = [item + ".SA" for item in tickers]
    return tickers[:10]  # só os 5 primeiros
    #return tickers

#Filtro

acoes = carregar_tickests_acoes()
dados = carregar_dados(acoes)


#criar a interface do streamlit
st.write("""
# App preço de Ações
O gráfico abaixo representa a evolução do preço das ações do Itaú (ITUB4) ao longo dos anos
""") # markdown

# prepara as visualizações = filtros
st.sidebar.header("Filtros")

#Filtro de ações
lista_acoes = st.sidebar.multiselect("Escolha as ações do filtro", dados.columns)
if lista_acoes:
    dados = dados[lista_acoes]
    if len(lista_acoes) == 1:
        acao_unica = lista_acoes[0]
        dados = dados.rename(columns={acao_unica : "Close"})        

#Filtro de datas
data_inicial = dados.index.min().to_pydatetime()
data_final = dados.index.max().to_pydatetime()
intervalo_data = st.sidebar.slider("Selecione o período", 
                                   min_value=data_inicial, 
                                   max_value=data_final, 
                                   value =(data_inicial, data_final),
                                   step= timedelta(days=30))

dados = dados.loc[intervalo_data[0]:intervalo_data[1]]

#criar gráfico
st.line_chart(dados)

#Calculo de Parformance
texto_performance_ativos = """"""

if len(lista_acoes) == 0:
    lista_acoes = list(dados.columns)
elif len(lista_acoes) == 1:
    dados = dados.rename(columns={"Close" : acao_unica}) 


carteira = [1000 for acao in lista_acoes]
total_inicial_carteira =  sum(carteira)

for i, acao in enumerate(lista_acoes):
    performance_ativo = dados[acao].iloc[-1] / dados[acao].iloc[0] - 1
    performance_ativo = float(performance_ativo)

    carteira[i] = carteira[i] * (1 + performance_ativo)

    if performance_ativo > 0:
        texto_performance_ativos = texto_performance_ativos + f"  \n{acao} : :green[{performance_ativo:.2f}]"
    elif performance_ativo < 0:
        texto_performance_ativos = texto_performance_ativos + f"  \n{acao} : :red[{performance_ativo:.2f}]"
    else:
        texto_performance_ativos = texto_performance_ativos + f"  \n{acao} : {performance_ativo:.2f}"


total_final_carteira = sum(carteira)
performance_carteira = total_final_carteira / total_inicial_carteira - 1

if performance_carteira > 0.0:
    texto_performance_carteira = f" Performance da Carteira com todos os ativos: :green[{performance_carteira:.2f}]"
elif performance_ativo < 0.0:
    texto_performance_carteira = f" Performance da Carteira com todos os ativos: :red[{performance_carteira:.2f}]"
else:
    texto_performance_carteira = f" Performance da Carteira com todos os ativos: {performance_carteira:.2f}"


st.write(f"""
### Performance dos Ativos
Essa foi a performance de cada ativo no periodo selecionado:

{texto_performance_ativos}

{texto_performance_carteira}
""") # markdown