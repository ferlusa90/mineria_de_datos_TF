import streamlit as st


st.title("Conclusiones")

st.subheader("Hallazgos")
st.write(
    """
La base necesitaba limpieza antes de cualquier lectura seria. Habia duplicados, categorias
inconsistentes, fechas invalidas, valores imposibles y extremos que podian empujar el analisis
hacia conclusiones equivocadas.

Despues de preparar los datos, el consumo mensual aparece como una variable central para
entender perfiles. La edad aporta contexto, pero no explica sola el comportamiento. El plan
y el genero favorito agregan una lectura mas comercial: ayudan a pensar segmentos de uso y
preferencias de contenido.
"""
)

st.subheader("Interpretacion general")
st.write(
    """
El resultado mas importante no es un numero aislado, sino el proceso. La base final queda
sin nulos, sin usuarios duplicados y con las mismas columnas originales. Eso permite analizar
con mas confianza y defender cada decision tomada durante la preparacion.
"""
)

st.subheader("Limitaciones")
st.write(
    """
El analisis es descriptivo. No se cuenta con variables como churn, fecha de alta, antiguedad,
precio pagado, satisfaccion, dispositivo o historial detallado de sesiones. Por eso no se
puede afirmar causalidad ni predecir abandono. Lo correcto es hablar de patrones observados,
no de causas definitivas.
"""
)

st.subheader("Proximos pasos")
st.write(
    """
Para profundizar el proyecto se podrian incorporar variables temporales y comerciales:
fecha de alta, cancelaciones, precio, promociones, cantidad de sesiones y satisfaccion.
Con esa informacion seria posible pasar de describir perfiles a estudiar retencion, riesgo
de baja o valor del usuario.
"""
)
