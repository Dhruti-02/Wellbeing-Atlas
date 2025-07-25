import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

# --- THEME TOGGLE ---
theme = st.sidebar.radio("Theme", ["Light", "Dark"])
if theme == "Dark":
    st.markdown("""
        <style>
        body {
            background-color: #0e1117;
            color: #f5f5f5;
        }
        </style>
    """, unsafe_allow_html=True)

# --- LOAD DATA ---
un_path = "country_profile_variables.csv"
whr_path = "WHR2023.csv"

un_df = pd.read_csv(un_path)
whr_df = pd.read_csv(whr_path)
whr_df.rename(columns={"Country name": "Country", "Ladder score": "Happiness Score"}, inplace=True)

# --- MERGE ---
df = pd.merge(un_df, whr_df, on="Country")

# --- SIDEBAR ---
st.sidebar.title("Country Insights")
countries = sorted(df['Country'].unique())
selected_country = st.sidebar.selectbox("Select a Country", countries)
show_interpretation = st.sidebar.checkbox("Show Interpretations", value=True)

# --- LEGEND ---
with st.expander("Color Legend"):
    st.markdown("""
    - 🟩 **Green**: Above global average (Good/High)
    - 🟨 **Yellow**: Around average (Neutral)
    - 🟥 **Red**: Below average (Needs Improvement)
    """)

# --- COUNTRY DATA ---
country_data = df[df['Country'] == selected_country].squeeze()

st.title("🌍 Wellbeing Atlas: Socioeconomic & Happiness Insights")
st.header(f"📌 Overview for {selected_country}")

# --- INDICATORS TO SHOW ---
indicators = [
    'GDP per capita (current US$)',
    'Economy: Agriculture (% of GVA)',
    'Economy: Industry (% of GVA)',
    'Economy: Services (% of GVA)',
    'Population density (per km2, 2017)',
    'Sex ratio (m per 100 f, 2017)',
    'Life expectancy at birth (years)',
    'Happiness Score'
]

# --- METRICS WITH COLOR & BAR ---
st.subheader("📊 Country Performance vs Global Average")

for ind in indicators:
    if ind not in df.columns or pd.isna(country_data[ind]):
        continue
    val = country_data[ind]
    mean = df[ind].mean()
    try:
        float_val = float(val)
        color = "🟩"
        if float_val < mean * 0.9:
            color = "🟥"
        elif float_val < mean * 1.1:
            color = "🟨"
        formatted = f"{float_val:.2f}"
        progress_val = max(0.0, min(float_val / (2 * mean), 1.0))
        st.progress(progress_val, text=f"{ind}: {color} {formatted} | Global Avg: {mean:.2f}")
        if show_interpretation:
            st.markdown(f"**{ind}** → {color} {'High' if color=='🟩' else 'Low' if color=='🟥' else 'Neutral'}")
    except:
        st.write(f"{ind}: {val}")

# --- CORRELATION HEATMAP ---
st.subheader("📈 Correlation Between Features")
num_df = df[indicators].dropna()
corr = num_df.corr()
fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
st.pyplot(fig)

# --- MULTI-FEATURE SCATTER ---
st.subheader("🧪 Happiness vs Multiple Indicators")
selected_features = st.multiselect("Select indicators to compare with Happiness Score", [i for i in indicators if i != 'Happiness Score'], default=['GDP per capita (current US$)', 'Life expectancy at birth (years)'])

if selected_features:
    melted = df[['Country', 'Happiness Score'] + selected_features].melt(id_vars=['Country', 'Happiness Score'], var_name='Feature', value_name='Value')
    chart = alt.Chart(melted.dropna()).mark_circle(size=60).encode(
        x=alt.X('Value:Q', title=None),
        y='Happiness Score:Q',
        color='Feature:N',
        tooltip=['Country', 'Feature', 'Value', 'Happiness Score']
    ).properties(
        width=250, height=250
    ).facet(
        facet='Feature:N', columns=2
    )
    st.altair_chart(chart, use_container_width=True)
