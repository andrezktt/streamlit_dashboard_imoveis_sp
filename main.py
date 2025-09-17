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

def data_processing(df):

    for col in ["Condo", "Suites", "Parking", "Toilets"]:
        df[col] = df[col].fillna(0).astype(int)

    for col in ["Elevator", "Furnished", "Swimming Pool", "New"]:
        df[col] = df[col].fillna(0).astype(int)

    df.dropna(subset=["Negotiation Type"], inplace=True)

    df["Price_m2"] = (df["Price"] / df["Size"]).round(2)
    df["Total_cost"] = df["Price"] + df["Condo"]

    return df

df_raw = load_data()
df = data_processing(df_raw)

st.subheader("Dados Brutos")
st.dataframe(df.sample(50))