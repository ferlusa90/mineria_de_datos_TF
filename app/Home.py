from pathlib import Path

import streamlit as st


st.set_page_config(page_title="Streaming Users - Mineria de Datos", layout="wide")

st.title("Usuarios de Streaming")
st.subheader("Proyecto Integrador - Mineria de Datos 1")

st.markdown(
    """
**Integrante:** Sanchez Luna Fernando Emmanuel.  

Este proyecto toma una base de usuarios de streaming y la convierte en un analisis claro y
ordenado. La base contaba con problemas muy comunes en datos reales:
duplicados, categorias escritas de distintas formas, fechas invalidas, valores extremos
y datos faltantes.

El objetivo fue trabajar la base de datos como un caso profesional: primero entender la base,
despues limpiar con criterio, luego analizar patrones y finalmente comunicar resultados.

Repositorio GitHub: https://github.com/ferlusa90/mineria_de_datos_TF

Aplicacion Streamlit: https://mineriadedatostf-a4hvlnmrwzjjvazcprcx7q.streamlit.app/
"""
)

st.info(
    "Lectura sugerida: primero Dataset, luego EDA, despues PCA y finalmente Conclusiones."
)
