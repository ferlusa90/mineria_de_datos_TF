from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from ui import callout, card, inject_global_styles


ROOT = Path(__file__).resolve().parents[2]
df = pd.read_csv(ROOT / "data" / "processed" / "streaming_users_processed.csv")
PALETTE = ["#0f766e", "#e56b55", "#2f5d7c", "#b5812a", "#6d5a8d", "#4f7f52"]

st.set_page_config(page_title="EDA | Streaming Users", page_icon="📈", layout="wide")
inject_global_styles()

st.sidebar.title("EDA")
st.sidebar.caption("Exploración visual del dataset")
st.sidebar.markdown("**Visualizaciones**")
st.sidebar.write("1. Distribución del consumo")
st.sidebar.write("2. Usuarios por plan")
st.sidebar.write("3. Edad vs consumo")
st.sidebar.write("4. Boxplot por plan")
st.sidebar.write("5. Edad, consumo y género")

st.markdown(
    """
    <div style="padding: 0.2rem 0 0.9rem;">
        <div style="font-size: 0.85rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: #0f766e;">
            Módulo 02
        </div>
        <h1 style="margin: 0.1rem 0 0.35rem;">EDA</h1>
        <p style="margin: 0; max-width: 860px; font-size: 1.02rem; line-height: 1.6; color: #5d6b78;">
            En esta parte dejo las cinco gráficas del EDA y la lectura principal de cada una.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

top_l, top_r = st.columns([1.02, 0.98], gap="large")
with top_l:
    callout(
        "Exploración visual en cinco pasos",
        "La guía pide exactamente 5 visualizaciones: 2 univariadas, 2 bivariadas y 1 multivariada. Arranco mirando variables sueltas y después paso a cruces entre variables.",
        "Análisis exploratorio",
    )
with top_r:
    card(
        "Resumen visual",
        "El orden elegido ayuda a leer consumo, edad, plan y género favorito sin mezclar todo desde el principio.",
        "Lectura",
        soft=True,
    )

st.write("")
metric1, metric2, metric3 = st.columns(3)
metric1.metric("Gráfica 1", "Consumo")
metric2.metric("Gráfica 3", "Edad vs consumo")
metric3.metric("Gráfica 5", "Multivariado")

fig1 = px.histogram(
    df,
    x="monthly_watch_time_mins",
    nbins=35,
    title="1. Univariado: distribución del tiempo mensual",
    color_discrete_sequence=["#0f766e"],
)
fig1.update_layout(template="plotly_white")
with st.container(border=True):
    st.plotly_chart(fig1, use_container_width=True)
    st.caption(
        "La mayor parte de los usuarios se concentra en consumos medios. También aparece una cola de usuarios más intensivos; por eso conviene mirar distribución y mediana, no solo promedio."
    )

fig2 = px.histogram(
    df,
    x="subscription_plan",
    color="subscription_plan",
    title="2. Univariado: usuarios por plan",
    color_discrete_sequence=PALETTE,
)
fig2.update_layout(template="plotly_white", showlegend=False)
with st.container(border=True):
    st.plotly_chart(fig2, use_container_width=True)
    st.caption(
        "Este gráfico muestra cuánto pesa cada plan dentro de la base. Lo tengo en cuenta porque comparar grupos muy distintos en tamaño puede cambiar la lectura."
    )

fig3 = px.scatter(
    df,
    x="age",
    y="monthly_watch_time_mins",
    opacity=0.45,
    title="3. Bivariado: edad y consumo mensual",
    color_discrete_sequence=["#2f5d7c"],
)
fig3.update_layout(template="plotly_white")
with st.container(border=True):
    st.plotly_chart(fig3, use_container_width=True)
    st.caption(
        "Este cruce me sirve para revisar si la edad explica el consumo por sí sola. La nube queda bastante dispersa, así que la edad ayuda, pero no alcanza para contar todo el comportamiento."
    )

fig4 = px.box(
    df,
    x="subscription_plan",
    y="monthly_watch_time_mins",
    color="subscription_plan",
    title="4. Bivariado: consumo mensual por plan",
    color_discrete_sequence=PALETTE,
)
fig4.update_layout(template="plotly_white", showlegend=False)
with st.container(border=True):
    st.plotly_chart(fig4, use_container_width=True)
    st.caption(
        "El boxplot compara medianas y dispersión entre planes. Acá busco si algún plan concentra usuarios más intensivos o si los consumos son parecidos."
    )

fig5 = px.scatter(
    df,
    x="age",
    y="monthly_watch_time_mins",
    color="favorite_genre",
    opacity=0.5,
    title="5. Multivariado: edad, consumo y género favorito",
    color_discrete_sequence=PALETTE,
)
fig5.update_layout(template="plotly_white")
with st.container(border=True):
    st.plotly_chart(fig5, use_container_width=True)
    st.caption(
        "Esta visualización suma una tercera variable: el género favorito. La uso para ver si el consumo por edad cambia cuando separo por preferencia de contenido."
    )
