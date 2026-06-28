from pathlib import Path

import streamlit as st


st.set_page_config(page_title="Streaming Users - Mineria de Datos", layout="wide")

st.title("Usuarios de Streaming")
st.subheader("Proyecto Integrador - Mineria de Datos 1")

st.markdown(
    """
**Integrantes:** completar con los nombres del grupo.  
**Comision:** completar.  
**Fecha:** junio de 2026.

Este proyecto toma una base de usuarios de streaming y la convierte en un analisis claro,
ordenado y defendible. La base venia con problemas muy comunes en datos reales:
duplicados, categorias escritas de distintas formas, fechas invalidas, valores extremos
y datos faltantes.

El objetivo fue trabajar como se haria en un caso profesional: primero entender la base,
despues limpiar con criterio, luego analizar patrones y finalmente comunicar resultados
sin exagerar lo que los datos permiten concluir.

Repositorio GitHub: https://github.com/ferlusa90/mineria_de_datos_TF
"""
)

st.info(
    "Lectura sugerida: primero Dataset, luego EDA, despues PCA y finalmente Conclusiones."
)
