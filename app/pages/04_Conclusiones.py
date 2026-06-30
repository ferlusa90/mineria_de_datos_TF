import streamlit as st

from ui import card, inject_global_styles


inject_global_styles()

st.title("Conclusiones")

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

card(
    "Cierre",
    "Despues de preparar los datos, el consumo mensual aparece como una variable central para entender perfiles. La limpieza deja una base sin nulos, sin duplicados y con categorias consistentes, lista para EDA y PCA.",
    "Sintesis",
    soft=True,
)
