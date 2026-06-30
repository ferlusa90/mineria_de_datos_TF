from pathlib import Path

import pandas as pd
import streamlit as st

from ui import callout, card, inject_global_styles


ROOT = Path(__file__).resolve().parents[2]
raw = pd.read_json(ROOT / "data" / "raw" / "streaming_users_dirty.json")
df = pd.read_csv(ROOT / "data" / "processed" / "streaming_users_processed.csv")
log = pd.read_csv(ROOT / "logs" / "pipeline_log.csv")

st.set_page_config(page_title="Dataset | Streaming Users", page_icon="🧾", layout="wide")
inject_global_styles()

st.sidebar.title("Dataset")
st.sidebar.caption("Diagnóstico, limpieza y trazabilidad")
st.sidebar.markdown("**Secciones**")
st.sidebar.write("1. Resumen")
st.sidebar.write("2. Diagnóstico")
st.sidebar.write("3. Código")
st.sidebar.write("4. Log ETL")

st.markdown(
    """
    <div style="padding: 0.2rem 0 0.8rem;">
        <div style="font-size: 0.85rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: #0f766e;">
            Módulo 01
        </div>
        <h1 style="margin: 0.1rem 0 0.35rem;">Dataset</h1>
        <p style="margin: 0; max-width: 840px; font-size: 1.02rem; line-height: 1.6; color: #5d6b78;">
            Aquí se documenta la base original, el diagnóstico previo y el resultado final de la limpieza con total trazabilidad.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

top_a, top_b = st.columns([1.05, 0.95], gap="large")
with top_a:
    callout(
        "Base preparada para el análisis",
        "El archivo original se conserva en data/raw/ y el procesado queda en data/processed/. La limpieza se documenta con una lógica simple: primero se observa el problema, después se aplica una regla y finalmente se controla el resultado.",
        "Trazabilidad",
    )
with top_b:
    card(
        "Lectura rápida",
        "Esta pantalla resume la calidad inicial, la estrategia de limpieza y la evidencia guardada en el log del pipeline.",
        "Resumen",
        soft=True,
    )

col1, col2, col3, col4 = st.columns(4)
col1.metric("Filas originales", f"{len(raw):,}")
col2.metric("Filas finales", f"{len(df):,}")
col3.metric("Nulos finales", int(df.isna().sum().sum()))
col4.metric("User ID repetidos", int(df.duplicated("user_id").sum()))

st.write("")

col_a, col_b = st.columns([0.9, 1.1])
with col_a:
    callout(
        "Qué representa cada fila",
        "Cada registro representa un usuario de una plataforma de streaming. Las variables describen edad, plan, país, género favorito, minutos de visualización, último login y tickets de soporte.",
        "Unidad de análisis",
    )
with col_b:
    card(
        "Lectura rápida de calidad",
        "La base final no tiene nulos, duplicados exactos ni usuarios repetidos. También mantiene las columnas originales y estandariza categorías para evitar que variantes como std, standard y estandar se lean como grupos distintos.",
        "Calidad",
        soft=True,
    )

st.markdown("### Diagnóstico antes de limpiar")
diag_col1, diag_col2 = st.columns([0.82, 1.18], gap="large")
with diag_col1:
    diagnostico = pd.DataFrame(
        {
            "filas": [raw.shape[0]],
            "columnas": [raw.shape[1]],
            "nulos_totales": [int(raw.isna().sum().sum())],
            "duplicados_exactos": [int(raw.duplicated().sum())],
            "user_id_repetidos": [int(raw.duplicated("user_id").sum())],
        }
    )
    st.dataframe(diagnostico, use_container_width=True, hide_index=True)
with diag_col2:
    st.info(
        "El diagnóstico resume el estado original de la base antes de cualquier transformación. Sirve como punto de comparación para medir el impacto de la limpieza."
    )

st.markdown("### Código y decisiones")
code_col1, code_col2 = st.columns(2, gap="large")
with code_col1:
    with st.expander("Código usado para revisar duplicados antes de limpiar"):
        st.code(
            """duplicados_exactos = raw[raw.duplicated(keep=False)]
user_id_repetidos = raw[raw.duplicated("user_id", keep=False)]

print(raw.duplicated().sum())
print(raw.duplicated("user_id").sum())
user_id_repetidos.sort_values("user_id").head(20)""",
            language="python",
        )

with code_col2:
    with st.expander("Lógica usada para elegir un registro cuando un user_id estaba repetido"):
        st.code(
            """# Criterio de ranking:
# 1. fecha de login válida y no futura
# 2. consumo mensual plausible
# 3. consumo más cercano al consumo típico
# 4. login más reciente
# 5. mayor completitud

orden = ordenar_usuarios_repetidos(df)
df = (
    df.loc[orden]
    .drop_duplicates(subset="user_id", keep="first")
    .sort_values("user_id")
    .reset_index(drop=True)
)""",
            language="python",
        )

with st.expander("Código usado para tratar valores imposibles e imputar"):
    st.code(
        """df.loc[(df["age"] < 13) | (df["age"] > 100), "age"] = np.nan
df.loc[df["monthly_watch_time_mins"] < 0, "monthly_watch_time_mins"] = np.nan
df.loc[df["customer_support_tickets"] < 0, "customer_support_tickets"] = np.nan

for col in ["age", "monthly_watch_time_mins"]:
    df[col] = df.groupby(["subscription_plan", "country"])[col].transform(
        lambda s: s.fillna(s.median())
    )
    df[col] = df[col].fillna(df[col].median())""",
        language="python",
    )

st.markdown("### Vista previa")
st.dataframe(df.head(50), use_container_width=True)

st.markdown("### Transformaciones principales")
callout(
    "Bitácora del proceso ETL",
    "El log muestra la decisión tomada, la evidencia que la justifica, cuántas filas quedaron, cuántos nulos había y qué porcentaje de la base se retuvo.",
    "Auditoría",
)
st.dataframe(log, use_container_width=True)
