import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("country_wise_latest.csv")
    return df

df = load_data()

# App title
st.title("COVID-19 Data Visualization & Storytelling 📊")

# Show dataset
if st.checkbox("Show raw data"):
    st.write(df.head(20))

# Basic stats
st.subheader("Dataset Summary")
st.write(df.describe())

# Plot 1: Confirmed Cases by Top 10 Countries
st.subheader("Top 10 Countries with Highest Confirmed Cases")
top10 = df.sort_values("Confirmed", ascending=False).head(10)

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x="Confirmed", y="Country/Region", data=top10, ax=ax, palette="Blues_r")
ax.set_title("Top 10 Countries by Confirmed Cases")
st.pyplot(fig)

# Misleading Visualization Example
st.subheader("⚠️ Misleading Visualization Example")
fig, ax = plt.subplots()
sns.barplot(x="Country/Region", y="Confirmed", data=top10, ax=ax, palette="Reds")
ax.set_title("Misleading: No rotation, Hard to Read, Wrong scale")
st.pyplot(fig)

# Redesigned Correct Visualization
st.subheader("✅ Redesigned Visualization")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x="Confirmed", y="Country/Region", data=top10, palette="Greens_r", ax=ax)
ax.set_title("Redesigned: Clear and Informative")
st.pyplot(fig)

# Death Rate vs Recovery Rate (Scatter)
st.subheader("Death Rate vs Recovery Rate")
fig, ax = plt.subplots(figsize=(8, 6))
sns.scatterplot(
    x="Deaths / 100 Cases", 
    y="Recovered / 100 Cases", 
    hue="WHO Region", 
    data=df, 
    ax=ax
)
ax.set_title("Recovery vs Death Rate Across Regions")
st.pyplot(fig)

# Storytelling: Confirmed vs Deaths
st.subheader("Storytelling with Data")
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(
    x="Confirmed", 
    y="Deaths", 
    size="Recovered", 
    hue="WHO Region", 
    data=df, 
    alpha=0.7, 
    ax=ax
)
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_title("Log Scale View: Confirmed vs Deaths (size=Recovered)")
st.pyplot(fig)

st.markdown("""
### Insights:
- Countries with the largest confirmed cases are driving the global numbers.
- Some visualizations can mislead (e.g., bad scaling or poor labeling).
- Log scale reveals patterns between confirmed and death counts across regions.
""")