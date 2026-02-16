import gradio as gr
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def co2_dashboard(file):

    df = pd.read_excel(file, engine="openpyxl")

    df["Timestamp"] = pd.to_datetime(df["Timestamp"])

    # auto detect CO2 columns
    co2_cols = [c for c in df.columns if "CO2" in c.upper()]

    long_df = df.melt(
        id_vars=["Timestamp"],
        value_vars=co2_cols,
        var_name="Sensor",
        value_name="CO2"
    )

    high_co2 = long_df[long_df["CO2"] > 1000]

    # Report
    report = f"""
    Total Records: {len(long_df)}
    High CO2 (>1000): {len(high_co2)}
    Max CO2: {high_co2['CO2'].max()}
    """

    # Chart 1
    plt.figure()
    sns.histplot(high_co2["CO2"], kde=True)
    plt.title("CO2 Distribution")
    hist = "hist.png"
    plt.savefig(hist)
    plt.close()

    # Chart 2
    plt.figure(figsize=(10,5))
    sns.lineplot(data=high_co2, x="Timestamp", y="CO2", hue="Sensor")
    plt.title("CO2 Trend")
    trend = "trend.png"
    plt.savefig(trend)
    plt.close()

    return report, high_co2[["Timestamp","Sensor","CO2"]], hist, trend

demo = gr.Interface(
    fn=co2_dashboard,
    inputs=gr.File(),
    outputs=["text","dataframe","image","image"],
    title="CO2 Monitoring Dashboard"
)

demo.launch(share=True)
