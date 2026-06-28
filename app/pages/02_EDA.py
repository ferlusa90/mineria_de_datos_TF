from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


ROOT = Path(__file__).resolve().parents[2]
df = pd.read_csv(ROOT / "data" / "processed" / "streaming_users_processed.csv")

st.title("EDA")



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
de usuarios mas intensivos. Por eso, para interpretar consumo conviene mirar mediana,
distribucion y segmentos, no solo promedio.
"""
)

fig2 = px.scatter(
    df,
    x="age",
    y="monthly_watch_time_mins",
    opacity=0.45,
    title="2. Multivariado de 2 variables: edad y consumo mensual",
)
st.plotly_chart(fig2, use_container_width=True)
st.write(
    """
Este cruce permite revisar si la edad explica por si sola el consumo. Si los puntos aparecen
muy dispersos, la lectura es clara: la edad aporta contexto, pero no alcanza para describir
todo el comportamiento de visualizacion.
"""
)

fig3 = px.scatter(
    df,
    x="age",
    y="monthly_watch_time_mins",
    color="subscription_plan",
    size="customer_support_tickets",
    opacity=0.55,
    title="3. Multivariado: edad, consumo, soporte y plan",
)
st.plotly_chart(fig3, use_container_width=True)
st.write(
    """
Al sumar plan y tickets de soporte, el analisis se vuelve mas rico: ya no miramos solo
edad y consumo, sino perfiles. Un usuario con mucho consumo y muchos tickets puede indicar
alto uso, pero tambien mayor friccion o necesidad de asistencia.
"""
)

fig4 = px.scatter(
    df,
    x="age",
    y="monthly_watch_time_mins",
    color="favorite_genre",
    opacity=0.5,
    title="4. Multivariado adicional: edad, consumo y genero favorito",
)
st.plotly_chart(fig4, use_container_width=True)
st.write(
    """
Este grafico ayuda a ver si las preferencias de contenido cambian la lectura del consumo.
Si un genero concentra consumos altos, puede sugerir usuarios mas intensivos o contenidos
que generan mayor permanencia.
"""
)

resumen_genero = (
    df.groupby("favorite_genre")
    .agg(
        usuarios=("user_id", "count"),
        edad_mediana=("age", "median"),
        consumo_mediano=("monthly_watch_time_mins", "median"),
        consumo_promedio=("monthly_watch_time_mins", "mean"),
    )
    .sort_values("consumo_mediano", ascending=False)
    .round(2)
)

st.subheader("Resumen por genero favorito")
st.write(
    """
Esta tabla baja el grafico a numeros concretos. Sirve para comparar volumen de usuarios,
edad tipica y consumo tipico por genero.
"""
)
st.dataframe(resumen_genero, use_container_width=True)

corr = df[["age", "monthly_watch_time_mins", "customer_support_tickets"]].corr()
fig5 = px.imshow(
    corr,
    text_auto=True,
    zmin=-1,
    zmax=1,
    color_continuous_scale="RdBu_r",
    title="5. Apoyo: correlacion entre variables numericas",
)
st.plotly_chart(fig5, use_container_width=True)
st.write(
    """
La correlacion resume relaciones lineales. Es util para orientarse, pero no prueba causalidad.
Un valor bajo no significa que no haya relacion: puede haber patrones por segmento que una
correlacion general no captura.
"""
)
