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

df_filtered = df_selection[
    (df_selection['Property Type'] == property_type) &
    (df_selection['Price'] >= price_range[0]) &
    (df_selection['Price'] <= price_range[1]) &
    (df_selection['Size'] >= size_range[0]) &
    (df_selection['Size'] <= size_range[1])
]

if districts:
    df_filtered = df_filtered[df_filtered["District"].isin(districts)]

st.header(f"Resultados de imóveis para {"aluguel" if negotiation_type == 'rent' else "compra"}: {df_filtered.shape[0]} encontrados")
st.subheader("Estatísticas Gerais")
col_01, col_02, col_03, col_04 = st.columns(4)
if not df_filtered.empty:
    metric_price_label = "Preço Médio" if negotiation_type == "sale" else "Aluguel Médio"
    col_01.metric(label=metric_price_label, value=f"R$ {df_filtered['Price'].mean():,.2f}")
    col_02.metric(label="Condomínio Médio", value=f"R$ {df_filtered['Condo'].mean():,.2f}")
    col_03.metric(label="Área Média", value=f"{df_filtered['Size'].mean():.2f} m²")
    col_04.metric(label="Preço/m² Médio", value=f"R$ {df_filtered['Price_m2'].mean():,.2f}")
else:
    st.warning("Nenhum imóvel encontrado com os filtros selecionados.")