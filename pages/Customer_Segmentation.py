import streamlit as st
import pandas as pd
import plotly.express as px

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

from firestore_data import load_data_from_firestore


st.set_page_config(
    page_title="Blitz AI | Customer Segmentation",
    page_icon="⚡",
    layout="wide"
)


@st.cache_data(ttl=60)
def get_data():
    return load_data_from_firestore()


st.title("⚡ Blitz AI — Customer Segmentation")

st.caption(
    "AI-powered customer behavior analysis using RFM and K-Means"
)

df = get_data()

if df.empty:
    st.error("No data found in Firebase Firestore.")
    st.stop()


# -----------------------------
# RFM Analysis
# -----------------------------

reference_date = df["Date"].max() + pd.Timedelta(days=1)

rfm = df.groupby("Customer").agg({

    "Date": lambda x: (
        reference_date - x.max()
    ).days,

    "Order_ID": "count",

    "Sales": "sum"

}).reset_index()


rfm.columns = [
    "Customer",
    "Recency",
    "Frequency",
    "Monetary"
]


# -----------------------------
# Standardization
# -----------------------------

features = [
    "Recency",
    "Frequency",
    "Monetary"
]

scaler = StandardScaler()

scaled_data = scaler.fit_transform(
    rfm[features]
)


# -----------------------------
# K-Means
# -----------------------------

kmeans = KMeans(
    n_clusters=4,
    random_state=42,
    n_init=10
)

rfm["Cluster"] = kmeans.fit_predict(
    scaled_data
)


# -----------------------------
# Segment Mapping
# -----------------------------

cluster_summary = (
    rfm.groupby("Cluster")[features]
    .mean()
)

cluster_summary["Score"] = (
    -cluster_summary["Recency"]
    + cluster_summary["Frequency"]
    + cluster_summary["Monetary"] / 10000
)

sorted_clusters = (
    cluster_summary["Score"]
    .sort_values(ascending=False)
    .index
    .tolist()
)


segment_names = {}

names = [
    "🏆 VIP Customers",
    "⭐ Loyal Customers",
    "🟡 Potential Customers",
    "🔵 At-Risk Customers"
]

for i, cluster in enumerate(sorted_clusters):

    segment_names[cluster] = names[i]


rfm["Segment"] = rfm["Cluster"].map(
    segment_names
)


# -----------------------------
# KPIs
# -----------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "👥 Customers",
    f"{len(rfm):,}"
)

col2.metric(
    "🏆 VIP",
    f"{(rfm['Segment'] == '🏆 VIP Customers').sum():,}"
)

col3.metric(
    "⭐ Loyal",
    f"{(rfm['Segment'] == '⭐ Loyal Customers').sum():,}"
)

col4.metric(
    "🔵 At-Risk",
    f"{(rfm['Segment'] == '🔵 At-Risk Customers').sum():,}"
)


st.divider()


# -----------------------------
# Segment Distribution
# -----------------------------

col1, col2 = st.columns(2)

with col1:

    st.subheader("👥 Customer Segment Distribution")

    segment_counts = (
        rfm["Segment"]
        .value_counts()
        .reset_index()
    )

    segment_counts.columns = [
        "Segment",
        "Customers"
    ]

    fig = px.pie(
        segment_counts,
        names="Segment",
        values="Customers",
        title="Customer Segments"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


with col2:

    st.subheader("💰 Customer Value")

    fig = px.scatter(
        rfm,
        x="Frequency",
        y="Monetary",
        size="Monetary",
        color="Segment",
        hover_name="Customer",
        title="Customer Frequency vs Monetary Value"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# -----------------------------
# Customer Table
# -----------------------------

st.subheader("📋 Customer Segments")

display_rfm = rfm.copy()

display_rfm["Monetary"] = (
    display_rfm["Monetary"]
    .round(2)
)

st.dataframe(
    display_rfm.sort_values(
        "Monetary",
        ascending=False
    ),
    use_container_width=True
)


# -----------------------------
# Recommendations
# -----------------------------

st.subheader("💡 Business Recommendations")

st.info("""
**🏆 VIP Customers**

Provide premium offers, loyalty rewards and personalized services.
""")

st.success("""
**⭐ Loyal Customers**

Use loyalty programs and repeat-purchase discounts.
""")

st.warning("""
**🟡 Potential Customers**

Use targeted promotions to increase purchase frequency.
""")

st.error("""
**🔵 At-Risk Customers**

Send re-engagement campaigns, special offers and reminders.
""")


st.success(
    "☁️ Customer data is loaded from Firebase Firestore."
)