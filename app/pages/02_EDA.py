from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


ROOT = Path(__file__).resolve().parents[2]
df = pd.read_csv(ROOT / "data" / "processed" / "streaming_users_processed.csv")

st.title("EDA")

st.write(
    """
La guia pide exactamente 5 visualizaciones: 2 univariadas, 2 bivariadas y 1 multivariada.
Esta seccion respeta esa estructura. La idea es leer los datos paso a paso: primero una
variable, despues relaciones entre dos variables y finalmente una mirada combinada.
"""
)

fig1 = px.histogram(
    df,
    x="monthly_watch_time_mins",
    nbins=35,
    title="1. Univariado: distribucion del tiempo mensual",
)
st.plotly_chart(fig1, use_container_width=True)
st.write(
    """
La mayor parte de los usuarios se concentra en consumos medios. Tambien aparece una cola
de usuarios mas intensivos. Por eso, para hablar de consumo conviene mirar distribucion y
mediana, no solo promedio.
"""
)

fig2 = px.histogram(
    df,
    x="subscription_plan",
    color="subscription_plan",
    title="2. Univariado: usuarios por plan",
)
st.plotly_chart(fig2, use_container_width=True)
st.write(
    """
Este grafico muestra el peso de cada plan dentro de la base. Sirve para contextualizar el
resto del analisis: no es lo mismo comparar promedios entre grupos del mismo tamaño que
entre grupos desbalanceados.
"""
)

fig3 = px.scatter(
    df,
    x="age",
    y="monthly_watch_time_mins",
    opacity=0.45,
    title="3. Bivariado: edad y consumo mensual",
)
st.plotly_chart(fig3, use_container_width=True)
st.write(
    """
Este cruce permite revisar si la edad explica por si sola el consumo. La dispersion muestra
que la edad aporta contexto, pero no alcanza para describir completamente el comportamiento
de visualizacion.
"""
)

fig4 = px.box(
    df,
    x="subscription_plan",
    y="monthly_watch_time_mins",
    color="subscription_plan",
    title="4. Bivariado: consumo mensual por plan",
)
st.plotly_chart(fig4, use_container_width=True)
st.write(
    """
El boxplot compara medianas y dispersion de consumo entre planes. Esta lectura ayuda a ver
si algun plan concentra usuarios mas intensivos o si los comportamientos se parecen entre
segmentos.
"""
)

fig5 = px.scatter(
    df,
    x="age",
    y="monthly_watch_time_mins",
    color="favorite_genre",
    opacity=0.5,
    title="5. Multivariado: edad, consumo y genero favorito",
)
st.plotly_chart(fig5, use_container_width=True)
st.write(
    """
Esta visualizacion suma una tercera variable: el genero favorito. Permite observar si los
patrones de consumo por edad cambian segun la preferencia de contenido. Si un genero
aparece asociado a consumos mas altos, puede orientar nuevas preguntas sobre permanencia.
"""
)
