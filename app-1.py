import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv("bos311.csv", parse_dates=["open_dt", "closed_dt"])

# Streamlit config
st.set_page_config(page_title='Boston 311 Dashboard', layout='wide', page_icon='📍')

# Sidebar filters
st.sidebar.header("Filter Requests")
date_range = st.sidebar.date_input("Open Date Range", [df.open_dt.min(), df.open_dt.max()])
status_options = st.sidebar.multiselect("Case Status", df['case_status'].unique(), default=list(df['case_status'].unique()))
neighborhood_options = st.sidebar.multiselect("Neighborhood", df['neighborhood'].dropna().unique(), default=list(df['neighborhood'].dropna().unique()))
reason_options = st.sidebar.multiselect("Reason", df['reason'].unique(), default=list(df['reason'].unique()))

# Apply filters
filtered = df[
    (df['open_dt'].dt.date >= date_range[0]) &
    (df['open_dt'].dt.date <= date_range[1]) &
    (df['case_status'].isin(status_options)) &
    (df['neighborhood'].isin(neighborhood_options)) &
    (df['reason'].isin(reason_options))
]

# Add derived column
filtered['resolution_time'] = (pd.to_datetime(filtered['closed_dt']) - filtered['open_dt']).dt.total_seconds() / 3600

# Dashboard title
st.title("📍 Boston 311 Service Request Dashboard")

# Top-level metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Requests", len(filtered))
col2.metric("Resolved On Time (%)", f"{(filtered['on_time'] == 'ONTIME').mean():.0%}")
col3.metric("Avg Resolution Time (hrs)", f"{filtered['resolution_time'].mean():.1f}")

# Charts
st.markdown("### Request Trends and Breakdown")

chart1, chart2 = st.columns((2, 1))

fig1 = px.histogram(filtered, x="reason", title="Requests by Reason", color="reason")
chart1.plotly_chart(fig1, use_container_width=True)

fig2 = px.pie(filtered, names="on_time", title="On Time vs Late")
chart2.plotly_chart(fig2, use_container_width=True)

chart3 = px.histogram(filtered, x="open_dt", nbins=30, title="Requests Over Time")
st.plotly_chart(chart3, use_container_width=True)

# Neighborhood heatmap
st.markdown("### Requests by Neighborhood")
neigh_df = filtered['neighborhood'].value_counts().reset_index()
neigh_df.columns = ['neighborhood', 'count']  # Rename columns

neigh_fig = px.bar(
    neigh_df,
    x='neighborhood',
    y='count',
    title='Request Volume by Neighborhood',
    labels={'count': 'Number of Requests'},
)
st.plotly_chart(neigh_fig, use_container_width=True)

# Raw data
st.markdown("### Filtered Data Table")
st.dataframe(filtered[['case_enquiry_id', 'open_dt', 'closed_dt', 'case_status', 'reason', 'neighborhood']])
