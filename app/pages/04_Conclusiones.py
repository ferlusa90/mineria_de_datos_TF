import streamlit as st

from ui import card, inject_global_styles


st.set_page_config(page_title="Conclusiones | Streaming Users", page_icon="✅", layout="wide")
inject_global_styles()

st.sidebar.title("Conclusiones")
st.sidebar.caption("Cierre del proyecto")
st.sidebar.markdown("**Bloques**")
st.sidebar.write("1. Hallazgos")
st.sidebar.write("2. Interpretacion")
st.sidebar.write("3. Limitaciones")
st.sidebar.write("4. Proximos pasos")

st.markdown(
    """
    <div style="padding: 0.2rem 0 0.9rem;">
        <div style="font-size: 0.85rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: #0f766e;">
            Modulo 04
        </div>
        <h1 style="margin: 0.1rem 0 0.35rem;">Conclusiones</h1>
        <p style="margin: 0; max-width: 840px; font-size: 1.02rem; line-height: 1.6; color: #5d6b78;">
            Esta pantalla cierra el recorrido resumiendo hallazgos, alcance y siguientes pasos del proyecto.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.success("La base final queda sin nulos, sin duplicados y con categorias consistentes, lista para analisis y comunicacion.")

col1, col2 = st.columns(2)
with col1:
    card(
        "Hallazgos",
        "La base necesitaba limpieza antes de cualquier lectura seria: habia duplicados exactos, user_id repetidos, categorias inconsistentes, fechas invalidas, valores imposibles y extremos.",
        "Resultado principal",
        soft=True,
    )
with col2:
    card(
        "Interpretacion general",
        "El resultado mas importante no es un numero aislado, sino el proceso: cada limpieza se apoya en evidencia previa, codigo reproducible y un control posterior.",
        "Lectura",
        soft=True,
    )

st.write("")

col3, col4 = st.columns(2)
with col3:
    card(
        "Limitaciones",
        "El analisis es descriptivo. No incluye churn, fecha de alta, antiguedad, precio, satisfaccion, dispositivo ni historial detallado; por eso no corresponde afirmar causalidad.",
        "Alcance",
    )
with col4:
    card(
        "Proximos pasos",
        "Para profundizar se podrian incorporar variables temporales y comerciales: altas, cancelaciones, precio, promociones, cantidad de sesiones y satisfaccion. Con eso seria posible estudiar retencion o riesgo de baja.",
        "Continuidad",
    )

st.write("")

left, right = st.columns([1.05, 0.95], gap="large")
with left:
    card(
        "Cierre",
        "Despues de preparar los datos, el consumo mensual aparece como una variable central para entender perfiles. La limpieza deja una base sin nulos, sin duplicados y con categorias consistentes, lista para EDA y PCA.",
        "Sintesis",
        soft=True,
    )
with right:
    st.info(
        "La conclusion metodologica es la mas importante: en mineria de datos no conviene interpretar sin antes revisar calidad, justificar transformaciones y validar el resultado."
    )
