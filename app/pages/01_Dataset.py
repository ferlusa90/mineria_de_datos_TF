from pathlib import Path

import pandas as pd
import streamlit as st

from ui import callout, card, inject_global_styles


ROOT = Path(__file__).resolve().parents[2]
raw = pd.read_json(ROOT / "data" / "raw" / "streaming_users_dirty.json")
df = pd.read_csv(ROOT / "data" / "processed" / "streaming_users_processed.csv")
log = pd.read_csv(ROOT / "logs" / "pipeline_log.csv")

inject_global_styles()

st.title("Dataset")

callout(
    "Base preparada para el analisis",
    "El archivo original se conserva en data/raw/ y el procesado queda en data/processed/. La limpieza se documenta con una logica simple: primero se observa el problema, despues se aplica una regla y finalmente se controla el resultado.",
    "Trazabilidad",
)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Filas originales", f"{len(raw):,}")
col2.metric("Filas finales", f"{len(df):,}")
col3.metric("Nulos finales", int(df.isna().sum().sum()))
col4.metric("User ID repetidos", int(df.duplicated("user_id").sum()))

st.write("")

col_a, col_b = st.columns([0.9, 1.1])
with col_a:
    card(
        "Que representa cada fila",
        "Cada registro representa un usuario de una plataforma de streaming. Las variables describen edad, plan, pais, genero favorito, minutos de visualizacion, ultimo login y tickets de soporte.",
        "Unidad de analisis",
    )
with col_b:
    card(
        "Lectura rapida de calidad",
        "La base final no tiene nulos, duplicados exactos ni usuarios repetidos. Tambien mantiene las columnas originales y estandariza categorias para evitar que variantes como std, standard y estandar se lean como grupos distintos.",
        "Calidad",
        soft=True,
    )

st.subheader("Diagnostico antes de limpiar")
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

with st.expander("Codigo usado para revisar duplicados antes de limpiar"):
    st.code(
        """duplicados_exactos = raw[raw.duplicated(keep=False)]
user_id_repetidos = raw[raw.duplicated("user_id", keep=False)]

print(raw.duplicated().sum())
print(raw.duplicated("user_id").sum())
user_id_repetidos.sort_values("user_id").head(20)""",
        language="python",
    )

with st.expander("Logica usada para elegir un registro cuando un user_id estaba repetido"):
    st.code(
        """# Criterio de ranking:
# 1. fecha de login valida y no futura
# 2. consumo mensual plausible
# 3. consumo mas cercano al consumo tipico
# 4. login mas reciente
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

with st.expander("Codigo usado para tratar valores imposibles e imputar"):
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

st.subheader("Vista previa")
st.dataframe(df.head(50), use_container_width=True)

st.subheader("Transformaciones principales")
callout(
    "Bitacora del proceso ETL",
    "El log muestra la decision tomada, la evidencia que la justifica, cuantas filas quedaron, cuantos nulos habia y que porcentaje de la base se retuvo.",
    "Auditoria",
)
st.dataframe(log, use_container_width=True)
