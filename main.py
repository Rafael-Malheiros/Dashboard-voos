import streamlit as st
import pandas as pd
import plotly.express as px
import kagglehub

@st.cache_data
def load_data():
    path = kagglehub.dataset_download("rohitgrewal/airlines-flights-data", path="airlines_flights_data.csv")
    df = pd.read_csv(path)
    if 'index' in df.columns:
        df = df.drop(columns=['index'])
    return df

flights = load_data()

st.set_page_config(page_title="Dashboard de Voos", layout="wide")
st.title("✈️ Dashboard Interativo de Voos")
st.image("https://www.shutterstock.com/image-vector/airplane-flying-hud-screen-analysis-600nw-1545254336.jpg", width=500)

col1, col2, col3 = st.columns(3)

with col1:
    airline_filter = st.selectbox("Companhia Aérea", options=["Todas"] + list(flights['airline'].unique()))
with col2:
    class_filter = st.multiselect("Classe", options=flights['class'].unique(), default=flights['class'].unique())
with col3:
    max_price = st.slider("Preço Máximo (USD)", min_value=int(flights['price'].min()),
                          max_value=int(flights['price'].max()), value=int(flights['price'].max()))

df_filtered = flights.copy()
if airline_filter != "Todas":
    df_filtered = df_filtered[df_filtered['airline'] == airline_filter]
df_filtered = df_filtered[df_filtered['class'].isin(class_filter)]
df_filtered = df_filtered[df_filtered['price'] <= max_price]

col_a, col_b, col_c = st.columns(3)
col_a.metric("Total de Voos", len(df_filtered))
col_b.metric("Preço Médio (USD)", round(df_filtered['price'].mean(), 2))
col_c.metric("Duração Média (h)", round(df_filtered['duration'].mean(), 2))

st.subheader("📊 Análises Visuais")

col_g1, col_g2 = st.columns(2)

with col_g1:
    fig_duracao = px.histogram(df_filtered, x="duration", nbins=50,
                               title="Distribuição da Duração dos Voos (h)",
                               color_discrete_sequence=["#1f77b4"])
    st.plotly_chart(fig_duracao, use_container_width=True)

with col_g2:
    fig_price_class = px.box(df_filtered, x="class", y="price",
                             title="Preços por Classe", color="class")
    st.plotly_chart(fig_price_class, use_container_width=True)

fig_avg_price = px.bar(df_filtered.groupby('airline')['price'].mean().reset_index(),
                       x="airline", y="price",
                       title="Preço Médio por Companhia Aérea",
                       color="price", color_continuous_scale="Tealgrn")
st.plotly_chart(fig_avg_price, use_container_width=True)

fig_stops = px.pie(df_filtered, names="stops", title="Proporção de Voos por Número de Escalas")
st.plotly_chart(fig_stops, use_container_width=True)

st.subheader("📋 Dados filtrados")
st.dataframe(df_filtered)