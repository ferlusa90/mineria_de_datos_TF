import streamlit as st

st.title("Conclusiones")

st.subheader("Hallazgos")
st.write("""
La base requería limpieza antes de cualquier análisis: duplicados, categorías inconsistentes,
fechas inválidas y extremos podían distorsionar resultados. Luego de la preparación, el consumo
mensual y los tickets de soporte permiten comparar perfiles por plan y país.
""")

st.subheader("Limitaciones")
st.write("""
No se cuenta con variables como churn, antigüedad, precio pagado o satisfacción. Por eso el análisis
describe patrones, pero no permite afirmar causas comerciales completas.
""")

st.subheader("Próximos pasos")
st.write("""
Incorporar métricas temporales, variables de retención y validación de reglas de negocio para ampliar
el análisis y fortalecer las conclusiones.
""")
