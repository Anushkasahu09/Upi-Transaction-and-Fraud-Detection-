from io import BytesIO
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots


DATA_FILE = Path(__file__).with_name("UPI TRANSACTION AND FRAUD DETECTION.csv")
REQUIRED_COLUMNS = {
    "transaction id",
    "timestamp",
    "transaction type",
    "merchant_category",
    "amount (INR)",
    "transaction_status",
    "sender_age_group",
    "receiver_age_group",
    "sender_state",
    "sender_bank",
    "receiver_bank",
    "device_type",
    "network_type",
    "fraud_flag",
    "hour_of_day",
    "day_of_week",
    "is_weekend",
}


st.set_page_config(page_title="UPI Fraud Analysis", page_icon="INR", layout="wide")


@st.cache_data(show_spinner="Reading transaction data...")
def load_data(contents: bytes) -> pd.DataFrame:
    data = pd.read_csv(BytesIO(contents))
    missing_columns = REQUIRED_COLUMNS.difference(data.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing_columns))}")

    data["timestamp"] = pd.to_datetime(data["timestamp"], format="mixed", errors="coerce")
    data["amount (INR)"] = pd.to_numeric(data["amount (INR)"], errors="coerce")
    data["fraud_flag"] = pd.to_numeric(data["fraud_flag"], errors="coerce")
    data = data.dropna(subset=["timestamp", "amount (INR)", "fraud_flag"]).copy()
    data["fraud_flag"] = data["fraud_flag"].astype(int)
    data["month"] = data["timestamp"].dt.to_period("M").dt.to_timestamp()
    return data


st.title("UPI Transaction & Fraud Analysis")
st.caption("Explore transaction behavior and compare fraud rates across the available data.")

uploaded_file = st.sidebar.file_uploader("Use another CSV", type="csv")
if uploaded_file is not None:
    csv_bytes = uploaded_file.getvalue()
elif DATA_FILE.exists():
    csv_bytes = DATA_FILE.read_bytes()
else:
    st.info("Place the transaction CSV next to app.py, or upload a CSV in the sidebar.")
    st.stop()

try:
    transactions = load_data(csv_bytes)
except (ValueError, pd.errors.ParserError) as error:
    st.error(f"Could not read this dataset: {error}")
    st.stop()

if transactions.empty:
    st.error("No usable rows remain after parsing timestamps, amounts, and fraud labels.")
    st.stop()

st.sidebar.header("Filter transactions")
date_min = transactions["timestamp"].min().date()
date_max = transactions["timestamp"].max().date()
date_range = st.sidebar.date_input(
    "Transaction dates",
    value=(date_min, date_max),
    min_value=date_min,
    max_value=date_max,
)

filter_columns = [
    ("Transaction type", "transaction type"),
    ("Merchant category", "merchant_category"),
    ("Transaction status", "transaction_status"),
    ("Device", "device_type"),
    ("Network", "network_type"),
]
selections = {
    column: st.sidebar.multiselect(
        label,
        options=sorted(transactions[column].dropna().unique().tolist()),
        default=sorted(transactions[column].dropna().unique().tolist()),
    )
    for label, column in filter_columns
}

filtered = transactions
if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
    filtered = filtered[filtered["timestamp"].dt.date.between(start_date, end_date)]
for column, selected_values in selections.items():
    filtered = filtered[filtered[column].isin(selected_values)]

if filtered.empty:
    st.warning("No transactions match the selected filters.")
    st.stop()

fraud_count = int(filtered["fraud_flag"].eq(1).sum())
fraud_rate = filtered["fraud_flag"].eq(1).mean() * 100
fraud_amount = filtered.loc[filtered["fraud_flag"].eq(1), "amount (INR)"].sum()
median_amount = filtered["amount (INR)"].median()

metric_columns = st.columns(4)
metric_columns[0].metric("Transactions", f"{len(filtered):,}")
metric_columns[1].metric("Fraud records", f"{fraud_count:,}")
metric_columns[2].metric("Fraud rate", f"{fraud_rate:.3f}%")
metric_columns[3].metric("Fraud amount", f"INR {fraud_amount:,.0f}")
st.caption(f"Median transaction amount: INR {median_amount:,.0f}")

left, right = st.columns(2)
with left:
    st.subheader("Monthly transactions and fraud rate")
    monthly = filtered.groupby("month", as_index=False).agg(
        transactions=("transaction id", "count"),
        fraud_rate=("fraud_flag", lambda labels: labels.eq(1).mean() * 100),
    )
    monthly_chart = make_subplots(specs=[[{"secondary_y": True}]])
    monthly_chart.add_trace(
        go.Scatter(x=monthly["month"], y=monthly["transactions"], name="Transactions", mode="lines+markers"),
        secondary_y=False,
    )
    monthly_chart.add_trace(
        go.Scatter(x=monthly["month"], y=monthly["fraud_rate"], name="Fraud rate (%)", mode="lines+markers"),
        secondary_y=True,
    )
    monthly_chart.update_xaxes(title_text="Month")
    monthly_chart.update_yaxes(title_text="Transactions", secondary_y=False)
    monthly_chart.update_yaxes(title_text="Fraud rate (%)", secondary_y=True)
    st.plotly_chart(monthly_chart, use_container_width=True)

with right:
    st.subheader("Fraud rate by category")
    dimension = st.selectbox(
        "Compare groups",
        ["merchant_category", "transaction type", "device_type", "network_type", "sender_state"],
        format_func=lambda value: value.replace("_", " ").title(),
    )
    grouped = filtered.groupby(dimension, dropna=False).agg(
        transactions=("fraud_flag", "size"),
        fraud_records=("fraud_flag", "sum"),
        fraud_rate=("fraud_flag", lambda labels: labels.eq(1).mean() * 100),
    ).reset_index()
    grouped = grouped.sort_values("fraud_rate", ascending=False).head(15)
    category_chart = px.bar(
        grouped,
        x="fraud_rate",
        y=dimension,
        orientation="h",
        hover_data={"transactions": True, "fraud_records": True, "fraud_rate": ":.3f"},
        labels={"fraud_rate": "Fraud rate (%)", dimension: "Group"},
    )
    category_chart.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(category_chart, use_container_width=True)

st.subheader("Transaction amount by fraud label")
amount_chart = px.histogram(
    filtered,
    x="amount (INR)",
    color=filtered["fraud_flag"].map({0: "Legitimate", 1: "Fraud"}),
    nbins=50,
    barmode="overlay",
    labels={"amount (INR)": "Amount (INR)", "count": "Transactions", "color": "Label"},
    opacity=0.7,
)
st.plotly_chart(amount_chart, use_container_width=True)

with st.expander("Data quality and preview"):
    quality_columns = st.columns(3)
    quality_columns[0].metric("Rows loaded", f"{len(transactions):,}")
    quality_columns[1].metric("Rows excluded", f"{transactions.shape[0] - len(transactions):,}")
    quality_columns[2].metric("Columns", f"{len(transactions.columns) - 1}")
    st.dataframe(filtered.head(100), use_container_width=True)

st.caption(
    "Fraud is rare in this dataset. Compare rates alongside transaction counts; small groups can produce unstable rates."
)