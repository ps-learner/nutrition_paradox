# ⚖️ Nutrition Paradox — A Global View on Obesity & Malnutrition

A full-stack data analytics project built on **WHO Global Health Observatory** data, investigating the coexistence of rising obesity and persistent malnutrition across 190+ countries from 2012 to 2022.
---

## 🎯 Problem Statement

As a data analyst for a global health organisation, the task is to investigate the **nutrition paradox** — why obesity rates are climbing globally while malnutrition in children and adults continues to persist, often **within the same countries**. Using publicly available WHO BMI indicator data, this project uncovers regional disparities, demographic vulnerabilities, and data-reliability gaps that can inform real public health intervention.

---

## 🖥️ Live Dashboard

The Streamlit app has **6 fully interactive pages**:

| Page | What it shows |
|------|--------------|
| 🏠 Overview | KPI metrics, dual-trend line, paradox scatter, world maps |
| 📊 EDA | Distribution checks, box plots, gender gaps, CI-width heatmaps |
| 🔴 Obesity Queries | All 10 SQL queries with charts + glowing insight boxes |
| 🔵 Malnutrition Queries | All 10 SQL queries with charts + glowing insight boxes |
| 🔗 Combined Queries | 5 JOIN queries revealing dual-burden countries |
| 🌍 Country Deep-Dive | Interactive per-country profile with dynamic health alerts |

---

## 📁 Project Structure

```
NUTRITION_PARADOX/
│
├── app/
│   ├── sql/
│   │   └── queries.py          # All 25 SQL queries + QUERY_META (chart type, insight text)
│   ├── streamlit_app.py        # Main Streamlit dashboard 
│   ├── db_utils.py             # SQLite connection, cached loaders, KPI stats
│   └── viz_utils.py            # 13 reusable Plotly chart functions
│
├── data/
│   ├── raw/                    # Cached WHO API JSON responses
│   └── processed/              # Cleaned CSVs (obesity_clean.csv, malnutrition_clean.csv)
│
├── notebooks/
│   ├── data_collection_01.ipynb   # WHO API fetch + local cache
│   ├── cleaning_eda_02.ipynb      # Cleaning, pycountry conversion, EDA visualisations
│   └── sql_queries_03.ipynb       # All 25 query outputs with charts
│
├── nutrition.db                # SQLite database (obesity + malnutrition tables)
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🔬 Data Sources

| Indicator | WHO API Endpoint | Coverage |
|-----------|-----------------|---------|
| Adult obesity (BMI ≥ 30) | `NCD_BMI_30C` | Adults, by country/sex/year |
| Child overweight (BMI +2SD) | `NCD_BMI_PLUS2C` | Children/adolescents |
| Adult underweight (BMI < 18.5) | `NCD_BMI_18C` | Adults, by country/sex/year |
| Child thinness (BMI −2SD) | `NCD_BMI_MINUS2C` | Children/adolescents |

- **Base URL:** `https://ghoapi.azureedge.net/api/`  
- **Period filtered:** 2012 – 2022  
- **Regions:** Africa, Americas, Europe, Eastern Mediterranean, South-East Asia, Western Pacific

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Data ingestion | Python `requests` + local JSON cache |
| Data cleaning | `pandas`, `pycountry` (ISO-3 → country name) |
| Storage | `SQLite` via `sqlite3` + `SQLAlchemy` |
| Analysis | `pandas`, `numpy` |
| Visualisation | `plotly.express`, `plotly.graph_objects`, `seaborn`, `matplotlib` |
| Dashboard | `Streamlit` |

---

## ⚙️ Setup & Installation

### 1 — Clone the repo
```bash
git clone https://github.com/ps-learner/nutrition_paradox.git
cd nutrition_paradox
```

### 2 — Create a virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3 — Install dependencies
```bash
pip install -r requirements.txt
```

### 4 — Collect & clean data (run once)
```bash
# Open and run all cells in order:
notebooks/data_collection_01.ipynb
notebooks/cleaning_eda_02.ipynb
```
This fetches the 4 WHO API endpoints, cleans the data, and writes `nutrition.db` to the project root.

### 5 — Run all 25 SQL queries (optional notebook)
```bash
notebooks/sql_queries_03.ipynb
```

### 6 — Launch the Streamlit dashboard
```bash
streamlit run app/streamlit_app.py
```
Open `http://localhost:8501` in your browser.

---

## 🗄️ Database Schema

### `obesity` table
| Column | Type | Description |
|--------|------|-------------|
| Year | INTEGER | Year of data collection (2012–2022) |
| Gender | TEXT | Male / Female / Both |
| Mean_Estimate | REAL | Estimated obesity % |
| LowerBound | REAL | Lower confidence interval bound |
| UpperBound | REAL | Upper confidence interval bound |
| Age_Group | TEXT | Adult or Child/Adolescent |
| Country | TEXT | Full country name (ISO-3 converted) |
| Region | TEXT | WHO region |
| CI_Width | REAL | UpperBound − LowerBound |
| Obesity_Level | TEXT | High (≥30%) / Moderate (25–29.9%) / Low (<25%) |

### `malnutrition` table
Same structure, with `Malnutrition_Level` instead of `Obesity_Level`:  
High (≥20%) / Moderate (10–19.9%) / Low (<10%)

---

## 📊 SQL Queries — Summary

### 🔴 Obesity (Q1–Q10)
| # | Query |
|---|-------|
| Q1 | Top 5 regions — highest avg obesity (2022) |
| Q2 | Top 5 countries — highest obesity estimate |
| Q3 | Obesity trend in India over the years |
| Q4 | Average obesity by gender |
| Q5 | Country count by obesity level & age group |
| Q6 | Least reliable vs most consistent countries (CI Width) |
| Q7 | Average obesity by age group |
| Q8 | Top 10 consistent low-obesity countries |
| Q9 | Countries where female obesity exceeds male by 5+ points |
| Q10 | Global average obesity percentage per year |

### 🔵 Malnutrition (Q11–Q20)
| # | Query |
|---|-------|
| Q11 | Avg malnutrition by age group |
| Q12 | Top 5 countries — highest malnutrition |
| Q13 | Africa malnutrition trend over years |
| Q14 | Average malnutrition by gender |
| Q15 | Avg CI Width by malnutrition level & age group |
| Q16 | India vs Nigeria vs Brazil — malnutrition trend |
| Q17 | Regions with lowest malnutrition averages |
| Q18 | Countries with increasing malnutrition |
| Q19 | Min / Max malnutrition year-wise comparison |
| Q20 | High CI Width monitoring flags (CI > 5) |

### 🔗 Combined JOIN Queries (Q21–Q25)
| # | Query |
|---|-------|
| Q21 | Obesity vs malnutrition — 5 key countries side-by-side |
| Q22 | Gender disparity across both conditions |
| Q23 | Africa vs Americas — regional comparison |
| Q24 | Countries where obesity rises AND malnutrition falls |
| Q25 | Age-wise trend across both conditions |

---

## 💡 Key Findings

### 1. The Dual Burden is Real
Over **80 countries** record both obesity rates above 10% and malnutrition rates above 10% simultaneously — disproving the assumption that these are mutually exclusive problems.

### 2. Global Obesity is Rising Without Pause
Every year from 2012 to 2022 shows a higher global average obesity rate. There is **no plateau** — the trend is unbroken.

### 3. Women Bear a Disproportionate Burden
Female obesity exceeds male obesity in every WHO region. In parts of Africa and the Middle East, the gap exceeds **15 percentage points** — driven by unequal physical activity, food access, and socioeconomic factors.

### 4. Data Quality is Worst Where It Matters Most
Countries with the highest malnutrition also have the widest confidence intervals (CI Width). The **most urgent intervention targets are the least reliably measured** — a systemic gap in global health surveillance.

### 5. The Nutritional Transition Is Accelerating
Countries like India, Indonesia, and Nigeria are simultaneously reducing undernutrition and growing obesity — driven by the global spread of cheap, calorie-dense, nutrient-poor processed foods.

### 6. Brazil Demonstrates What Policy Can Do
Brazil shows the largest malnutrition decline in the dataset alongside a moderate obesity rise — directly attributable to sustained social protection programmes (Bolsa Família, school feeding). It is a proof-of-concept for targeted intervention.

---

## 📈 EDA Visualisations Included

1. Global obesity trend line (2012–2022)
2. Global malnutrition trend line (2012–2022)
3. Dual-overlay trend (obesity vs malnutrition)
4. Top 10 countries — obesity horizontal bar
5. Top 10 countries — malnutrition horizontal bar
6. Regional box plots (spread and outliers)
7. Gender gap grouped bar — by region
8. Adults vs Children bar — both conditions
9. CI Width heatmap — region × age group
10. **Paradox scatter** — every country as a dot (obesity x-axis, malnutrition y-axis)
11. Obesity level donut chart (High/Moderate/Low)
12. Choropleth world maps — obesity and malnutrition side-by-side

---

## 🏗️ Architecture Decisions

**Why SQLite?**  
Zero-configuration, file-based, and fully portable. The `nutrition.db` file can be committed alongside the code for instant reproducibility.

**Why `QUERY_META` instead of raw strings?**  
Each query in `queries.py` carries metadata (`chart_type`, `x`, `y`, `color_col`, `insight`) that drives the Streamlit chart builder automatically — no per-query if/else logic in the app. Adding a new query requires zero changes to `streamlit_app.py`.

**Why local JSON caching for API calls?**  
The WHO API is rate-limited and occasionally slow. Caching responses locally means the cleaning notebook runs instantly on subsequent executions without re-fetching 4 endpoints.

**Why `pycountry` for ISO conversion?**  
The WHO API returns ISO Alpha-3 codes (`IND`, `NGA`, `BRA`). `pycountry` converts these to full names used by Plotly's `locationmode="country names"` choropleth — enabling world maps with no manual mapping table.

---

## 📋 requirements.txt

```
pandas==2.2.1
requests==2.31.0
pycountry==23.12.11
sqlalchemy==2.0.29
plotly==5.20.0
seaborn==0.13.2
matplotlib==3.8.3
streamlit==1.32.2
numpy==1.26.4
```

---

## 🗂️ .gitignore

```
# Python
__pycache__/
*.pyc
.venv/
venv/
*.egg-info/

# Data (raw API cache — regenerate with notebook)
data/raw/

# Jupyter checkpoints
.ipynb_checkpoints/

# OS
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
```

---

## 📬 Contact

Built as part of the **GUVI AI-ML Programme** — Mini Project 2.

**Domain:** Global Health & Nutrition Analytics  
**Data:** WHO Global Health Observatory (GHO) API  
**Period:** 2012–2022  

---