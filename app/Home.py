import streamlit as st

from ui import badges, callout, card, hero_image, inject_global_styles


st.set_page_config(
    page_title="Usuarios de Streaming | Mineria de Datos",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_global_styles()

st.sidebar.title("Navegación")
st.sidebar.markdown(
    "Explora el proyecto en el orden recomendado para seguir el flujo natural del análisis."
)
st.sidebar.markdown("**Recorrido sugerido**")
st.sidebar.write("1. Dataset")
st.sidebar.write("2. EDA")
st.sidebar.write("3. PCA")
st.sidebar.write("4. Conclusiones")
st.sidebar.markdown("**Acerca de**")
st.sidebar.caption("Proyecto Integrador - Minería de Datos 1")
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
            Una aplicación para revisar usuarios de streaming, mostrar cómo se limpió la base y resumir los principales resultados del análisis.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

badges(["Limpieza de datos", "EDA", "PCA", "Visualización", "Streamlit"])

st.write("")

hero_col, info_col = st.columns([1.15, 0.85], gap="large")
with hero_col:
    hero_image()
with info_col:
    callout(
        "Lectura del proyecto",
        "Primero reviso la calidad de la base, después limpio con reglas concretas y al final interpreto el comportamiento de los usuarios.",
        "Flujo de trabajo",
    )
    st.write("")
    st.info(
        "La app mantiene el contenido técnico, pero lo muestra en un orden más fácil de seguir."
    )

st.write("")

metric_col1, metric_col2, metric_col3 = st.columns(3)
metric_col1.metric("Etapas principales", "4")
metric_col2.metric("Variables centrales", "3")
metric_col3.metric("Enfoque", "Controlado")

st.write("")

tabs = st.tabs(["Introducción", "Análisis de Datos", "Modelado / PCA"])

with tabs[0]:
    left, right = st.columns([1.05, 0.95], gap="large")
    with left:
        card(
            "Caso de estudio",
            "Análisis de usuarios de una plataforma de streaming con variables de consumo, plan, edad, género favorito y soporte.",
            "Contexto",
            soft=True,
        )
    with right:
        card(
            "Objetivo",
            "Convertir una base con problemas reales en un dataset confiable, mostrando evidencia antes de cada limpieza y controlando el impacto después.",
            "Proceso",
            soft=True,
        )

with tabs[1]:
    c1, c2, c3 = st.columns(3, gap="large")
    with c1:
        card(
            "Análisis de Datos",
            "La app organiza el recorrido por Dataset y EDA para revisar calidad, distribuciones, comparaciones por plan y patrones de consumo.",
            "Exploración",
        )
    with c2:
        card(
            "Vista de trabajo",
            "La idea es que se vea rápido qué problema había, qué regla se aplicó y qué cambió después.",
            "Visualización",
            soft=True,
        )
    with c3:
        card(
            "Mensajes clave",
            "La información importante se destaca con cards, métricas e info boxes para que la interpretación no quede enterrada en una lista larga.",
            "Resumen",
        )

with tabs[2]:
    left, right = st.columns([1.0, 1.0], gap="large")
    with left:
        card(
            "Modelado / PCA",
            "PCA se usa para resumir las variables numéricas principales y observar cómo se distribuyen los usuarios en un espacio reducido.",
            "Reducción",
            soft=True,
        )
    with right:
        card(
            "Estado del proyecto",
            "No se presenta un modelo predictivo de machine learning; el foco está puesto en limpieza, EDA, PCA y comunicación de hallazgos.",
            "Alcance",
            soft=True,
        )

st.write("")

col_a, col_b = st.columns([1.05, 0.95], gap="large")
with col_a:
    card(
        "Resumen del proyecto",
        "La base tenía duplicados, user_id repetidos, categorías escritas de distintas formas, fechas inválidas, valores extremos y datos faltantes. El trabajo sigue una lógica simple: revisar, explicar la regla, limpiar y controlar.",
        "Visión general",
    )
with col_b:
    card(
        "Lectura sugerida",
        "Primero Dataset, luego EDA, después PCA y finalmente Conclusiones. Ese orden ayuda a no interpretar resultados antes de revisar la calidad de la base.",
        "Recorrido",
        soft=True,
    )

st.write("")

st.link_button("Repositorio GitHub", "https://github.com/ferlusa90/mineria_de_datos_TF")
st.link_button("Aplicación Streamlit", "https://mineriadedatostf-a4hvlnmrwzjjvazcprcx7q.streamlit.app/")

st.write("")

card(
    "Datos del autor",
    "Sanchez Luna Fernando Emmanuel | Comisión ITSE NODO TARDE | 28/06/2026",
    "Presentación",
    soft=True,
)
