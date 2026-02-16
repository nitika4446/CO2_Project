# ==================================
# IMPORTS
# ==================================
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ==================================
# PAGE SETTINGS
# ==================================
st.set_page_config(page_title="CO2 Monitoring Dashboard", layout="wide")

st.title("🔥 CO2 Monitoring Dashboard (CO2 > 1000)")

# ==================================
# LOAD DATA FROM LOCAL PROJECT
# ==================================
DATA_PATH = "master_sheet.xlsx"   # file inside github repo

try:
    df = pd.read_excel(DATA_PATH, engine="openpyxl")

except Exception as e:
    st.error(f"File loading error: {str(e)}")
    st.stop()

# ==================================
# AUTO DETECT DATE/TIME COLUMN
# ==================================
date_cols = [c for c in df.columns if any(x in c.lower() for x in ["time","date","timestamp","datetime"])]

if len(date_cols) == 0:
    st.error("No Date/Time column found.")
    st.stop()

time_col = date_cols[0]
df[time_col] = pd.to_datetime(df[time_col], errors="coerce")

# ==================================
# AUTO DETECT CO2 COLUMNS
# ==================================
co2_cols = [c for c in df.columns if "co2" in c.lower()]

if len(co2_cols) == 0:
    st.error("No CO2 columns detected.")
    st.stop()

# ==================================
# RESHAPE DATA
# ==================================
long_df = df.melt(
    id_vars=[time_col],
    value_vars=co2_cols,
    var_name="Sensor",
    value_name="CO2"
)

long_df = long_df.dropna()

# ==================================
# FILTER CO2 > 1000
# ==================================
high_co2 = long_df[long_df["CO2"] > 1000]

# ==================================
# REPORT
# ==================================
st.subheader("📊 Report Summary")

col1, col2, col3 = st.columns(3)

col1.metric("Total Records", len(long_df))
col2.metric("CO2 Above 1000", len(high_co2))
col3.metric("Max CO2", high_co2["CO2"].max())

# ==================================
# TABLE
# ==================================
st.subheader("🚨 CO2 Above 1000 (with Date & Time)")

st.dataframe(high_co2[[time_col,"Sensor","CO2"]])

# ==================================
# CHARTS
# ==================================
st.subheader("📈 Charts")

# Histogram
fig1 = plt.figure()
sns.histplot(high_co2["CO2"], kde=True)
st.pyplot(fig1)

# Boxplot
fig2 = plt.figure()
sns.boxplot(y=high_co2["CO2"])
st.pyplot(fig2)

# Trend chart
fig3 = plt.figure(figsize=(10,5))
sns.lineplot(data=high_co2, x=time_col, y="CO2", hue="Sensor")
st.pyplot(fig3)
