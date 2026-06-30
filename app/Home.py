import streamlit as st

from ui import badges, callout, card, hero_image, inject_global_styles


st.set_page_config(
    page_title="Usuarios de Streaming | Mineria de Datos",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_global_styles()

st.sidebar.title("Navegacion")
st.sidebar.markdown(
    "Explora el proyecto en el orden recomendado para seguir el flujo natural del an?lisis."
)
st.sidebar.markdown("**Recorrido sugerido**")
st.sidebar.write("1. Dataset")
st.sidebar.write("2. EDA")
st.sidebar.write("3. PCA")
st.sidebar.write("4. Conclusiones")
st.sidebar.markdown("**Acerca de**")
st.sidebar.caption("Proyecto Integrador - Mineria de Datos 1")
st.sidebar.caption("Sanchez Luna Fernando Emmanuel")
st.sidebar.caption("ITSE NODO TARDE | 28/06/2026")

st.markdown(
    """
    <div style="padding: 0.35rem 0 0.9rem;">
        <div style="font-size: 0.88rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: #0f766e;">
            Proyecto Integrador
        </div>
        <h1 style="margin: 0.1rem 0 0.45rem;">Usuarios de Streaming</h1>
        <p style="margin: 0; max-width: 780px; font-size: 1.05rem; line-height: 1.6; color: #5d6b78;">
            Una aplicacion interactiva para analizar usuarios de una plataforma de streaming con foco en calidad de datos,
            exploraci?n visual, reducci?n de dimensionalidad y comunicaci?n del proceso.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

badges(["Limpieza de datos", "EDA", "PCA", "Visualizacion", "Streamlit"])

st.write("")

hero_col, info_col = st.columns([1.15, 0.85], gap="large")
with hero_col:
    hero_image()
with info_col:
    callout(
        "Lectura del proyecto",
        "Primero se diagnostica la calidad de la base, luego se limpia con reglas explicitas y al final se interpreta el comportamiento de los usuarios.",
        "Flujo de trabajo",
    )
    st.write("")
    st.info("La app mantiene el contenido tecnico original, pero reorganiza la presentacion para una lectura m?s clara y profesional.")

st.write("")

metric_col1, metric_col2, metric_col3 = st.columns(3)
metric_col1.metric("Etapas principales", "4")
metric_col2.metric("Variables centrales", "3")
metric_col3.metric("Enfoque", "Trazable")

st.write("")

tabs = st.tabs(["Introduccion", "Analisis de Datos", "Modelado / PCA"])

with tabs[0]:
    left, right = st.columns([1.05, 0.95], gap="large")
    with left:
        card(
            "Caso de estudio",
            "An?lisis de usuarios de una plataforma de streaming con variables de consumo, plan, edad, g?nero favorito y soporte.",
            "Contexto",
            soft=True,
        )
    with right:
        card(
            "Objetivo",
            "Convertir una base con problemas reales en un dataset confiable, mostrando evidencia antes de cada limpieza y controlando el impacto despu?s.",
            "Proceso",
            soft=True,
        )

with tabs[1]:
    c1, c2, c3 = st.columns(3, gap="large")
    with c1:
        card(
            "Analisis de Datos",
            "La app organiza el recorrido por Dataset y EDA para revisar calidad, distribuciones, comparaciones por plan y patrones de consumo.",
            "Exploracion",
        )
    with c2:
        card(
            "Vista de trabajo",
            "Se prioriza una lectura clara de diagn?stico, limpieza y visualizaci?n para que el proceso sea auditable y f?cil de explicar.",
            "Visualizacion",
            soft=True,
        )
    with c3:
        card(
            "Mensajes clave",
            "La informaci?n importante se destaca con cards, m?tricas e info boxes para que la interpretaci?n no quede enterrada en una lista larga.",
            "Resumen",
        )

with tabs[2]:
    left, right = st.columns([1.0, 1.0], gap="large")
    with left:
        card(
            "Modelado / PCA",
            "PCA se usa para resumir las variables num?ricas principales y observar c?mo se distribuyen los usuarios en un espacio reducido.",
            "Reduccion",
            soft=True,
        )
    with right:
        card(
            "Estado del proyecto",
            "No se presenta un modelo predictivo de machine learning; el foco est? puesto en limpieza, EDA, PCA y comunicaci?n de hallazgos.",
            "Alcance",
            soft=True,
        )

st.write("")

col_a, col_b = st.columns([1.05, 0.95], gap="large")
with col_a:
    card(
        "Resumen del proyecto",
        "La base ten?a duplicados, user_id repetidos, categor?aas escritas de distintas formas, fechas inv?lidas, valores extremos y datos faltantes. El trabajo sigue una l?gica de analista junior: diagnosticar, justificar, limpiar y validar.",
        "Vision general",
    )
with col_b:
    card(
        "Lectura sugerida",
        "Primero Dataset, luego EDA, despu?s PCA y finalmente Conclusiones. Ese orden acompa?a el flujo natural de un proyecto de miner?a de datos.",
        "Recorrido",
        soft=True,
    )

st.write("")

st.link_button("Repositorio GitHub", "https://github.com/ferlusa90/mineria_de_datos_TF")
st.link_button("Aplicacion Streamlit", "https://mineriadedatostf-a4hvlnmrwzjjvazcprcx7q.streamlit.app/")

st.write("")

card(
    "Datos del autor",
    "Sanchez Luna Fernando Emmanuel | Comisi?n ITSE NODO TARDE | 28/06/2026",
    "Presentacion",
    soft=True,
)
