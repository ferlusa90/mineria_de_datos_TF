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
st.sidebar.caption("Diagnóstico y limpieza")
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
            Acá muestro cómo venía la base original, qué problemas tenía y cómo quedó después de limpiarla.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

top_a, top_b = st.columns([1.05, 0.95], gap="large")
with top_a:
    callout(
        "Base preparada para el análisis",
        "El archivo original queda guardado en data/raw/ y la versión limpia queda en data/processed/. La lógica fue simple: primero mirar el problema, después aplicar una regla y al final revisar si el resultado quedó bien.",
        "Control",
    )
with top_b:
    card(
        "Lectura rápida",
        "Esta pantalla resume la calidad inicial, las reglas de limpieza y el impacto que fue quedando guardado en el log.",
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
        "La base final no tiene nulos, duplicados exactos ni usuarios repetidos. También mantiene las columnas originales y une categorías que eran lo mismo, por ejemplo std, standard y estandar.",
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
        "Este diagnóstico muestra cómo estaba la base antes de tocarla. Lo uso como punto de comparación para ver qué cambió con la limpieza."
    )

st.markdown("### Criterios usados en la limpieza")
left, right = st.columns(2, gap="large")
with left:
    card(
        "Duplicados exactos",
        "Los eliminé porque eran la misma fila repetida. Si los dejaba, algunos conteos iban a quedar inflados sin agregar información real.",
        "Regla 1",
        soft=True,
    )
with right:
    card(
        "user_id repetidos",
        "No los imputé porque un identificador no es un dato faltante, es una clave. Usé un ranking de calidad para quedarme con una sola fila por usuario. Dicho simple: preferí conservar la versión más confiable antes que inventar o duplicar información.",
        "Regla 2",
        soft=True,
    )

st.markdown("### ¿Fue significativo?")
sig1, sig2, sig3 = st.columns(3)
sig1.metric("Nulos iniciales", "753")
sig2.metric("Duplicados exactos", "126")
sig3.metric("user_id repetidos", "160")
st.caption(
    "Los nulos representaban 1.15% de las celdas; los duplicados exactos 1.54% de las filas; y los user_id repetidos 1.96% de la base. No era un volumen enorme, pero alcanzaba para mover conteos y perfiles."
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

st.markdown("### Mecanismo de faltantes")
st.info(
    "Para los faltantes no asumí que todo faltaba por azar puro. Los traté como un caso más cercano a MAR, usando variables observadas como plan y país para imputar con más criterio."
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
    "El log deja anotado qué decisión se tomó, qué evidencia había antes y cómo fue cambiando la base después de cada paso.",
    "Registro",
)
st.dataframe(log, use_container_width=True)
