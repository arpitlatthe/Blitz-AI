import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

from firestore_data import load_data_from_firestore


st.set_page_config(
    page_title="Blitz AI | Sales Prediction",
    page_icon="⚡",
    layout="wide"
)


@st.cache_data(ttl=60)
def get_data():
    return load_data_from_firestore()


st.title("⚡ Blitz AI — AI Sales Prediction")

st.caption(
    "Machine Learning powered future sales forecasting"
)

df = get_data()

if df.empty:
    st.error("No data found in Firebase Firestore.")
    st.stop()


# -----------------------------
# Prepare Data
# -----------------------------

daily_sales = (
    df.groupby("Date")["Sales"]
    .sum()
    .reset_index()
    .sort_values("Date")
)

daily_sales["Day_Number"] = range(
    len(daily_sales)
)


# -----------------------------
# Train Model
# -----------------------------

X = daily_sales[["Day_Number"]]

y = daily_sales["Sales"]

model = LinearRegression()

model.fit(X, y)

predictions = model.predict(X)

mae = mean_absolute_error(
    y,
    predictions
)

r2 = r2_score(
    y,
    predictions
)


# -----------------------------
# Forecast Settings
# -----------------------------

st.sidebar.header("🔮 Forecast Settings")

forecast_days = st.sidebar.slider(
    "Forecast Days",
    min_value=7,
    max_value=60,
    value=30
)


# -----------------------------
# Future Forecast
# -----------------------------

last_day_number = daily_sales["Day_Number"].max()

future_days = range(
    last_day_number + 1,
    last_day_number + forecast_days + 1
)

future_predictions = model.predict(
    pd.DataFrame({
        "Day_Number": list(future_days)
    })
)

last_date = daily_sales["Date"].max()

future_dates = pd.date_range(
    start=last_date + pd.Timedelta(days=1),
    periods=forecast_days
)


forecast_df = pd.DataFrame({
    "Date": future_dates,
    "Predicted_Sales": future_predictions
})


# -----------------------------
# KPIs
# -----------------------------

predicted_total = forecast_df["Predicted_Sales"].sum()

average_prediction = forecast_df[
    "Predicted_Sales"
].mean()

historical_average = daily_sales[
    "Sales"
].mean()

change_percentage = (
    (average_prediction - historical_average)
    / historical_average
) * 100


col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "🔮 Forecast Period",
    f"{forecast_days} Days"
)

col2.metric(
    "💰 Predicted Sales",
    f"₹{predicted_total:,.0f}"
)

col3.metric(
    "📊 Avg Daily Prediction",
    f"₹{average_prediction:,.0f}"
)

col4.metric(
    "📈 Expected Change",
    f"{change_percentage:.2f}%"
)


st.divider()


# -----------------------------
# Forecast Chart
# -----------------------------

st.subheader("📈 Historical vs Predicted Sales")

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=daily_sales["Date"],
        y=daily_sales["Sales"],
        mode="lines",
        name="Historical Sales"
    )
)

fig.add_trace(
    go.Scatter(
        x=forecast_df["Date"],
        y=forecast_df["Predicted_Sales"],
        mode="lines",
        name="Predicted Sales"
    )
)

fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Sales",
    hovermode="x unified"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# -----------------------------
# Forecast Table
# -----------------------------

st.subheader("🔮 Sales Forecast")

display_forecast = forecast_df.copy()

display_forecast["Predicted_Sales"] = (
    display_forecast["Predicted_Sales"]
    .round(2)
)

st.dataframe(
    display_forecast,
    use_container_width=True
)


# -----------------------------
# Model Performance
# -----------------------------

st.subheader("🤖 Model Performance")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Mean Absolute Error",
        f"₹{mae:,.2f}"
    )

with col2:
    st.metric(
        "R² Score",
        f"{r2:.3f}"
    )


st.info("""
### How Blitz AI predicts sales

Blitz AI uses **Linear Regression** to learn the relationship
between time and historical daily sales.

The trained model is then used to estimate future sales
for the selected number of days.
""")

st.success(
    "☁️ Sales data is loaded from Firebase Firestore."
)