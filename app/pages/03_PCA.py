from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

from ui import callout, card, inject_global_styles


ROOT = Path(__file__).resolve().parents[2]
df = pd.read_csv(ROOT / "data" / "processed" / "streaming_users_processed.csv")
variables = ["age", "monthly_watch_time_mins", "customer_support_tickets"]
PALETTE = ["#0f766e", "#e56b55", "#2f5d7c", "#b5812a", "#6d5a8d", "#4f7f52"]

inject_global_styles()

st.title("PCA")

left, right = st.columns([0.95, 1.05])
with left:
    card(
        "Variables usadas",
        ", ".join(variables),
        "Entrada del modelo",
        soft=True,
    )
with right:
    callout(
        "Por que se escalo",
        "Las variables tienen unidades distintas: edad en anos, consumo en minutos y soporte en tickets. Con Z-score se evita que los minutos dominen solo por tener numeros mas grandes.",
        "Preparacion",
    )

X_scaled = StandardScaler().fit_transform(df[variables])
pca = PCA(n_components=3, random_state=42)
pcs = pca.fit_transform(X_scaled)
varianza = pd.DataFrame(
    {
        "componente": ["PC1", "PC2", "PC3"],
        "varianza_explicada": pca.explained_variance_ratio_,
        "varianza_acumulada": np.cumsum(pca.explained_variance_ratio_),
    }
)

st.write("")
col1, col2, col3 = st.columns(3)
for col, row in zip([col1, col2, col3], varianza.itertuples(index=False)):
    col.metric(row.componente, f"{row.varianza_explicada:.1%}", f"Acum. {row.varianza_acumulada:.1%}")

fig1 = px.bar(
    varianza,
    x="componente",
    y="varianza_explicada",
    title="Varianza explicada por componente",
    color="componente",
    color_discrete_sequence=PALETTE,
)
fig1.update_layout(template="plotly_white", showlegend=False, yaxis_tickformat=".0%")
with st.container(border=True):
    st.plotly_chart(fig1, use_container_width=True)
    st.caption(
        "La varianza explicada indica cuanta informacion resume cada componente. Si una componente explica poco, se interpreta con prudencia."
    )

pc_df = pd.DataFrame(pcs[:, :2], columns=["PC1", "PC2"])
pc_df["subscription_plan"] = df["subscription_plan"]

fig2 = px.scatter(
    pc_df,
    x="PC1",
    y="PC2",
    color="subscription_plan",
    opacity=0.55,
    title="Proyeccion PC1-PC2 por plan",
    color_discrete_sequence=PALETTE,
)
fig2.update_layout(template="plotly_white")
with st.container(border=True):
    st.plotly_chart(fig2, use_container_width=True)
    st.caption(
        "La proyeccion permite observar si los planes tienden a agruparse en el espacio numerico. Si los colores se mezclan, edad, consumo y soporte no separan de forma contundente los planes."
    )
