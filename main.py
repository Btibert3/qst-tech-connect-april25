import streamlit as st
import pandas as pd

# Load data
df = pd.read_csv("bos311.csv", parse_dates=["open_dt"])

# Set wide layout
st.set_page_config(layout="wide")

# Sidebar: Select date range
st.sidebar.header("Filter by Date")
min_date = df["open_dt"].min().date()
max_date = df["open_dt"].max().date()

date_range = st.sidebar.slider(
    "Select date range:",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date),
)

# Filter data
filtered_df = df[
    (df["open_dt"].dt.date >= date_range[0]) &
    (df["open_dt"].dt.date <= date_range[1])
]

# Main content
st.title("📅 Boston 311 Requests - Simple Date Filter")
st.write(f"Showing {len(filtered_df)} requests between {date_range[0]} and {date_range[1]}")
st.dataframe(filtered_df)
