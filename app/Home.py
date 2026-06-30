import streamlit as st

from ui import badges, card, hero_image, inject_global_styles


st.set_page_config(page_title="Streaming Users - Mineria de Datos", layout="wide")
inject_global_styles()

st.title("Usuarios de Streaming")
st.subheader("Proyecto Integrador - Mineria de Datos 1")

hero_image()

badges(["Limpieza de datos", "EDA", "PCA", "Visualizacion", "Streamlit"])

st.write("")

col1, col2, col3 = st.columns(3)
with col1:
    card(
        "Caso de estudio",
        "Analisis de usuarios de una plataforma de streaming con variables de consumo, plan, edad, genero favorito y soporte.",
        "Contexto",
        soft=True,
    )
with col2:
    card(
        "Objetivo",
        "Convertir una base con problemas reales en un dataset confiable, mostrando evidencia antes de cada limpieza y controlando el impacto despues.",
        "Proceso",
        soft=True,
    )
with col3:
    card(
        "Resultado",
        "Una app interactiva que ordena el recorrido: dataset, exploracion visual, PCA y conclusiones del proyecto.",
        "Entrega",
        soft=True,
    )

st.write("")

left, right = st.columns([1.15, 0.85])
with left:
    card(
        "Resumen del proyecto",
        "La base tenia duplicados, user_id repetidos, categorias escritas de distintas formas, fechas invalidas, valores extremos y datos faltantes. El trabajo sigue una logica de analista junior: diagnosticar, justificar, limpiar y validar.",
        "Vision general",
    )
with right:
    card(
        "Lectura sugerida",
        "Primero Dataset, luego EDA, despues PCA y finalmente Conclusiones. Ese orden acompana el flujo natural de un proyecto de mineria de datos.",
        "Recorrido",
    )

st.write("")

col_a, col_b, col_c = st.columns(3)
with col_a:
    st.link_button("Repositorio GitHub", "https://github.com/ferlusa90/mineria_de_datos_TF")
with col_b:
    st.link_button(
        "Aplicacion Streamlit",
        "https://mineriadedatostf-a4hvlnmrwzjjvazcprcx7q.streamlit.app/",
    )
with col_c:
    card(
        "Datos del autor",
        "Sanchez Luna Fernando Emmanuel | Comision ITSE NODO TARDE | 28/06/2026",
        "Presentacion",
    )
