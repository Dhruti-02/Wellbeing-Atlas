import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Wellbeing Atlas",
    page_icon="🌍",
    layout="wide"
)

# -----------------------------
# LOAD AND PREPARE DATA
# -----------------------------
@st.cache_data
def load_data():
    un_df = pd.read_csv("country_profile_variables.csv")
    whr_df = pd.read_csv("WHR2023.csv")

    un_df.rename(columns={"country": "Country"}, inplace=True)

    whr_df.rename(
        columns={
            "Country name": "Country",
            "Ladder score": "Happiness Score"
        },
        inplace=True
    )

    # Standardize country names
    un_df["Country"] = un_df["Country"].astype(str).str.strip()
    whr_df["Country"] = whr_df["Country"].astype(str).str.strip()

    # Merge datasets
    df = pd.merge(un_df, whr_df, on="Country", how="inner")

    # Create average life expectancy
    life_col = "Life expectancy at birth (females/males, years)"

    if life_col in df.columns:
        extracted = (
            df[life_col]
            .astype(str)
            .str.extract(r"([\d.]+)\s*/\s*([\d.]+)")
        )

        df["LifeExp_f"] = pd.to_numeric(
            extracted[0], errors="coerce"
        )

        df["LifeExp_m"] = pd.to_numeric(
            extracted[1], errors="coerce"
        )

        df["Life expectancy at birth (years)"] = df[
            ["LifeExp_f", "LifeExp_m"]
        ].mean(axis=1)

    # Convert numeric-looking columns
    text_cols = {
        "Country",
        "Country_clean",
        life_col
    }

    for col in df.columns:
        if col not in text_cols and df[col].dtype == "object":
            cleaned = (
                df[col]
                .astype(str)
                .str.replace(",", "", regex=False)
                .str.replace(" ", "", regex=False)
            )

            converted = pd.to_numeric(
                cleaned, errors="coerce"
            )

            if converted.notna().any():
                df[col] = converted

    df["Country_clean"] = df["Country"].astype(str).str.strip()

    return df


try:
    df = load_data()

except FileNotFoundError as e:
    st.error(
        f"Could not find {e.filename}. Keep both CSV files "
        "in the same folder as app.py and include them "
        "in your GitHub repository."
    )
    st.stop()

except Exception as e:
    st.error(f"Could not load the datasets: {e}")
    st.stop()


if "Happiness Score" not in df.columns:
    st.error(
        "Happiness Score was not found. "
        "Check the columns in WHR2023.csv."
    )
    st.stop()


# -----------------------------
# TITLE AND SIDEBAR
# -----------------------------
st.title("🌍 Wellbeing Atlas")

st.write(
    "Explore how happiness scores relate to socioeconomic "
    "indicators across countries. These comparisons show "
    "associations, not proof of cause and effect."
)

countries = sorted(
    df["Country_clean"].dropna().unique().tolist()
)

if not countries:
    st.error("No countries found after merging the datasets.")
    st.stop()

st.sidebar.header("Explore a country")

selected_country = st.sidebar.selectbox(
    "Select a country",
    countries
)

show_data_table = st.sidebar.checkbox(
    "Show country data table",
    value=False
)

country_rows = df[
    df["Country_clean"] == selected_country
]

country_data = country_rows.iloc[0]


# -----------------------------
# OVERVIEW METRICS
# -----------------------------
st.header(f"Country Overview: {selected_country}")

happiness = pd.to_numeric(
    country_data["Happiness Score"],
    errors="coerce"
)

global_happiness = pd.to_numeric(
    df["Happiness Score"],
    errors="coerce"
).mean()

happiness_values = pd.to_numeric(
    df["Happiness Score"],
    errors="coerce"
).dropna()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Happiness Score",
    f"{happiness:.2f}" if pd.notna(happiness) else "N/A"
)

col2.metric(
    "Dataset Average Happiness",
    f"{global_happiness:.2f}"
    if pd.notna(global_happiness) else "N/A"
)

col3.metric(
    "Countries in Merged Dataset",
    f"{df['Country_clean'].nunique():,}"
)

col4.metric(
    "Countries with Happiness Data",
    f"{len(happiness_values):,}"
)

if pd.notna(happiness) and pd.notna(global_happiness):
    difference = happiness - global_happiness

    if difference > 0:
        st.info(
            f"{selected_country} is {difference:.2f} points "
            "above the dataset's average happiness score."
        )

    elif difference < 0:
        st.info(
            f"{selected_country} is {abs(difference):.2f} points "
            "below the dataset's average happiness score."
        )

    else:
        st.info(
            f"{selected_country} is at the dataset's "
            "average happiness score."
        )


# -----------------------------
# COUNTRY INDICATORS VS MEAN
# -----------------------------
st.header("Country Performance Compared with the Dataset Average")

st.caption(
    "Values are compared with the available-country mean. "
    "A higher value is not automatically better for every indicator."
)

comparison_indicators = [
    "GDP per capita (current US$)",
    "Life expectancy at birth (years)",
    "Healthy life expectancy",
    "Happiness Score",
    "Economy: Agriculture (% of GVA)",
    "Economy: Industry (% of GVA)",
    "Economy: Services and other activity (% of GVA)"
]

comparison_indicators = [
    col for col in comparison_indicators
    if col in df.columns
]

rows = []

for col in comparison_indicators:
    values = pd.to_numeric(df[col], errors="coerce")

    country_value = pd.to_numeric(
        pd.Series([country_data.get(col)]),
        errors="coerce"
    ).iloc[0]

    mean_value = values.mean()

    count = int(values.notna().sum())

    if pd.notna(country_value):
        rows.append({
            "Indicator": col,
            "Selected Country": country_value,
            "Dataset Mean": mean_value,
            "Countries with Data": count,
            "Difference from Mean": country_value - mean_value
        })

if rows:
    summary = pd.DataFrame(rows)

    numeric_cols = [
        "Selected Country",
        "Dataset Mean",
        "Difference from Mean"
    ]

    summary[numeric_cols] = summary[numeric_cols].round(2)

    st.dataframe(
        summary,
        use_container_width=True,
        hide_index=True
    )

else:
    st.info(
        "No comparable indicator values are available "
        "for this country."
    )


# -----------------------------
# HAPPINESS DISTRIBUTION
# -----------------------------
st.header("Distribution of Happiness Scores")

happiness_df = df[
    ["Country_clean", "Happiness Score"]
].copy()

happiness_df["Happiness Score"] = pd.to_numeric(
    happiness_df["Happiness Score"],
    errors="coerce"
)

happiness_df = happiness_df.dropna(
    subset=["Happiness Score"]
)

if not happiness_df.empty:
    fig, ax = plt.subplots(figsize=(9, 4))

    sns.histplot(
        data=happiness_df,
        x="Happiness Score",
        bins=15,
        kde=True,
        ax=ax
    )

    if pd.notna(happiness):
        ax.axvline(
            happiness,
            linestyle="--",
            linewidth=2,
            label=f"{selected_country}: {happiness:.2f}"
        )
        ax.legend()

    ax.set_title(
        "Distribution of Happiness Scores Across Countries"
    )
    ax.set_xlabel("Happiness Score")
    ax.set_ylabel("Number of Countries")

    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)


# -----------------------------
# TOP AND BOTTOM COUNTRIES
# -----------------------------
st.header("Countries with the Highest and Lowest Happiness Scores")

top_tab, bottom_tab = st.tabs(
    ["Highest Scores", "Lowest Scores"]
)

top_10 = happiness_df.nlargest(
    10, "Happiness Score"
).sort_values("Happiness Score")

bottom_10 = happiness_df.nsmallest(
    10, "Happiness Score"
).sort_values("Happiness Score", ascending=False)

with top_tab:
    fig, ax = plt.subplots(figsize=(9, 5))

    ax.barh(
        top_10["Country_clean"],
        top_10["Happiness Score"]
    )

    ax.set_xlabel("Happiness Score")
    ax.set_ylabel("")
    ax.set_title("10 Countries with the Highest Scores")

    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

with bottom_tab:
    fig, ax = plt.subplots(figsize=(9, 5))

    ax.barh(
        bottom_10["Country_clean"],
        bottom_10["Happiness Score"]
    )

    ax.set_xlabel("Happiness Score")
    ax.set_ylabel("")
    ax.set_title("10 Countries with the Lowest Scores")

    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)


# -----------------------------
# CORRELATION WITH HAPPINESS
# -----------------------------
st.header("Which Indicators Are Associated with Happiness?")

correlation_candidates = [
    "GDP per capita (current US$)",
    "Economy: Agriculture (% of GVA)",
    "Economy: Industry (% of GVA)",
    "Economy: Services and other activity (% of GVA)",
    "Population density (per km2, 2017)",
    "Sex ratio (m per 100 f, 2017)",
    "Life expectancy at birth (years)",
    "Healthy life expectancy"
]

correlation_candidates = [
    col for col in correlation_candidates
    if col in df.columns
    and pd.to_numeric(
        df[col], errors="coerce"
    ).notna().sum() >= 3
]

if correlation_candidates:
    corr_source = df[
        ["Happiness Score"] + correlation_candidates
    ].copy()

    for col in corr_source.columns:
        corr_source[col] = pd.to_numeric(
            corr_source[col],
            errors="coerce"
        )

    correlations = (
        corr_source.corr(numeric_only=True)["Happiness Score"]
        .drop("Happiness Score")
        .dropna()
        .sort_values()
    )

    if not correlations.empty:
        corr_plot = (
            correlations.rename("Correlation")
            .reset_index()
            .rename(columns={"index": "Indicator"})
        )

        fig, ax = plt.subplots(
            figsize=(10, max(4, 0.45 * len(corr_plot)))
        )

        bar_colors = [
            "steelblue" if value >= 0 else "indianred"
            for value in corr_plot["Correlation"]
        ]

        ax.barh(
            corr_plot["Indicator"],
            corr_plot["Correlation"],
            color=bar_colors
        )

        ax.axvline(0, color="black", linewidth=0.8)
        ax.set_xlim(-1, 1)

        ax.set_xlabel(
            "Pearson Correlation with Happiness (-1 to +1)"
        )

        ax.set_title(
            "Correlation of Each Indicator with Happiness"
        )

        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

        strongest = correlations.abs().idxmax()
        strongest_value = correlations[strongest]

        st.caption(
            f"Strongest absolute association among the displayed "
            f"indicators: {strongest} "
            f"(r = {strongest_value:.2f}). "
            "Correlation does not imply causation."
        )

    else:
        st.info(
            "Not enough paired numeric data to calculate correlations."
        )

else:
    st.info(
        "No suitable numeric indicators were found for correlation analysis."
    )


# -----------------------------
# INTERACTIVE SCATTER PLOT
# -----------------------------
st.header("Explore Happiness Against One Indicator")

scatter_options = [
    col for col in correlation_candidates
    if col != "Happiness Score"
]

if scatter_options:
    selected_indicator = st.selectbox(
        "Choose an indicator for the horizontal axis",
        scatter_options
    )

    scatter_df = df[
        ["Country_clean", "Happiness Score", selected_indicator]
    ].copy()

    scatter_df["Happiness Score"] = pd.to_numeric(
        scatter_df["Happiness Score"],
        errors="coerce"
    )

    scatter_df[selected_indicator] = pd.to_numeric(
        scatter_df[selected_indicator],
        errors="coerce"
    )

    scatter_df = scatter_df.dropna(
        subset=["Happiness Score", selected_indicator]
    )

    if len(scatter_df) >= 2:
        r = scatter_df[selected_indicator].corr(
            scatter_df["Happiness Score"]
        )

        fig, ax = plt.subplots(figsize=(9, 5))

        sns.regplot(
            data=scatter_df,
            x=selected_indicator,
            y="Happiness Score",
            scatter_kws={"alpha": 0.7, "s": 45},
            line_kws={"color": "red"},
            ax=ax
        )

        selected_point = scatter_df[
            scatter_df["Country_clean"] == selected_country
        ]

        if not selected_point.empty:
            ax.scatter(
                selected_point[selected_indicator],
                selected_point["Happiness Score"],
                s=120,
                marker="*",
                edgecolor="black",
                label=selected_country
            )
            ax.legend()

        ax.set_title(
            f"Happiness vs {selected_indicator} (r = {r:.2f})"
        )

        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

        st.caption(
            f"{len(scatter_df)} countries included. "
            "The line shows the overall linear trend; "
            "it does not establish cause and effect."
        )

    else:
        st.info(
            "Not enough complete observations to draw this chart."
        )


# -----------------------------
# HIGHER VS LOWER HAPPINESS GROUPS
# -----------------------------
st.header("How Do Higher- and Lower-Happiness Groups Differ?")

group_indicators = [
    "GDP per capita (current US$)",
    "Life expectancy at birth (years)"
]

group_indicators = [
    col for col in group_indicators
    if col in df.columns
]

if group_indicators:
    group_df = df[
        ["Country_clean", "Happiness Score"] + group_indicators
    ].copy()

    for col in ["Happiness Score"] + group_indicators:
        group_df[col] = pd.to_numeric(
            group_df[col],
            errors="coerce"
        )

    group_df = group_df.dropna(
        subset=["Happiness Score"]
    )

    if len(group_df) >= 4:
        low_cutoff = group_df["Happiness Score"].quantile(0.25)
        high_cutoff = group_df["Happiness Score"].quantile(0.75)

        group_df["Happiness Group"] = np.select(
            [
                group_df["Happiness Score"] <= low_cutoff,
                group_df["Happiness Score"] >= high_cutoff
            ],
            [
                "Lower Happiness (Bottom 25%)",
                "Higher Happiness (Top 25%)"
            ],
            default="Middle"
        )

        selected_groups = group_df[
            group_df["Happiness Group"] != "Middle"
        ]

        group_summary = (
            selected_groups
            .groupby("Happiness Group")[
                ["Happiness Score"] + group_indicators
            ]
            .mean()
            .round(2)
        )

        st.dataframe(
            group_summary,
            use_container_width=True
        )

        st.caption(
            "These are averages for the bottom and top quartiles "
            "of happiness scores. They describe group differences, "
            "not causal effects."
        )

    else:
        st.info(
            "Not enough rows to compare happiness groups."
        )


# -----------------------------
# OPTIONAL DATA TABLE
# -----------------------------
if show_data_table:
    st.header("Merged Dataset")

    st.dataframe(
        df,
        use_container_width=True
    )


# -----------------------------
# FOOTER
# -----------------------------
st.divider()

st.caption(
    "Data: UN country profile variables and World Happiness "
    "Report 2023. The merge includes countries present in both "
    "datasets. Indicators may have different reference years "
    "and missing-value coverage."
)
