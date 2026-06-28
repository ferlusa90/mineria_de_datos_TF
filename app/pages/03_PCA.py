from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


ROOT = Path(__file__).resolve().parents[2]
df = pd.read_csv(ROOT / "data" / "processed" / "streaming_users_processed.csv")
variables = ["age", "monthly_watch_time_mins", "customer_support_tickets"]

st.title("PCA")

st.write(
    """
PCA es una tecnica para resumir variables numericas en nuevas dimensiones llamadas
componentes principales. Dicho simple: intenta condensar informacion sin mirar cada
variable por separado.
"""
)

st.subheader("Variables usadas")
st.write(", ".join(variables))

st.subheader("Por que se escalo")
st.write(
    """
Las variables tienen unidades distintas: edad esta en anios, consumo en minutos y soporte
en cantidad de tickets. Si no se escalan, los minutos podrian dominar el analisis solo por
tener numeros mas grandes. Por eso se aplico Z-score con `StandardScaler`.
"""
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

fig1 = px.bar(
    varianza,
    x="componente",
    y="varianza_explicada",
    title="Varianza explicada por componente",
)
st.plotly_chart(fig1, use_container_width=True)

st.write(
    """
La varianza explicada indica cuanta informacion resume cada componente. Si una componente
explica poco, no conviene venderla como gran hallazgo: se interpreta con prudencia.
"""
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
)
st.plotly_chart(fig2, use_container_width=True)

st.write(
    """
La proyeccion permite observar si los planes tienden a agruparse en el espacio numerico.
Si los colores se mezclan mucho, significa que edad, consumo y soporte no separan de forma
contundente los planes. Eso tambien es una conclusion valida.
"""
)
