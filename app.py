import streamlit as st

st.set_page_config(
    page_title="Blitz AI",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ Blitz AI")
st.subheader("AI-Powered E-Commerce Business Analytics & Sales Prediction")

st.markdown("""
### Welcome to Blitz AI 👋

Blitz AI is an intelligent e-commerce business analytics system
that helps businesses analyze sales performance, understand customers,
predict future sales, detect unusual transactions, and generate
business recommendations.
""")

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.info("""
    **📊 Business Analytics**

    Analyze revenue, profit, sales,
    products, categories and regions.
    """)

with col2:
    st.success("""
    **🤖 Artificial Intelligence**

    Sales prediction, customer segmentation
    and anomaly detection.
    """)

with col3:
    st.warning("""
    **☁️ Cloud Computing**

    Data is stored and retrieved using
    Firebase Cloud Firestore.
    """)

st.divider()

st.subheader("🚀 Blitz AI Modules")

st.write("📊 **Dashboard** — Overall business performance")
st.write("📈 **Sales Prediction** — Predict future sales")
st.write("👥 **Customer Segmentation** — Identify customer groups")
st.write("🚨 **Anomaly Detection** — Detect unusual transactions")
st.write("🤖 **AI Business Insights** — Generate business recommendations")

st.divider()

st.success("☁️ Cloud Status: Firebase Firestore Connected")

st.caption(
    "⚡ Blitz AI — AI-Powered E-Commerce Business Analytics & Sales Prediction System"
)