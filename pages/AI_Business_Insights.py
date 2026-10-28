import streamlit as st
import pandas as pd
import plotly.express as px

from firestore_data import load_data_from_firestore


st.set_page_config(
    page_title="Blitz AI | Business Insights",
    page_icon="⚡",
    layout="wide"
)


@st.cache_data(ttl=60)
def get_data():
    return load_data_from_firestore()


st.title("⚡ Blitz AI — AI Business Insights")

st.caption(
    "Automated business intelligence and decision support"
)

df = get_data()

if df.empty:
    st.error("No data found in Firebase Firestore.")
    st.stop()


# -----------------------------
# Overall Metrics
# -----------------------------

total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
total_orders = df["Order_ID"].nunique()
total_customers = df["Customer"].nunique()

average_order_value = (
    total_sales / total_orders
    if total_orders > 0
    else 0
)

profit_margin = (
    total_profit / total_sales * 100
    if total_sales > 0
    else 0
)


col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "💰 Revenue",
    f"₹{total_sales:,.0f}"
)

col2.metric(
    "💵 Profit",
    f"₹{total_profit:,.0f}"
)

col3.metric(
    "📦 Orders",
    f"{total_orders:,}"
)

col4.metric(
    "👥 Customers",
    f"{total_customers:,}"
)

col5.metric(
    "📈 Profit Margin",
    f"{profit_margin:.2f}%"
)


st.divider()


# -----------------------------
# Business Leaders
# -----------------------------

best_product = (
    df.groupby("Product")["Sales"]
    .sum()
    .idxmax()
)

best_category = (
    df.groupby("Category")["Sales"]
    .sum()
    .idxmax()
)

best_region = (
    df.groupby("Region")["Sales"]
    .sum()
    .idxmax()
)

most_profitable_product = (
    df.groupby("Product")["Profit"]
    .sum()
    .idxmax()
)

top_customer = (
    df.groupby("Customer")["Sales"]
    .sum()
    .idxmax()
)


col1, col2, col3 = st.columns(3)

with col1:
    st.success(
        f"🏆 **Top Product:** {best_product}"
    )

with col2:
    st.info(
        f"📊 **Top Category:** {best_category}"
    )

with col3:
    st.warning(
        f"🌍 **Top Region:** {best_region}"
    )


st.divider()


col1, col2 = st.columns(2)

with col1:

    st.subheader("💰 Most Profitable Product")

    st.metric(
        "Product",
        most_profitable_product
    )


with col2:

    st.subheader("👑 Top Customer")

    st.metric(
        "Customer",
        top_customer
    )


# -----------------------------
# Category Analysis
# -----------------------------

st.subheader("📊 Category Performance")

category_data = (
    df.groupby("Category")[["Sales", "Profit"]]
    .sum()
    .reset_index()
)

fig_category = px.bar(
    category_data,
    x="Category",
    y=["Sales", "Profit"],
    barmode="group",
    title="Sales and Profit by Category"
)

st.plotly_chart(
    fig_category,
    use_container_width=True
)


# -----------------------------
# Region Analysis
# -----------------------------

st.subheader("🌍 Regional Performance")

region_data = (
    df.groupby("Region")[["Sales", "Profit"]]
    .sum()
    .reset_index()
)

fig_region = px.bar(
    region_data,
    x="Region",
    y=["Sales", "Profit"],
    barmode="group",
    title="Sales and Profit by Region"
)

st.plotly_chart(
    fig_region,
    use_container_width=True
)


# -----------------------------
# Business Recommendations
# -----------------------------

st.subheader("🤖 AI-Generated Business Recommendations")

st.success(
    f"🏆 Focus marketing efforts on the best-performing product: **{best_product}**."
)

st.info(
    f"📊 The **{best_category}** category generates the highest revenue."
)

st.warning(
    f"🌍 Consider expanding business activity in the **{best_region}** region."
)

st.success(
    f"💰 Promote **{most_profitable_product}** because it generates strong profit."
)

if profit_margin >= 20:
    st.success(
        f"💚 Profit margin is healthy at **{profit_margin:.2f}%**."
    )
elif profit_margin >= 10:
    st.warning(
        f"🟡 Profit margin is moderate at **{profit_margin:.2f}%**."
    )
else:
    st.error(
        f"🔴 Profit margin is low at **{profit_margin:.2f}%**."
    )


st.divider()

st.success(
    "☁️ Business data is loaded from Firebase Firestore."
)