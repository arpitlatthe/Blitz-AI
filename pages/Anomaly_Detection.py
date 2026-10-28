import streamlit as st
import pandas as pd
import plotly.express as px

from sklearn.ensemble import IsolationForest

from firestore_data import load_data_from_firestore


st.set_page_config(
    page_title="Blitz AI | Anomaly Detection",
    page_icon="⚡",
    layout="wide"
)


@st.cache_data(ttl=60)
def get_data():
    return load_data_from_firestore()


st.title("⚡ Blitz AI — Anomaly Detection")

st.caption(
    "AI-powered detection of unusual e-commerce transactions"
)

df = get_data()

if df.empty:
    st.error("No data found in Firebase Firestore.")
    st.stop()


# -----------------------------
# Features
# -----------------------------

features = [
    "Quantity",
    "Sales",
    "Cost",
    "Profit"
]


# -----------------------------
# Isolation Forest
# -----------------------------

model = IsolationForest(
    n_estimators=200,
    contamination=0.05,
    random_state=42
)

df["Anomaly"] = model.fit_predict(
    df[features]
)

df["Anomaly_Status"] = df["Anomaly"].map({
    1: "Normal",
    -1: "Anomaly"
})


# -----------------------------
# KPIs
# -----------------------------

total_transactions = len(df)

anomalies = (
    df["Anomaly_Status"] == "Anomaly"
).sum()

normal_transactions = (
    df["Anomaly_Status"] == "Normal"
).sum()

anomaly_rate = (
    anomalies / total_transactions
) * 100


col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "📦 Transactions",
    f"{total_transactions:,}"
)

col2.metric(
    "🚨 Anomalies",
    f"{anomalies:,}"
)

col3.metric(
    "✅ Normal",
    f"{normal_transactions:,}"
)

col4.metric(
    "⚠️ Anomaly Rate",
    f"{anomaly_rate:.2f}%"
)


st.divider()


# -----------------------------
# Scatter Plot
# -----------------------------

st.subheader("🔎 Sales vs Profit")

fig = px.scatter(
    df,
    x="Sales",
    y="Profit",
    size="Quantity",
    color="Anomaly_Status",
    hover_data=[
        "Order_ID",
        "Customer",
        "Product",
        "Category",
        "Region"
    ],
    title="Normal vs Anomalous Transactions"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# -----------------------------
# Distribution
# -----------------------------

st.subheader("📊 Sales Distribution")

fig_hist = px.histogram(
    df,
    x="Sales",
    color="Anomaly_Status",
    nbins=30,
    title="Sales Distribution"
)

st.plotly_chart(
    fig_hist,
    use_container_width=True
)


# -----------------------------
# Anomaly Table
# -----------------------------

st.subheader("🚨 Detected Anomalies")

anomaly_df = df[
    df["Anomaly_Status"] == "Anomaly"
].copy()

st.dataframe(
    anomaly_df.sort_values(
        "Sales",
        ascending=False
    ),
    use_container_width=True
)


# -----------------------------
# Business Interpretation
# -----------------------------

st.subheader("💡 Business Interpretation")

st.info("""
Blitz AI uses the **Isolation Forest machine learning algorithm**
to identify transactions that significantly differ from normal
transaction patterns.

Potential reasons for anomalies may include:

- unusually high order quantities
- unusually high sales
- unusual profit values
- abnormal transaction combinations
- possible data-entry issues
""")

st.success(
    "☁️ Transaction data is loaded from Firebase Firestore."
)