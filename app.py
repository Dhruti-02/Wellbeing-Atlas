import os
import pandas as pd

# Use current working directory instead of __file__
script_dir = os.getcwd()

# Build full paths
un_path = os.path.join(script_dir, 'country_profile_variables.csv')
happiness_path = os.path.join(script_dir, 'WHR2023.csv')

# Read the CSV files
un_df = pd.read_csv(un_path)
happiness_df = pd.read_csv(happiness_path)

# 1. Standardize column names
un_df.rename(columns={
    'country': 'Country'  # Normalize to match other dataset
}, inplace=True)

happiness_df.rename(columns={
    'Country name': 'Country',
    'Ladder score': 'Happiness Score'
}, inplace=True)

# 2. Get country sets
un_countries = set(un_df['Country'])
happy_countries = set(happiness_df['Country'])

# 3. Find unmatched countries
only_in_un = sorted(un_countries - happy_countries)
only_in_happiness = sorted(happy_countries - un_countries)

# 4. Merge datasets (inner join)
merged_df = pd.merge(un_df, happiness_df, on='Country', how='inner')

# 5. Save merged data
merged_df.to_csv('merged_data.csv', index=False)

# 6. Save unmatched countries
unmatched_df = pd.DataFrame({
    'Only in UN Dataset': pd.Series(only_in_un),
    'Only in Happiness Dataset': pd.Series(only_in_happiness)
})
unmatched_df.to_csv('unmatched_countries.csv', index=False)

# 7. Confirmation
print("✅ Files saved:")
print("- merged_data.csv")
print("- unmatched_countries.csv")


import pandas as pd
import os

# File paths
script_dir = os.getcwd()
un_path = os.path.join(script_dir, 'country_profile_variables.csv')
happiness_path = os.path.join(script_dir, 'WHR2023.csv')

# Load data
un_df = pd.read_csv(un_path)
happiness_df = pd.read_csv(happiness_path)

# Rename columns for consistency
un_df.rename(columns={'country': 'Country'}, inplace=True)
happiness_df.rename(columns={
    'Country name': 'Country',
    'Ladder score': 'Happiness Score'
}, inplace=True)

# Replace UN formal names with common names
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

# Merge on common names
merged_df = pd.merge(un_df, happiness_df, on='Country', how='inner')

# Save result
merged_df.to_csv('merged_data.csv', index=False)
print("✅ Merged CSV saved as 'merged_data.csv' with common country names.")


import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    return pd.read_csv("merged_data.csv")

# Setup
st.set_page_config(layout="wide")
df = load_data()

st.title("🌍 Global Socioeconomic Explorer & Happiness Analysis")

# Sidebar - Country selector
countries = sorted(df['Country'].dropna().unique())
selected_country = st.sidebar.selectbox("Select a Country", countries)

# Filter data for selected country
country_data = df[df['Country'] == selected_country]

# Category-wise indicators (based on your actual columns)
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

# Display data by category
for section, cols in categories.items():
    with st.expander(f"{section} Indicators", expanded=False):
        available_cols = [col for col in cols if col in country_data.columns]
        if not available_cols:
            st.warning("No data available for this section.")
            continue
        display_cols = ['Country'] + available_cols
        df_display = country_data[display_cols].transpose().reset_index()
        df_display.columns = ['Indicator', 'Value']
        df_display['Value'] = df_display['Value'].astype(str)

        st.dataframe(df_display, use_container_width=True)
