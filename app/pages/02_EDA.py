from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from ui import callout, inject_global_styles


ROOT = Path(__file__).resolve().parents[2]
df = pd.read_csv(ROOT / "data" / "processed" / "streaming_users_processed.csv")
PALETTE = ["#0f766e", "#e56b55", "#2f5d7c", "#b5812a", "#6d5a8d", "#4f7f52"]

inject_global_styles()

st.title("EDA")

callout(
    "Exploracion visual en cinco pasos",
    "La guia pide exactamente 5 visualizaciones: 2 univariadas, 2 bivariadas y 1 multivariada. La lectura avanza desde una variable hacia relaciones y patrones combinados.",
    "Analisis exploratorio",
)

fig1 = px.histogram(
    df,
    x="monthly_watch_time_mins",
    nbins=35,
    title="1. Univariado: distribucion del tiempo mensual",
    color_discrete_sequence=["#0f766e"],
)
fig1.update_layout(template="plotly_white")
with st.container(border=True):
    st.plotly_chart(fig1, use_container_width=True)
    st.caption(
        "La mayor parte de los usuarios se concentra en consumos medios. Tambien aparece una cola de usuarios mas intensivos; por eso conviene mirar distribucion y mediana, no solo promedio."
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
        "Este grafico muestra el peso de cada plan dentro de la base. Sirve para contextualizar el resto del analisis cuando los grupos no tienen el mismo tamano."
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
        "Este cruce permite revisar si la edad explica por si sola el consumo. La dispersion muestra que aporta contexto, pero no alcanza para describir completamente el comportamiento."
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
        "El boxplot compara medianas y dispersion de consumo entre planes. Ayuda a ver si algun plan concentra usuarios mas intensivos o si los comportamientos son similares."
    )

fig5 = px.scatter(
    df,
    x="age",
    y="monthly_watch_time_mins",
    color="favorite_genre",
    opacity=0.5,
    title="5. Multivariado: edad, consumo y genero favorito",
    color_discrete_sequence=PALETTE,
)
fig5.update_layout(template="plotly_white")
with st.container(border=True):
    st.plotly_chart(fig5, use_container_width=True)
    st.caption(
        "Esta visualizacion suma una tercera variable: el genero favorito. Permite observar si los patrones de consumo por edad cambian segun la preferencia de contenido."
    )
