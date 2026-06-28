from pathlib import Path
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
df = pd.read_csv(ROOT / "data" / "processed" / "streaming_users_processed.csv")
log = pd.read_csv(ROOT / "logs" / "pipeline_log.csv")

st.title("Dataset")
st.write("Base procesada de usuarios de streaming. El archivo original se preserva sin modificaciones en `data/raw/`.")

col1, col2, col3 = st.columns(3)
col1.metric("Filas", f"{len(df):,}")
col2.metric("Columnas", df.shape[1])
col3.metric("Nulos finales", int(df.isna().sum().sum()))

st.subheader("Vista previa")
st.dataframe(df.head(50), use_container_width=True)

st.subheader("Transformaciones principales")
st.dataframe(log, use_container_width=True)
