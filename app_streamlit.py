import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("CO2 Monitoring Dashboard")

file = st.file_uploader("Upload Excel", type=["xlsx"])

if file:

    df = pd.read_excel(file, engine="openpyxl")

    df["Timestamp"] = pd.to_datetime(df["Timestamp"])

    co2_cols = [c for c in df.columns if "CO2" in c.upper()]

    long_df = df.melt(
        id_vars=["Timestamp"],
        value_vars=co2_cols,
        var_name="Sensor",
        value_name="CO2"
    )

    high_co2 = long_df[long_df["CO2"] > 1000]

    st.subheader("CO2 Above 1000")
    st.dataframe(high_co2[["Timestamp","Sensor","CO2"]])

    # histogram
    fig1 = plt.figure()
    sns.histplot(high_co2["CO2"], kde=True)
    st.pyplot(fig1)

    # trend chart
    fig2 = plt.figure()
    sns.lineplot(data=high_co2, x="Timestamp", y="CO2", hue="Sensor")
    st.pyplot(fig2)
