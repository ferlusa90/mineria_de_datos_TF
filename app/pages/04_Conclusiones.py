import streamlit as st

from ui import card, inject_global_styles


st.set_page_config(page_title="Conclusiones | Streaming Users", page_icon="✅", layout="wide")
inject_global_styles()

st.sidebar.title("Conclusiones")
st.sidebar.caption("Cierre del proyecto")
st.sidebar.markdown("**Bloques**")
st.sidebar.write("1. Hallazgos")
st.sidebar.write("2. Interpretación")
st.sidebar.write("3. Limitaciones")
st.sidebar.write("4. Próximos pasos")

st.markdown(
    """
    <div style="padding: 0.2rem 0 0.9rem;">
        <div style="font-size: 0.85rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: #0f766e;">
            Módulo 04
        </div>
        <h1 style="margin: 0.1rem 0 0.35rem;">Conclusiones</h1>
        <p style="margin: 0; max-width: 840px; font-size: 1.02rem; line-height: 1.6; color: #5d6b78;">
            Esta pantalla cierra el recorrido resumiendo hallazgos, alcance y siguientes pasos del proyecto.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.success(
    "La base final queda sin nulos, sin duplicados y con categorías consistentes, lista para análisis y comunicación."
)

col1, col2 = st.columns(2)
with col1:
    card(
        "Hallazgos",
        "La base necesitaba limpieza antes de cualquier lectura seria: había duplicados exactos, user_id repetidos, categorías inconsistentes, fechas inválidas, valores imposibles y extremos.",
        "Resultado principal",
        soft=True,
    )
with col2:
    card(
        "Interpretación general",
        "El resultado más importante no es un número aislado, sino el proceso: cada limpieza se apoya en evidencia previa, código reproducible y un control posterior.",
        "Lectura",
        soft=True,
    )

st.write("")

col3, col4 = st.columns(2)
with col3:
    card(
        "Limitaciones",
        "El análisis es descriptivo. No incluye churn, fecha de alta, antigüedad, precio, satisfacción, dispositivo ni historial detallado; por eso no corresponde afirmar causalidad.",
        "Alcance",
    )
with col4:
    card(
        "Próximos pasos",
        "Para profundizar se podrían incorporar variables temporales y comerciales: altas, cancelaciones, precio, promociones, cantidad de sesiones y satisfacción. Con eso sería posible estudiar retención o riesgo de baja.",
        "Continuidad",
    )

st.write("")

left, right = st.columns([1.05, 0.95], gap="large")
with left:
    card(
        "Cierre",
        "Después de preparar los datos, el consumo mensual aparece como una variable central para entender perfiles. La limpieza deja una base sin nulos, sin duplicados y con categorías consistentes, lista para EDA y PCA.",
        "Síntesis",
        soft=True,
    )
with right:
    st.info(
        "La conclusión metodológica es la más importante: en minería de datos no conviene interpretar sin antes revisar calidad, justificar transformaciones y validar el resultado."
    )

st.markdown("### Lectura metodológica")
st.write(
    "En la imputación, el mecanismo de faltantes se interpreta mejor como MAR que como MCAR, porque se condiciona por variables observadas como plan y país. Eso hace que la decisión sea más defendible que una imputación ciega o una eliminación indiscriminada."
)
