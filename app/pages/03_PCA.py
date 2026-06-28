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
st.write("Variables utilizadas:", ", ".join(variables))
st.write("Escalamiento aplicado: Z-score con `StandardScaler`.")

X_scaled = StandardScaler().fit_transform(df[variables])
pca = PCA(n_components=3, random_state=42)
pcs = pca.fit_transform(X_scaled)
varianza = pd.DataFrame({
    "componente": ["PC1", "PC2", "PC3"],
    "varianza_explicada": pca.explained_variance_ratio_,
    "varianza_acumulada": np.cumsum(pca.explained_variance_ratio_)
})

fig1 = px.bar(varianza, x="componente", y="varianza_explicada", title="Varianza explicada")
st.plotly_chart(fig1, use_container_width=True)

pc_df = pd.DataFrame(pcs[:, :2], columns=["PC1", "PC2"])
pc_df["subscription_plan"] = df["subscription_plan"]
fig2 = px.scatter(pc_df, x="PC1", y="PC2", color="subscription_plan", opacity=0.55, title="Proyección PC1-PC2 por plan")
st.plotly_chart(fig2, use_container_width=True)

st.write("Interpretación: PCA sintetiza edad, consumo y soporte en ejes comparables. La lectura depende de la varianza explicada y de las cargas de cada variable.")
