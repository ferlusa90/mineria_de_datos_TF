from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
df = pd.read_csv(ROOT / "data" / "processed" / "streaming_users_processed.csv")

st.title("EDA")
st.write("Análisis principal: univariado, multivariado de 2 variables y multivariado de 3 variables.")

fig1 = px.histogram(df, x="monthly_watch_time_mins", nbins=35, title="1. Univariado: distribución del tiempo mensual")
st.plotly_chart(fig1, use_container_width=True)
st.write("La mayoría de usuarios se concentra en consumos medios, con una cola derecha moderada.")

fig2 = px.scatter(df, x="age", y="monthly_watch_time_mins", opacity=0.45, title="2. Multivariado de 2 variables: edad y consumo mensual")
st.plotly_chart(fig2, use_container_width=True)
st.write("Permite evaluar si el consumo cambia con la edad. Una relación débil indica que la edad sola no explica el consumo.")

fig3 = px.scatter(df, x="age", y="monthly_watch_time_mins", color="subscription_plan", size="customer_support_tickets", opacity=0.55, title="3. Multivariado de 3 variables: edad, consumo y soporte por plan")
st.plotly_chart(fig3, use_container_width=True)
st.write("Al sumar plan y tickets se observa si los usuarios con mayor consumo también concentran mayor necesidad de soporte.")

fig4 = px.scatter(df, x="age", y="monthly_watch_time_mins", color="favorite_genre", opacity=0.5, title="4. Multivariado adicional: edad, consumo y género favorito")
st.plotly_chart(fig4, use_container_width=True)
st.write("Este cruce permite observar si los patrones de consumo por edad cambian según el género favorito.")

resumen_genero = (
    df.groupby("favorite_genre")
      .agg(
          usuarios=("user_id", "count"),
          edad_mediana=("age", "median"),
          consumo_mediano=("monthly_watch_time_mins", "median"),
          consumo_promedio=("monthly_watch_time_mins", "mean")
      )
      .sort_values("consumo_mediano", ascending=False)
      .round(2)
)
st.dataframe(resumen_genero, use_container_width=True)

corr = df[["age", "monthly_watch_time_mins", "customer_support_tickets"]].corr()
fig5 = px.imshow(corr, text_auto=True, zmin=-1, zmax=1, color_continuous_scale="RdBu_r", title="Apoyo: correlación entre variables numéricas")
st.plotly_chart(fig5, use_container_width=True)
st.write("El heatmap resume relaciones lineales entre variables numéricas; no implica causalidad.")
