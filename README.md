# Wellbeing Atlas 🌍

An interactive data analytics dashboard exploring the relationship between country-level indicators, life expectancy, and happiness scores. The project combines data cleaning, exploratory data analysis (EDA), statistical correlation, and interactive visualisation to help users explore differences across countries.

## 📌 Project Overview

Wellbeing Atlas brings together country profile data and the World Happiness Report 2023 to explore patterns associated with national well-being.

The project has two main components:

* **Exploratory Data Analysis (`analysis.ipynb`):** Data inspection, cleaning, statistical analysis, and visualisation.
* **Interactive Dashboard (`app.py`):** A Streamlit web application for exploring country-level data and relationships between indicators.

## 🎯 Objectives

* Explore differences in well-being indicators across countries
* Examine the relationship between happiness scores and numerical indicators
* Analyse life expectancy using available country profile data
* Identify patterns and associations through statistical analysis
* Present findings through an interactive dashboard

## 📂 Dataset

The project uses two datasets:

**1. World Happiness Report 2023 (`WHR2023.csv`)**

Contains country-level happiness scores and associated indicators reported in the World Happiness Report 2023.

**2. Country Profile Variables (`country_profile_variables.csv`)**

Contains country-level demographic, health, economic, and other development indicators, including life expectancy.

The datasets are cleaned and merged using country identifiers. The merged dataset supports comparisons between happiness scores and country-level indicators.

*Note: The availability of individual indicators depends on the original datasets. Missing values are retained where appropriate rather than automatically replaced with zero.*

## 🛠️ Tools and Technologies

* **Python** — Data analysis and processing
* **Pandas** — Data cleaning, manipulation, and statistical calculations
* **NumPy** — Numerical operations
* **Matplotlib and Seaborn** — Data visualisation
* **Jupyter Notebook** — Exploratory data analysis
* **Streamlit** — Interactive dashboard development
* **Git and GitHub** — Version control and project hosting
* **Streamlit Community Cloud** — Dashboard deployment

## ⚙️ Project Workflow

### 1. Data Loading and Inspection

* Loaded both datasets into Pandas DataFrames
* Inspected column names, data types, and missing values
* Identified country identifiers and relevant numerical indicators

### 2. Data Cleaning and Preparation

* Standardised country identifiers for merging
* Converted relevant columns to numerical data types
* Examined missing values and prepared data for analysis
* Combined the datasets into a merged DataFrame

### 3. Exploratory Data Analysis

* Examined the distribution of numerical indicators
* Compared country-level values
* Created visualisations to explore patterns in the data
* Investigated associations between happiness scores and other indicators

### 4. Statistical Correlation Analysis

Calculated Pearson correlation coefficients to examine the direction and strength of linear relationships between numerical indicators and happiness scores.

### 5. Interactive Dashboard

Developed a Streamlit dashboard that allows users to explore country data and visualise selected relationships.

### 6. Deployment

Deployed the application using Streamlit Community Cloud, making the dashboard accessible through a web browser.

## 📊 Dashboard Features

* **Country Selection:** Select a country to explore its available data
* **Country Data Table:** Inspect the selected country's indicator values
* **Indicator Comparison:** Compare country-level values with dataset averages where supported
* **Happiness Distribution:** Explore the distribution of happiness scores
* **Country Rankings:** Compare countries with higher and lower happiness scores
* **Correlation Analysis:** Examine the linear associations between numerical indicators and happiness
* **Scatter Plots:** Explore relationships between selected indicators and happiness scores

## 📐 Statistical Concepts: Mean, Variance, Covariance and Correlation

This project uses statistical measures to examine relationships between country-level indicators and happiness scores.

### 1. Mean

The mean is the average value of a variable.

**Formula:**

```text
Mean(X) = Sum of all X values / n
```

Where:

* `X` = numerical variable, such as life expectancy
* `n` = number of valid observations

**Example:** For values 60, 70 and 80:

Mean(X) = (60 + 70 + 80) / 3 = 70

### 2. Variance

Variance measures how widely observations are spread around their mean.

**Sample variance:**

```text
s² = Sum of (Xᵢ - X̄)² / (n - 1)
```

**Population variance:**

```text
σ² = Sum of (Xᵢ - μ)² / N
```

Where:

* `Xᵢ` = individual observation
* `X̄` = sample mean
* `μ` = population mean
* `n` = sample size
* `N` = population size
* `s²` = sample variance
* `σ²` = population variance

**How it works:**

1. Calculate the mean.
2. Subtract the mean from each observation.
3. Square each difference.
4. Add the squared differences.
5. Divide by `n - 1` for sample variance or `N` for population variance.

### 3. Standard Deviation

Standard deviation measures the spread of observations in the original units of the variable.

**Sample standard deviation:**

```text
s = √(s²)
```

**Population standard deviation:**

```text
σ = √(σ²)
```

Standard deviation is the square root of variance.

### 4. Covariance

Covariance measures whether two variables tend to vary in the same or opposite directions relative to their means.

**Sample covariance:**

```text
Cov(X, Y) = Sum[(Xᵢ - X̄)(Yᵢ - Ȳ)] / (n - 1)
```

**Population covariance:**

```text
Cov(X, Y) = Sum[(Xᵢ - μₓ)(Yᵢ - μᵧ)] / N
```

Where:

* `X` = numerical indicator, such as life expectancy
* `Y` = happiness score
* `Xᵢ`, `Yᵢ` = paired observations for country `i`
* `X̄`, `Ȳ` = sample means
* `μₓ`, `μᵧ` = population means

**Interpretation:**

* **Positive covariance:** The variables tend to be above their means together or below their means together.
* **Negative covariance:** The variables tend to deviate from their means in opposite directions.
* **Zero covariance:** No net linear co-variation; a nonlinear relationship may still exist.

Covariance depends on the units of the variables, so its magnitude is difficult to compare across different variable pairs.

### 5. Pearson Correlation Coefficient

Pearson correlation measures the direction and strength of the linear relationship between two numerical variables.

**Formula:**

```text
r = Cov(X, Y) / (sₓ × sᵧ)
```

Equivalently, using sample observations:

```text
r = Sum[(Xᵢ - X̄)(Yᵢ - Ȳ)]
    / √[Sum(Xᵢ - X̄)² × Sum(Yᵢ - Ȳ)²]
```

Where:

* `r` = Pearson correlation coefficient
* `Cov(X, Y)` = sample covariance
* `sₓ`, `sᵧ` = sample standard deviations of X and Y

**Interpretation:**

| Correlation value | Meaning                              |
| ----------------- | ------------------------------------ |
| `+1`              | Perfect positive linear relationship |
| Greater than `0`  | Positive linear association          |
| Approximately `0` | Little or no linear association      |
| Less than `0`     | Negative linear association          |
| `-1`              | Perfect negative linear relationship |

The closer the absolute value of `r` is to 1, the stronger the linear association.

### 6. Application to Wellbeing Atlas

In this project:

* `X` represents a numerical country-level indicator, such as life expectancy.
* `Y` represents the happiness score of the country.

Pearson correlation is used to examine whether countries with higher or lower indicator values tend to have correspondingly higher or lower happiness scores.

**Important limitation:** Correlation does not imply causation. These calculations identify statistical associations in the available country-level data; they do not establish that a particular indicator causes changes in happiness.


### 6. Application to Wellbeing Atlas

In this project, \(X\) represents a numerical country-level indicator, such as life expectancy, while \(Y\) represents the country's happiness score.

Pearson correlation is used to examine whether countries with higher or lower values of a given indicator tend to have correspondingly higher or lower happiness scores.

**Important limitation:** Correlation does not imply causation. These calculations identify statistical associations in the available country-level data; they do not establish that a particular indicator causes changes in happiness.

### Understanding Covariance

Covariance measures whether two variables tend to vary together.

For \(n\) paired observations, the sample covariance is:

$$
\operatorname{Cov}(X,Y)=
\frac{\displaystyle\sum_{i=1}^{n}
(X_i-\bar X)(Y_i-\bar Y)}{n-1}
$$

Where:

* \(X_i\) and \(Y_i\) are the observed values for country \(i\)
* \(\bar X\) and \(\bar Y\) are the respective means
* \(n\) is the number of observations with valid values for both variables
* \(n-1\) is the denominator used for sample covariance

**Interpretation:**

* **Positive covariance:** The variables tend to deviate from their means in the same direction
* **Negative covariance:** The variables tend to deviate from their means in opposite directions
* **Zero covariance:** There is no net linear co-variation, although a nonlinear relationship may still exist

Covariance depends on the units and scales of the variables. Pearson correlation standardises covariance by dividing it by the product of the standard deviations, making the coefficient unitless and easier to compare across different pairs of variables.

### Implementation in Python

Pandas can calculate Pearson correlation coefficients using:

```python
correlations = df.corr(numeric_only=True)
```

To extract the correlations with a particular happiness-score column:

```python
happiness_correlations = correlations["Happiness score"]
```

The column name must match the name used in the merged DataFrame.

### Limitations

* Correlation does not imply causation.
* A positive association does not prove that an indicator causes higher happiness.
* Pearson correlation measures linear relationships and may not capture nonlinear patterns.
* Missing values and the countries included in each comparison can affect the results.
* Country-level associations do not necessarily describe relationships between individuals.

## 📈 Key Analytical Questions

The project can be used to explore questions such as:

* How do happiness scores vary across countries?
* How does life expectancy relate to happiness scores?
* Which numerical indicators show stronger positive or negative associations with happiness?
* How do selected indicators differ between countries with higher and lower happiness scores?
* What patterns can be observed in the merged country-level dataset?

The dashboard supports exploratory analysis of these questions; findings should be interpreted in the context of the available data.

## 🚀 How to Run Locally

### Prerequisites

Install Python and ensure that the project files are available locally.

### 1. Clone the repository

```bash
git clone https://github.com/Dhruti-02/Wellbeing-Atlas.git
cd Wellbeing-Atlas
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` is not yet available, install the required libraries:

```bash
pip install streamlit pandas numpy matplotlib seaborn
```

### 3. Check the project files

Ensure that `app.py` and the required CSV datasets are present in the repository directory. The notebook can be opened separately for analysis.

### 4. Run the dashboard

```bash
streamlit run app.py
```

The dashboard will open in your browser, usually at `http://localhost:8501`.

### 5. Run the notebook separately

Open `analysis.ipynb` in Jupyter Notebook or JupyterLab to inspect and execute the exploratory analysis.

## 📁 Project Structure

```text
Wellbeing-Atlas/
├── app.py
├── analysis.ipynb
├── WHR2023.csv
├── country_profile_variables.csv
├── requirements.txt
└── README.md
```

The notebook and other filenames should match the files actually present in the repository.

## 🌐 Live Dashboard

Explore the deployed application:

[**Wellbeing Atlas — Streamlit Dashboard**](https://wellbeing-atlas-jpcbs6vhxabhcbd98zueby.streamlit.app/)

## 🔮 Future Improvements

* Add more detailed country comparisons
* Improve handling and reporting of missing values
* Include additional statistical measures where appropriate
* Add filters for regions and selected indicators
* Expand the dashboard with more interactive visualisations

## 👩‍💻 Author

**Dhruti Shende**

B.Tech, Civil Engineering — IIT (BHU), Varanasi

GitHub: [Dhruti-02](https://github.com/Dhruti-02)

---

*Wellbeing Atlas is an exploratory data analytics project. Its visualisations highlight patterns and statistical associations in the available data and should not be interpreted as evidence of causation.*
