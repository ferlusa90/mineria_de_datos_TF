import streamlit as st


st.title("Conclusiones")

st.subheader("Hallazgos")
st.write(
    """
La base necesitaba limpieza antes de cualquier lectura seria. Habia duplicados, categorias
inconsistentes, fechas invalidas, valores imposibles y extremos que podian empujar el analisis
hacia conclusiones equivocadas.

Despues de preparar los datos, el consumo mensual aparece como una variable central para
entender perfiles. La edad aporta contexto, pero no explica sola el comportamiento. Cuando
sumamos plan, soporte y genero favorito, aparecen lecturas mas utiles: usuarios intensivos,
posibles puntos de friccion y preferencias de contenido.
"""
)

st.subheader("Que significa esto para el negocio")
st.write(
    """
En terminos simples: no todos los usuarios se comportan igual. Algunos consumen mucho,
otros requieren mas soporte y otros se diferencian por preferencias de contenido. Esa mirada
permite pensar mejores preguntas comerciales, por ejemplo que segmentos necesitan mas
acompanamiento o que generos concentran mayor permanencia.
"""
)

st.subheader("Limitaciones")
st.write(
    """
El analisis es descriptivo. No se cuenta con churn, antiguedad, precio pagado, satisfaccion,
dispositivos usados ni historial de sesiones. Por eso no corresponde afirmar causalidad ni
predecir abandono. El alcance es entender patrones con la informacion disponible.
"""
)

st.subheader("Proximos pasos")
st.write(
    """
Una mejora natural seria incorporar variables temporales y comerciales: fecha de alta,
cancelaciones, precio, promociones, cantidad de sesiones y satisfaccion. Con eso se podria
pasar de describir perfiles a analizar retencion, riesgo de baja o valor del usuario.
"""
)
