from pathlib import Path

import pandas as pd
import streamlit as st


ROOT = Path(__file__).resolve().parents[2]
df = pd.read_csv(ROOT / "data" / "processed" / "streaming_users_processed.csv")
log = pd.read_csv(ROOT / "logs" / "pipeline_log.csv")

st.title("Dataset")

st.write(
    """
Esta seccion muestra la base ya preparada para el analisis. El archivo original se
conserva sin tocar en `data/raw/`, y el archivo procesado se guarda en `data/processed/`.
Esa separacion es importante: permite volver al punto de partida y auditar que se hizo.
"""
)

col1, col2, col3 = st.columns(3)
col1.metric("Filas finales", f"{len(df):,}")
col2.metric("Columnas", df.shape[1])
col3.metric("Nulos finales", int(df.isna().sum().sum()))

st.subheader("Que representa cada fila")
st.write(
    """
Cada registro representa un usuario de una plataforma de streaming. Las variables describen
su edad, plan de suscripcion, pais, genero favorito, minutos de visualizacion mensual,
ultima fecha de login y cantidad de tickets de soporte.
"""
)

st.subheader("Vista previa")
st.dataframe(df.head(50), use_container_width=True)

st.subheader("Transformaciones principales")
st.write(
    """
El siguiente log funciona como una bitacora del proceso ETL. En criollo: muestra que paso
se hizo, cuantas filas quedaron, cuantos nulos habia y que porcentaje de la base se retuvo.
"""
)
st.dataframe(log, use_container_width=True)

st.subheader("Lectura rapida de calidad")
st.write(
    """
La base final no tiene nulos ni usuarios duplicados. Ademas, conserva las mismas columnas
originales: no se agregaron variables nuevas al dataset procesado. Las variables categoricas
fueron estandarizadas para que, por ejemplo, `Premium`, `premium` y variantes similares no
se interpreten como categorias distintas.
"""
)
