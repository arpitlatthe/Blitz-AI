import streamlit as st
import pandas as pd
import plotly.express as px

from firestore_data import load_data_from_firestore


st.set_page_config(
    page_title="Blitz AI | Dashboard",
    page_icon="⚡",
    layout="wide"
)


@st.cache_data(ttl=60)
def get_data():
    return load_data_from_firestore()


st.title("⚡ Blitz AI — Business Dashboard")

st.caption(
    "Cloud-connected e-commerce business analytics dashboard"
)

df = get_data()

if df.empty:
    st.error("No data found in Firebase Firestore.")
    st.stop()


# -----------------------------
# Filters
# -----------------------------

st.sidebar.header("🔎 Filters")

categories = ["All"] + sorted(df["Category"].dropna().unique().tolist())

selected_category = st.sidebar.selectbox(
    "Category",
    categories
)

regions = ["All"] + sorted(df["Region"].dropna().unique().tolist())

selected_region = st.sidebar.selectbox(
    "Region",
    regions
)


filtered_df = df.copy()

if selected_category != "All":
    filtered_df = filtered_df[
        filtered_df["Category"] == selected_category
    ]

if selected_region != "All":
    filtered_df = filtered_df[
        filtered_df["Region"] == selected_region
    ]


if filtered_df.empty:
    st.warning("No data available for the selected filters.")
    st.stop()


# -----------------------------
# KPIs
# -----------------------------

revenue = filtered_df["Sales"].sum()
orders = filtered_df["Order_ID"].nunique()
customers = filtered_df["Customer"].nunique()
profit = filtered_df["Profit"].sum()
avg_order_value = revenue / orders if orders > 0 else 0


col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "💰 Revenue",
    f"₹{revenue:,.0f}"
)

col2.metric(
    "📦 Orders",
    f"{orders:,}"
)

col3.metric(
    "👥 Customers",
    f"{customers:,}"
)

col4.metric(
    "💵 Profit",
    f"₹{profit:,.0f}"
)

col5.metric(
    "🛒 Avg Order Value",
    f"₹{avg_order_value:,.0f}"
)


st.divider()


# -----------------------------
# Monthly Sales Trend
# -----------------------------

st.subheader("📈 Monthly Sales Trend")

monthly_sales = (
    filtered_df
    .set_index("Date")
    .resample("ME")["Sales"]
    .sum()
    .reset_index()
)

fig_monthly = px.line(
    monthly_sales,
    x="Date",
    y="Sales",
    markers=True,
    title="Monthly Revenue"
)

fig_monthly.update_layout(
    xaxis_title="Month",
    yaxis_title="Sales"
)

st.plotly_chart(
    fig_monthly,
    use_container_width=True
)


# -----------------------------
# Category Analysis
# -----------------------------

col1, col2 = st.columns(2)

with col1:

    st.subheader("📊 Sales by Category")

    category_sales = (
        filtered_df
        .groupby("Category")["Sales"]
        .sum()
        .reset_index()
        .sort_values("Sales", ascending=False)
    )

    fig_category = px.bar(
        category_sales,
        x="Category",
        y="Sales",
        title="Revenue by Category"
    )

    st.plotly_chart(
        fig_category,
        use_container_width=True
    )


with col2:

    st.subheader("🌍 Sales by Region")

    region_sales = (
        filtered_df
        .groupby("Region")["Sales"]
        .sum()
        .reset_index()
        .sort_values("Sales", ascending=False)
    )

    fig_region = px.bar(
        region_sales,
        x="Region",
        y="Sales",
        title="Revenue by Region"
    )

    st.plotly_chart(
        fig_region,
        use_container_width=True
    )


# -----------------------------
# Top Products
# -----------------------------

st.subheader("🏆 Top Products")

top_products = (
    filtered_df
    .groupby("Product")["Sales"]
    .sum()
    .reset_index()
    .sort_values("Sales", ascending=False)
    .head(10)
)

fig_products = px.bar(
    top_products,
    x="Sales",
    y="Product",
    orientation="h",
    title="Top 10 Products by Revenue"
)

st.plotly_chart(
    fig_products,
    use_container_width=True
)


# -----------------------------
# Profit Analysis
# -----------------------------

st.subheader("💹 Profit Analysis")

profit_data = (
    filtered_df
    .groupby("Category")[["Sales", "Profit"]]
    .sum()
    .reset_index()
)

fig_profit = px.bar(
    profit_data,
    x="Category",
    y=["Sales", "Profit"],
    barmode="group",
    title="Sales vs Profit by Category"
)

st.plotly_chart(
    fig_profit,
    use_container_width=True
)


# -----------------------------
# Dataset
# -----------------------------

st.subheader("☁️ Cloud Dataset")

st.dataframe(
    filtered_df,
    use_container_width=True
)

st.success(
    f"☁️ Blitz AI is reading {len(filtered_df):,} records from Firebase Firestore."
)