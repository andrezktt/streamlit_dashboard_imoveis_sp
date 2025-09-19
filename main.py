import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit import sidebar

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

st.sidebar.markdown("---")
st.sidebar.markdown("**Preços e Área**")

price_label = "Preço (R$)" if negotiation_type == "sale" else "Aluguel (R$)"
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

sidebar.markdown("---")
st.sidebar.markdown("**Cômodos e Vagas**")
rooms_range = st.sidebar.slider(
    label="Número de Quartos",
    min_value=0,
    max_value=int(df_selection["Rooms"].max()),
    value=(0, int(df_selection["Rooms"].max()))
)
parking_range = st.sidebar.slider(
    label="Vagas na Garagem",
    min_value=0,
    max_value=int(df_selection["Parking"].max()),
    value=(0, int(df_selection["Parking"].max()))
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Características Adicionais**")
use_elevator = st.sidebar.checkbox("Com Elevador", value=False) # Inicia desmarcado para busca mais ampla
is_furnished = st.sidebar.checkbox("Mobiliado")
has_pool = st.sidebar.checkbox("Com Piscina")
is_new = st.sidebar.checkbox("Imóvel Novo")

df_filtered = df_selection[
    (df_selection['Property Type'] == property_type) &
    (df_selection['Price'] >= price_range[0]) &
    (df_selection['Price'] <= price_range[1]) &
    (df_selection['Size'] >= size_range[0]) &
    (df_selection['Size'] <= size_range[1]) &
    (df_selection['Rooms'] >= rooms_range[0]) &
    (df_selection['Rooms'] <= rooms_range[1]) &
    (df_selection['Parking'] >= parking_range[0]) &
    (df_selection['Parking'] <= parking_range[1])
]

if districts:
    df_filtered = df_filtered[df_filtered["District"].isin(districts)]

if use_elevator:
    df_filtered = df_filtered[df_filtered['Elevator'] == 1]
if is_furnished:
    df_filtered = df_filtered[df_filtered['Furnished'] == 1]
if has_pool:
    df_filtered = df_filtered[df_filtered['Swimming Pool'] == 1]
if is_new:
    df_filtered = df_filtered[df_filtered['New'] == 1]

st.header(f"Resultados de imóveis para {"Aluguel" if negotiation_type == 'rent' else "Compra"}: {df_filtered.shape[0]} encontrados")
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

st.markdown("---")

st.header("Análise Geográfica e de Preços")

col_map, col_expensive = st.columns(2)

with col_map:
    st.subheader("Mapa de Densidade de Preços")
    if not df_filtered.empty:
        centro_sp = {'lat': -23.5505, "lon": -46.6333}
        fig_map = px.scatter_map(
            data_frame=df_filtered,
            lat="Latitude",
            lon="Longitude",
            color="Price_m2",
            size="Size",
            color_continuous_scale=px.colors.cyclical.IceFire,
            size_max=15,
            center=centro_sp,
            zoom=10,
            hover_name="District",
            hover_data={"Price": ":,.2f", "Size": True}
        )
        fig_map.update_layout(map_style="carto-positron")
        fig_map.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.write("Mapa Indisponível. Selecione filtros que retornem algum imóvel.")

with col_expensive:
    st.subheader("Top 10 Bairros Mais Caros por m²")
    if not df_filtered.empty and districts:
        df_districts = df_filtered.groupby("District")["Price_m2"].mean().sort_values(ascending=False).reset_index()
        fig_bar = px.bar(
            data_frame=df_districts.head(10),
            x="District",
            y="Price_m2",
            labels={"Districts": "Bairros", "Price_m2": "Preço por m² (R$)"},
            color="Price_m2",
            color_continuous_scale="Blues"
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.warning("Selecione pelo menos um bairro para ver o gráfico.")

st.markdown("---")

st.header("Análise de Investimento: Comprar vs. Alugar")

df_selling = df[df['Negotiation Type'] == 'sale'].groupby('District')['Price'].mean()

df_renting = df[df['Negotiation Type'] == 'rent'].groupby('District')['Price'].mean()

df_ratio = pd.concat([df_selling, df_renting], axis=1)
df_ratio.columns = ['Selling_Price', 'Renting_Price']
df_ratio.dropna(inplace=True)

df_ratio['Ratio'] = df_ratio['Selling_Price'] / (df_ratio['Renting_Price'] * 12)
df_ratio = df_ratio.sort_values('Ratio', ascending=False).reset_index()

fig_ratio = px.bar(
    df_ratio.head(25),
    x='District',
    y='Ratio',
    title='Índice Preço/Aluguel por Bairro (Quanto maior, mais caro é comprar vs. alugar)',
    labels={'District': 'Bairro', 'Ratio': 'Índice (Preço Venda / Aluguel Anual)'}
)
st.plotly_chart(fig_ratio, use_container_width=True)
st.info("O Índice Preço/Aluguel é um indicador para avaliar o custo de propriedade em relação ao aluguel. Valores mais altos indicam que pode ser financeiramente mais vantajoso alugar, enquanto valores mais baixos podem indicar uma boa oportunidade de compra.")

st.markdown("---")

st.header("Análises Detalhadas")
col_sct, col_cond = st.columns(2)

with col_sct:
    st.subheader("Relação entre Área e Preço")
    if not df_filtered.empty and districts:
        fig_scatter = px.scatter(
            data_frame=df_filtered,
            x="Size",
            y="Price",
            color="District",
            title="Área vs Preço",
            labels={"Size": "Área (m²)", "Price": "Preço (R$)"}
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    else:
        st.warning("Selecione pelo menos um bairro para gerar este gráfico.")

with col_cond:
    st.subheader("Valor Médio do Condomínio por Bairro")
    if not df_filtered.empty and districts:
        df_condo_district = df_filtered.groupby("District")["Condo"].mean().sort_values(ascending=False).reset_index()
        fig_condo_bar = px.bar(
            data_frame=df_condo_district.head(10),
            x="District",
            y="Condo",
            title="Top 10 Bairros por Valor Médio de Condomínio",
            color="Condo",
            color_continuous_scale="Blues"
        )
        st.plotly_chart(fig_condo_bar, use_container_width=True)
    else:
        st.warning("Selecione pelo menos um bairro para gerar este gráfico.")

st.markdown("---")

st.header("🔎 Análise Detalhada de um Bairro Específico")
district_list = sorted(df_selection["District"].unique())
selected_district = st.selectbox(
    label="Selecione um bairro para ver os detalhes",
    options=district_list
)

df_selected_district = df_selection[df_selection["District"] == selected_district]

if not df_selected_district.empty:
    st.subheader(f"Estatísticas de '{selected_district}'")
    price_label = "Preço Médio" if negotiation_type == "sale" else "Aluguel Médio"

    avg_price = df_selected_district["Price"].mean()
    avg_condo = df_selected_district["Condo"].mean()
    avg_size = df_selected_district["Size"].mean()
    avg_rooms = df_selected_district["Rooms"].mean()
    avg_parking = df_selected_district["Parking"].mean()

    col_01, col_02, col_03, col_04, col_05 = st.columns(5)
    col_01.metric(label=price_label, value=f"R$ {avg_price:,.2f}")
    col_02.metric(label="Condomínio Médio", value=f"R$ {avg_condo:,.2f}")
    col_03.metric(label="Área Média", value=f"{avg_size:.2f} m²")
    col_04.metric(label="Nº Médio de Quartos", value=f"{avg_rooms:.0f}")
    col_05.metric(label="Nº Médio de Vagas", value=f"{avg_parking:.0f}")

    st.markdown("---")

    col_hist1, col_hist2 = st.columns(2)

    with col_hist1:
        # Histograma de Preços/Aluguéis
        fig_hist_price_bairro = px.histogram(
            df_selected_district,
            x='Price',
            nbins=25,
            title=f"Distribuição de Preços ({negotiation_type})"
        )
        st.plotly_chart(fig_hist_price_bairro, use_container_width=True)

    with col_hist2:
        # Histograma de Área (m²)
        fig_hist_size_bairro = px.histogram(
            df_selected_district,
            x='Size',
            nbins=25,
            title="Distribuição de Área (m²)",
        )
        st.plotly_chart(fig_hist_size_bairro, use_container_width=True)
else:
    st.warning("Não há dados para o bairro selecionado com os filtros atuais.")