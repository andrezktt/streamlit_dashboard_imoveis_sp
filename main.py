import streamlit as st
import pandas as pd
import plotly.express as px

# Configurando a Página Streamlit
st.set_page_config(layout="wide")

st.title("🏙️ Análise de Imóveis em São Paulo")
st.markdown("""
Este dashboard interativo permite explorar e analisar dados de imóveis à venda na cidade de São Paulo.
Use filtros na barra lateral para segmentar os dados por tipo, bairro, características e preço.
"""
)

# Carregando os Dados
@st.cache_data
def load_data():
    df = pd.read_csv("./data/sao_paulo_imoveis_2019.csv")
    return df

# Processamento e Tratamento dos Dados
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

# Barra Lateral - Filtros
st.sidebar.header("Filtros")

negotiation_type = st.sidebar.radio(
    label="Tipo de Negociação",
    options=df["Negotiation Type"].unique(),
    horizontal=True
)

df_selection = df[df["Negotiation Type"] == negotiation_type].copy()

property_type = st.sidebar.selectbox(
    label="Tipo de Imóvel",
    options=sorted(df_selection["Property Type"].unique())
)

districts = st.sidebar.multiselect(
    label="Bairros",
    options=sorted(df_selection["District"].unique()),
    default=df_selection["District"].value_counts().index[:10]
)

price_label = "Preço (R$)" if negotiation_type == "Sale" else "Aluguel (R$)"
price_range = st.sidebar.slider(
    label=price_label,
    min_value=int(df_selection["Price"].min()),
    max_value=int(df_selection["Price"].max()),
    value=(int(df_selection["Price"].min()), int(df_selection["Price"].max()))
)

size_range = st.sidebar.slider(
    label="Área (m2)",
    min_value=int(df_selection["Size"].min()),
    max_value=int(df_selection["Size"].max()),
    value=(int(df_selection["Size"].min()), int(df_selection["Size"].max()))
)