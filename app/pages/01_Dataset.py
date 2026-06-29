from pathlib import Path

import pandas as pd
import streamlit as st

from ui import callout, card, inject_global_styles


ROOT = Path(__file__).resolve().parents[2]
df = pd.read_csv(ROOT / "data" / "processed" / "streaming_users_processed.csv")
log = pd.read_csv(ROOT / "logs" / "pipeline_log.csv")

inject_global_styles()

st.title("Dataset")

callout(
    "Base preparada para el analisis",
    "El archivo original se conserva en data/raw/ y el procesado queda en data/processed/. Esa separacion permite volver al punto de partida y auditar cada decision de limpieza.",
    "Trazabilidad",
)

col1, col2, col3 = st.columns(3)
col1.metric("Filas finales", f"{len(df):,}")
col2.metric("Columnas", df.shape[1])
col3.metric("Nulos finales", int(df.isna().sum().sum()))

st.write("")

col_a, col_b = st.columns([0.9, 1.1])
with col_a:
    card(
        "Que representa cada fila",
        "Cada registro representa un usuario de una plataforma de streaming. Las variables describen edad, plan, pais, genero favorito, minutos de visualizacion, ultimo login y tickets de soporte.",
        "Unidad de analisis",
    )
with col_b:
    card(
        "Lectura rapida de calidad",
        "La base final no tiene nulos ni usuarios duplicados. Tambien mantiene las columnas originales y estandariza categorias para evitar que variantes como Premium y premium se lean como grupos distintos.",
        "Calidad",
        soft=True,
    )

st.subheader("Vista previa")
st.dataframe(df.head(50), use_container_width=True)

st.subheader("Transformaciones principales")
callout(
    "Bitacora del proceso ETL",
    "El log muestra que paso se hizo, cuantas filas quedaron, cuantos nulos habia y que porcentaje de la base se retuvo.",
    "Auditoria",
)
st.dataframe(log, use_container_width=True)
