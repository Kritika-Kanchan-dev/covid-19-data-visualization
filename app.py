import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

@st.cache_data
def load_data():
    return pd.read_csv("country_wise_latest.csv")

df = load_data()

st.sidebar.title("⚙️ Dashboard Controls")

countries = df["Country/Region"].unique()
selected_country = st.sidebar.selectbox("Select Country", ["All Countries"] + list(countries))

selected_metric = st.sidebar.selectbox(
    "Select Metric", ["Confirmed", "Deaths", "Recovered", "Active"]
)

st.title("🌍 COVID-19 Interactive Data Visualization Dashboard")

st.markdown("""
This dashboard explores **COVID-19 statistics** across countries and regions.  
Use the **sidebar dropdown** to switch between:
- A **specific country view**  
- **All countries combined view**  
""")

if selected_country != "All Countries":
    st.subheader(f"📌 COVID-19 Statistics for {selected_country}")
    country_data = df[df["Country/Region"] == selected_country].iloc[0]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Confirmed", f"{country_data['Confirmed']:,}")
    col2.metric("Deaths", f"{country_data['Deaths']:,}")
    col3.metric("Recovered", f"{country_data['Recovered']:,}")
    col4.metric("Active", f"{country_data['Active']:,}")

    fig = px.pie(
        values=[country_data["Deaths"], country_data["Recovered"], country_data["Active"]],
        names=["Deaths", "Recovered", "Active"],
        hole=0.4,
        title=f"Case Distribution in {selected_country}",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    st.plotly_chart(fig)

else:
    st.subheader(f"🌍 Top 10 Countries by {selected_metric}")
    top10 = df.sort_values(selected_metric, ascending=False).head(10)

    fig = px.bar(
        top10,
        x=selected_metric,
        y="Country/Region",
        orientation="h",
        color=selected_metric,
        color_continuous_scale="Viridis",
        title=f"Top 10 Countries by {selected_metric}",
    )
    st.plotly_chart(fig)

    st.subheader("Recovery vs Death Rate Across Regions")
    fig = px.scatter(
        df,
        x="Deaths / 100 Cases",
        y="Recovered / 100 Cases",
        color="WHO Region",
        size="Confirmed",
        hover_name="Country/Region",
        title="Recovery vs Death Rate",
    )
    st.plotly_chart(fig)

    st.subheader("Proportion of Cases by WHO Region")
    region_sum = df.groupby("WHO Region")[["Confirmed", "Deaths"]].sum().reset_index()
    fig = px.pie(
        region_sum,
        names="WHO Region",
        values="Confirmed",
        hole=0.4,
        color="WHO Region",
        title="Share of Confirmed Cases by Region",
    )
    st.plotly_chart(fig)

    st.subheader("Correlation Heatmap")
    corr = df[["Confirmed", "Deaths", "Recovered", "Active"]].corr()
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
    st.pyplot(fig)

    confirmed_global = df["Confirmed"].sum()
    deaths_global = df["Deaths"].sum()
    recovered_global = df["Recovered"].sum()

    col1, col2, col3 = st.columns(3)
    col1.metric("🌍 Global Confirmed", f"{confirmed_global:,}")
    col2.metric("💀 Global Deaths", f"{deaths_global:,}")
    col3.metric("💚 Global Recovered", f"{recovered_global:,}")