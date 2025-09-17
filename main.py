import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.title("🏙️ Análise de Imóveis em São Paulo")

st.markdown("""
Este dashboard interativo permite explorar e analisar dados de imóveis à venda na cidade de São Paulo.
Use filtros na barra lateral para segmentar os dados por tipo, bairro, características e preço.
"""
)

@st.cache_data
def load_data():
    df = pd.read_csv("./data/sao_paulo_imoveis_2019.csv")
    return df

df_raw = load_data()

st.subheader("Dados Brutos")
st.dataframe(df_raw.head())