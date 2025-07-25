import os
import pandas as pd
import numpy as np
import streamlit as st

# ------------------------
# File Loading & Preprocessing
# ------------------------

script_dir = os.getcwd()
un_path = os.path.join(script_dir, 'country_profile_variables.csv')
happiness_path = os.path.join(script_dir, 'WHR2023.csv')

un_df = pd.read_csv(un_path)
happiness_df = pd.read_csv(happiness_path)

# Standardize column names
un_df.rename(columns={'country': 'Country'}, inplace=True)
happiness_df.rename(columns={
    'Country name': 'Country',
    'Ladder score': 'Happiness Score'
}, inplace=True)

# Replace formal names with common names for consistency
name_map = {
    'Viet Nam': 'Vietnam',
    'Bolivia (Plurinational State of)': 'Bolivia',
    'Turkey': 'Turkiye',
    'United States of America': 'United States',
    'China, Hong Kong SAR': 'Hong Kong S.A.R. of China',
    'Iran (Islamic Republic of)': 'Iran',
    'Russian Federation': 'Russia',
    'Republic of Korea': 'South Korea',
    'Venezuela (Bolivarian Republic of)': 'Venezuela'
}
un_df['Country'] = un_df['Country'].replace(name_map)

# Save unmatched country names for inspection
un_countries = set(un_df['Country'])
happy_countries = set(happiness_df['Country'])
only_in_un = sorted(un_countries - happy_countries)
only_in_happiness = sorted(happy_countries - un_countries)

unmatched_df = pd.DataFrame({
    'Only in UN Dataset': pd.Series(only_in_un),
    'Only in Happiness Dataset': pd.Series(only_in_happiness)
})
unmatched_df.to_csv('unmatched_countries.csv', index=False)

# Merge on cleaned country names
merged_df = pd.merge(un_df, happiness_df, on='Country', how='inner')
merged_df.to_csv('merged_data.csv', index=False)
print("Merged CSV saved as 'merged_data.csv' with common country names.")

# ------------------------
# Streamlit App
# ------------------------

@st.cache_data
def load_data():
    return pd.read_csv("merged_data.csv")

# Setup Streamlit page
st.set_page_config(layout="wide")
df = load_data()

st.title("🌍 Global Socioeconomic Explorer & Happiness Analysis")

# Sidebar - Select country
countries = sorted(df['Country'].dropna().unique())
selected_country = st.sidebar.selectbox("Select a Country", countries)

# Filter for selected country
country_data = df[df['Country'] == selected_country]

# Define categories and indicators
categories = {
    "Demographic": [
        "Population in thousands (2017)",
        "Population density (per km2, 2017)",
        "Sex ratio (m per 100 f, 2017)",
        "Population growth rate (average annual %)",
        "Urban population (% of total population)"
    ],
    "Economy": [
        "GDP: Gross domestic product (million current US$)",
        "GDP growth rate (annual %, const. 2005 prices)",
        "GDP per capita (current US$)",
        "Unemployment (% of labour force)",
        "Labour force participation (female/male pop. %)"
    ],
    "Sectoral Breakdown": [
        "Economy: Agriculture (% of GVA)",
        "Economy: Industry (% of GVA)",
        "Economy: Services and other activity (% of GVA)",
        "Employment: Agriculture (% of employed)",
        "Employment: Industry (% of employed)",
        "Employment: Services (% of employed)"
    ],
    "Trade": [
        "International trade: Exports (million US$)",
        "International trade: Imports (million US$)",
        "International trade: Balance (million US$)",
        "Balance of payments, current account (million US$)"
    ],
    "Agriculture & Food": [
        "Agricultural production index (2004-2006=100)",
        "Food production index (2004-2006=100)"
    ],
    "Happiness Contributors": [
        "Explained by: Freedom to make life choices",
        "Explained by: Generosity",
        "Explained by: Perceptions of corruption",
        "Dystopia + residual"
    ]
}

# Global statistics
global_means = df.mean(numeric_only=True)
global_stds = df.std(numeric_only=True)

# Function to format value with colored label
def format_value(val, mean, std):
    try:
        val = float(val)
    except:
        return str(val)

    diff = val - mean
    if abs(diff) < 0.1 * std:
        return f"{val:.2f} (normal)"
    elif diff >= std:
        return f"<span style='color:green'><b>{val:.2f}</b> (very good)</span>"
    elif diff >= 0.1 * std:
        return f"<span style='color:green'>{val:.2f} (good)</span>"
    elif diff <= -std:
        return f"<span style='color:red'><b>{val:.2f}</b> (very bad)</span>"
    elif diff <= -0.1 * std:
        return f"<span style='color:red'>{val:.2f} (bad)</span>"
    else:
        return f"{val:.2f}"

# Display all sections
for section, cols in categories.items():
    with st.expander(f"{section} Indicators", expanded=False):
        available_cols = [col for col in cols if col in country_data.columns]
        if not available_cols:
            st.warning("No data available for this section.")
            continue

        st.markdown(f"### {selected_country}'s {section} Overview")
        for col in available_cols:
            val = country_data[col].values[0]
            mean = global_means.get(col, None)
            std = global_stds.get(col, None)
            if mean is not None and std is not None:
                formatted = format_value(val, mean, std)
            else:
                formatted = str(val)
            st.markdown(f"<b>{col}:</b> {formatted}", unsafe_allow_html=True)
