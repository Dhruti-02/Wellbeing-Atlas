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

un_df.rename(columns={'country': 'Country'}, inplace=True)
whr_df.rename(columns={'Country name': 'Country', 'Ladder score': 'Happiness Score'}, inplace=True)

# --- MERGE ---
df = pd.merge(un_df, whr_df, on="Country")

# --- CLEAN COUNTRY NAMES ---
df['Country_clean'] = df['Country'].astype(str).str.strip()

# --- CONVERT NUMERIC COLUMNS ---
non_convert_cols = ['Country', 'Country_clean']
for col in df.columns:
    if df[col].dtype == 'object' and col not in non_convert_cols:
        df[col] = df[col].str.replace(",", "").str.replace(" ", "")
        df[col] = pd.to_numeric(df[col], errors='coerce')

# --- HANDLE MISSING LIFE EXPECTANCY ---
if 'Life expectancy at birth (females/males, years)' in df.columns:
    df[['LifeExp_f', 'LifeExp_m']] = df['Life expectancy at birth (females/males, years)'] \
    .astype(str).str.extract(r'([\d.]+)[ /]+([\d.]+)').astype(float)

    df['Life expectancy at birth (years)'] = df[['LifeExp_f', 'LifeExp_m']].mean(axis=1)

# --- SIDEBAR ---
st.sidebar.title("Country Insights")
countries = sorted(df['Country_clean'].dropna().unique())
selected_country = str(st.sidebar.selectbox("Select a Country", countries)).strip()
show_interpretation = st.sidebar.checkbox("Show Interpretations", value=True)

# --- LEGEND ---
with st.expander("Color Legend"):
    st.markdown("""
    - 🟩 **Green**: Above global average (Good/High)
    - 🟨 **Yellow**: Around average (Neutral)
    - 🟥 **Red**: Below average (Needs Improvement)
    """)

# --- FILTER COUNTRY ---
filtered_df = df[df['Country_clean'].str.lower() == selected_country.lower()]
if filtered_df.empty:
    st.error(f"❌ No data found for '{selected_country}'. Please try another country.")
    st.caption(f"Available countries: {df['Country_clean'].unique().tolist()}")
    st.stop()
country_data = filtered_df.iloc[0]

# --- MAIN TITLE ---
st.title("🌍 Wellbeing Atlas: Socioeconomic & Happiness Insights")
st.header(f"📌 Overview for {selected_country}")

# --- INDICATORS ---
indicators = [
    'GDP per capita (current US$)',
    'Economy: Agriculture (% of GVA)',
    'Economy: Industry (% of GVA)',
    'Economy: Services and other activity (% of GVA)',  # corrected full column
    'Population density (per km2, 2017)',
    'Sex ratio (m per 100 f, 2017)',
    'Life expectancy at birth (years)',  # fixed
    'Happiness Score'
]

# --- METRICS WITH COLOR ---
st.subheader("📊 Country Performance vs Global Average")

for ind in indicators:
    if ind not in df.columns:
        st.warning(f"⚠️ Indicator not found in dataset: {ind}")
        continue

    val = country_data.get(ind, np.nan)
    if pd.isna(val):
        continue

    mean = df[ind].mean()
    try:
        float_val = float(val)
        if float_val < mean * 0.9:
            color = "🟥"
        elif float_val < mean * 1.1:
            color = "🟨"
        else:
            color = "🟩"

        formatted = f"{float_val:.2f}"
        progress_val = max(0.0, min(float_val / (2 * mean), 1.0))

        st.progress(progress_val, text=f"{ind}: {color} {formatted} | Global Avg: {mean:.2f}")
        if show_interpretation:
            st.markdown(f"**{ind}** → {color} {'High' if color == '🟩' else 'Low' if color == '🟥' else 'Neutral'}")
    except:
        st.write(f"{ind}: {val}")

# --- CORRELATION HEATMAP ---
st.subheader("📈 Correlation Between Features")
num_df = df[[i for i in indicators if i in df.columns]].dropna()
if not num_df.empty:
    corr = num_df.corr()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
    st.pyplot(fig)
else:
    st.info("Not enough data for correlation heatmap.")

# --- MULTI-FEATURE SCATTER ---
st.subheader("🧪 Happiness vs Multiple Indicators")
scatter_options = [i for i in indicators if i != 'Happiness Score' and i in df.columns]
selected_features = st.multiselect(
    "Select indicators to compare with Happiness Score",
    scatter_options,
    default=['GDP per capita (current US$)', 'Life expectancy at birth (years)']
)

if selected_features:
    melted = df[['Country', 'Happiness Score'] + selected_features].melt(
        id_vars=['Country', 'Happiness Score'],
        var_name='Feature', value_name='Value'
    )
    chart = alt.Chart(melted.dropna()).mark_circle(size=60).encode(
        x=alt.X('Value:Q', title=None),
        y='Happiness Score:Q',
        color='Feature:N',
        tooltip=['Country', 'Feature', 'Value', 'Happiness Score']
    ).properties(width=250, height=250).facet(
        facet='Feature:N', columns=2
    )
    st.altair_chart(chart, use_container_width=True)
else:
    st.info("Select at least one feature to display scatter plots.")

# --- Calculate global average happiness ---
global_avg_happiness = df['Happiness Score'].mean()

# --- Get selected country happiness score ---
country_happiness = country_data['Happiness Score']

# --- Plot comparison ---
fig, ax = plt.subplots(figsize=(6, 3.5))
bars = ax.bar(['Global Avg', selected_country], [global_avg_happiness, country_happiness],
              color=['gray', 'royalblue'])

# Annotate values on bars
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, height + 0.05,
            f'{height:.2f}', ha='center', va='bottom', fontsize=10)
    
color = 'green' if country_happiness >= global_avg_happiness else 'red'
bars[1].set_color(color)

ax.set_ylabel("Happiness Score")
ax.set_title("Happiness Score: Country vs Global Average")
st.pyplot(fig)
