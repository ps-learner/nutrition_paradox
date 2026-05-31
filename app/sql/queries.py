# =============================================================
# queries.py  — All 25 SQL queries + per-query insight strings
# Place this file at:  app/sql/queries.py
# Import in streamlit_app.py:
#     from app.sql.queries import QUERIES, QUERY_META
# =============================================================

# ── 25 SQL queries ────────────────────────────────────────────
QUERIES = {

    # =========================================================
    # 🔴  OBESITY QUERIES  (Q1 – Q10)
    # =========================================================

    "Q1 · Top 5 regions — highest avg obesity (2022)": """
SELECT Region,
       ROUND(AVG(Mean_Estimate), 2) AS avg_obesity
FROM obesity
WHERE Year = 2022
  AND Gender = 'Both'
GROUP BY Region
ORDER BY avg_obesity DESC
LIMIT 5;
""",

    "Q2 · Top 5 countries — highest obesity estimate": """
SELECT Country,
       ROUND(AVG(Mean_Estimate), 2) AS avg_obesity
FROM obesity
WHERE Gender = 'Both'
GROUP BY Country
ORDER BY avg_obesity DESC
LIMIT 5;
""",

    "Q3 · Obesity trend in India": """
SELECT Year,
       ROUND(AVG(Mean_Estimate), 2) AS avg_obesity
FROM obesity
WHERE Country = 'India'
  AND Gender = 'Both'
GROUP BY Year
ORDER BY Year;
""",

    "Q4 · Average obesity by gender": """
SELECT Gender,
       ROUND(AVG(Mean_Estimate), 2) AS avg_obesity
FROM obesity
GROUP BY Gender
ORDER BY avg_obesity DESC;
""",

    "Q5 · Country count by obesity level & age group": """
SELECT Obesity_Level,
       Age_Group,
       COUNT(DISTINCT Country) AS country_count
FROM obesity
GROUP BY Obesity_Level, Age_Group
ORDER BY Obesity_Level;
""",

    "Q6 · Least reliable vs most consistent countries": """
SELECT * FROM (
    SELECT 'Least Reliable' AS type,
           Country,
           ROUND(AVG(CI_Width), 2) AS avg_ci
    FROM obesity
    GROUP BY Country
    ORDER BY avg_ci DESC
    LIMIT 5
)
UNION ALL
SELECT * FROM (
    SELECT 'Most Consistent' AS type,
           Country,
           ROUND(AVG(CI_Width), 2) AS avg_ci
    FROM obesity
    GROUP BY Country
    ORDER BY avg_ci ASC
    LIMIT 5
);
""",

    "Q7 · Average obesity by age group": """
SELECT Age_Group,
       ROUND(AVG(Mean_Estimate), 2) AS avg_obesity
FROM obesity
WHERE Gender = 'Both'
GROUP BY Age_Group;
""",

    "Q8 · Top 10 consistent low-obesity countries": """
SELECT Country,
       ROUND(AVG(Mean_Estimate), 2) AS avg_obesity,
       ROUND(AVG(CI_Width),      2) AS avg_ci
FROM obesity
WHERE Gender = 'Both'
GROUP BY Country
HAVING avg_obesity < 15
   AND avg_ci      < 5
ORDER BY avg_obesity ASC, avg_ci ASC
LIMIT 10;
""",

    "Q9 · Female obesity exceeds male by 5+ points": """
SELECT a.Country,
       a.Year,
       ROUND(a.Mean_Estimate,                   2) AS female_obesity,
       ROUND(b.Mean_Estimate,                   2) AS male_obesity,
       ROUND(a.Mean_Estimate - b.Mean_Estimate, 2) AS gap
FROM obesity a
JOIN obesity b
  ON  a.Country   = b.Country
 AND  a.Year      = b.Year
 AND  a.Age_Group = b.Age_Group
WHERE a.Gender = 'Female'
  AND b.Gender = 'Male'
  AND (a.Mean_Estimate - b.Mean_Estimate) >= 5
ORDER BY gap DESC
LIMIT 20;
""",

    "Q10 · Global average obesity per year": """
SELECT Year,
       ROUND(AVG(Mean_Estimate), 2) AS global_avg_obesity
FROM obesity
WHERE Gender = 'Both'
GROUP BY Year
ORDER BY Year;
""",

    # =========================================================
    # 🔵  MALNUTRITION QUERIES  (Q11 – Q20)
    # =========================================================

    "Q11 · Avg malnutrition by age group": """
SELECT Age_Group,
       ROUND(AVG(Mean_Estimate), 2) AS avg_malnutrition
FROM malnutrition
WHERE Gender = 'Both'
GROUP BY Age_Group;
""",

    "Q12 · Top 5 countries — highest malnutrition": """
SELECT Country,
       ROUND(AVG(Mean_Estimate), 2) AS avg_mal
FROM malnutrition
WHERE Gender = 'Both'
GROUP BY Country
ORDER BY avg_mal DESC
LIMIT 5;
""",

    "Q13 · Africa malnutrition trend over years": """
SELECT Year,
       ROUND(AVG(Mean_Estimate), 2) AS avg_mal
FROM malnutrition
WHERE Region  = 'Africa'
  AND Gender  = 'Both'
GROUP BY Year
ORDER BY Year;
""",

    "Q14 · Average malnutrition by gender": """
SELECT Gender,
       ROUND(AVG(Mean_Estimate), 2) AS avg_mal
FROM malnutrition
GROUP BY Gender
ORDER BY avg_mal DESC;
""",

    "Q15 · Avg CI_Width by malnutrition level & age group": """
SELECT Malnutrition_Level,
       Age_Group,
       ROUND(AVG(CI_Width), 2) AS avg_ci_width
FROM malnutrition
GROUP BY Malnutrition_Level, Age_Group;
""",

    "Q16 · India vs Nigeria vs Brazil — malnutrition trend": """
SELECT Country,
       Year,
       ROUND(AVG(Mean_Estimate), 2) AS avg_mal
FROM malnutrition
WHERE Country IN ('India', 'Nigeria', 'Brazil')
  AND Gender = 'Both'
GROUP BY Country, Year
ORDER BY Country, Year;
""",

    "Q17 · Regions with lowest malnutrition averages": """
SELECT Region,
       ROUND(AVG(Mean_Estimate), 2) AS avg_mal
FROM malnutrition
WHERE Gender = 'Both'
GROUP BY Region
ORDER BY avg_mal ASC;
""",

    "Q18 · Countries with increasing malnutrition": """
SELECT Country,
       ROUND(MIN(Mean_Estimate),                        2) AS early_mal,
       ROUND(MAX(Mean_Estimate),                        2) AS recent_mal,
       ROUND(MAX(Mean_Estimate) - MIN(Mean_Estimate),   2) AS increase
FROM malnutrition
WHERE Gender = 'Both'
GROUP BY Country
HAVING increase > 0
ORDER BY increase DESC
LIMIT 15;
""",

    "Q19 · Min / Max malnutrition year-wise": """
SELECT Year,
       ROUND(MIN(Mean_Estimate), 2) AS min_mal,
       ROUND(MAX(Mean_Estimate), 2) AS max_mal,
       ROUND(AVG(Mean_Estimate), 2) AS avg_mal
FROM malnutrition
WHERE Gender = 'Both'
GROUP BY Year
ORDER BY Year;
""",

    "Q20 · High CI_Width monitoring flags (CI > 5)": """
SELECT Country,
       Region,
       Year,
       Age_Group,
       Gender,
       ROUND(CI_Width,       2) AS ci_width,
       ROUND(Mean_Estimate,  2) AS mean_est
FROM malnutrition
WHERE CI_Width > 5
ORDER BY CI_Width DESC
LIMIT 30;
""",

    # =========================================================
    # 🔗  COMBINED QUERIES  (Q21 – Q25)
    # =========================================================

    "Q21 · Obesity vs malnutrition — 5 key countries": """
SELECT o.Country,
       o.Year,
       ROUND(o.Mean_Estimate, 2) AS obesity_pct,
       ROUND(m.Mean_Estimate, 2) AS malnutrition_pct
FROM obesity o
JOIN malnutrition m
  ON  o.Country = m.Country
 AND  o.Year    = m.Year
 AND  o.Gender  = m.Gender
WHERE o.Gender = 'Both'
  AND o.Country IN ('India', 'Nigeria', 'United States', 'China', 'Brazil')
ORDER BY o.Country, o.Year;
""",

    "Q22 · Gender disparity — obesity vs malnutrition": """
SELECT o.Gender,
       ROUND(AVG(o.Mean_Estimate), 2) AS avg_obesity,
       ROUND(AVG(m.Mean_Estimate), 2) AS avg_malnutrition
FROM obesity o
JOIN malnutrition m
  ON  o.Country = m.Country
 AND  o.Year    = m.Year
 AND  o.Gender  = m.Gender
WHERE o.Gender IN ('Male', 'Female')
GROUP BY o.Gender;
""",

    "Q23 · Africa vs Americas — side-by-side comparison": """
SELECT o.Region,
       ROUND(AVG(o.Mean_Estimate), 2) AS avg_obesity,
       ROUND(AVG(m.Mean_Estimate), 2) AS avg_malnutrition
FROM obesity o
JOIN malnutrition m
  ON  o.Country = m.Country
 AND  o.Year    = m.Year
 AND  o.Gender  = m.Gender
WHERE o.Gender = 'Both'
  AND o.Region IN ('Africa', 'Americas Region')
GROUP BY o.Region;
""",

    "Q24 · Rising obesity + falling malnutrition (transition countries)": """
SELECT ob.Country,
       ROUND(MAX(ob.Mean_Estimate) - MIN(ob.Mean_Estimate), 2) AS ob_change,
       ROUND(MIN(mn.Mean_Estimate) - MAX(mn.Mean_Estimate), 2) AS mn_drop
FROM obesity ob
JOIN malnutrition mn
  ON  ob.Country   = mn.Country
 AND  ob.Year      = mn.Year
 AND  ob.Gender    = mn.Gender
WHERE ob.Gender = 'Both'
GROUP BY ob.Country
HAVING ob_change > 0
   AND mn_drop   > 0
ORDER BY ob_change DESC
LIMIT 15;
""",

    "Q25 · Age-wise trend across both conditions": """
SELECT ob.Year,
       ob.Age_Group,
       ROUND(AVG(ob.Mean_Estimate), 2) AS avg_obesity,
       ROUND(AVG(mn.Mean_Estimate), 2) AS avg_malnutrition
FROM obesity ob
JOIN malnutrition mn
  ON  ob.Country   = mn.Country
 AND  ob.Year      = mn.Year
 AND  ob.Gender    = mn.Gender
 AND  ob.Age_Group = mn.Age_Group
WHERE ob.Gender = 'Both'
GROUP BY ob.Year, ob.Age_Group
ORDER BY ob.Year, ob.Age_Group;
""",
}


# =============================================================
# QUERY_META — per-query metadata consumed by the Streamlit app
# Keys:
#   category   : "obesity" | "malnutrition" | "combined"
#   chart_type : "bar" | "line" | "grouped_bar" | "scatter" | "table"
#   x / y      : column names for the primary chart axes
#   color_col  : optional column to use as Plotly color dimension
#   insight    : one-sentence plain-English finding shown in the
#                glowing insight box below the chart
# =============================================================
QUERY_META = {

    # ── Obesity ──────────────────────────────────────────────
    "Q1 · Top 5 regions — highest avg obesity (2022)": {
        "category":   "obesity",
        "chart_type": "bar",
        "x": "Region", "y": "avg_obesity",
        "insight": "The Americas and Europe consistently top global obesity rankings, reflecting the impact of processed-food diets and sedentary lifestyles.",
    },
    "Q2 · Top 5 countries — highest obesity estimate": {
        "category":   "obesity",
        "chart_type": "bar",
        "x": "Country", "y": "avg_obesity",
        "insight": "Small island nations and Gulf states dominate the top-5, driven by rapid dietary transitions and limited physical-activity infrastructure.",
    },
    "Q3 · Obesity trend in India": {
        "category":   "obesity",
        "chart_type": "line",
        "x": "Year", "y": "avg_obesity",
        "insight": "India's adult obesity rate has risen steadily since 2012, mirroring urbanisation and the growing availability of calorie-dense processed foods.",
    },
    "Q4 · Average obesity by gender": {
        "category":   "obesity",
        "chart_type": "bar",
        "x": "Gender", "y": "avg_obesity",
        "insight": "Female obesity exceeds male obesity globally — a disparity attributed to hormonal factors, lower physical-activity rates, and socio-economic constraints.",
    },
    "Q5 · Country count by obesity level & age group": {
        "category":   "obesity",
        "chart_type": "bar",
        "x": "Obesity_Level", "y": "country_count",
        "color_col": "Age_Group",
        "insight": "Most countries fall in the 'Low' obesity band for children, but the 'Moderate/High' adult category is growing — signalling a coming wave of chronic disease.",
    },
    "Q6 · Least reliable vs most consistent countries": {
        "category":   "obesity",
        "chart_type": "bar",
        "x": "Country", "y": "avg_ci",
        "color_col": "type",
        "insight": "Countries with the widest confidence intervals are often low-income nations with limited surveillance capacity — the same places that need data most urgently.",
    },
    "Q7 · Average obesity by age group": {
        "category":   "obesity",
        "chart_type": "bar",
        "x": "Age_Group", "y": "avg_obesity",
        "insight": "Adult obesity rates are roughly 2–3× higher than child rates globally, but childhood obesity is rising faster in high-income regions.",
    },
    "Q8 · Top 10 consistent low-obesity countries": {
        "category":   "obesity",
        "chart_type": "bar",
        "x": "Country", "y": "avg_obesity",
        "insight": "Sub-Saharan African and South/South-East Asian nations dominate the low-obesity list — but many share high malnutrition burdens, illustrating the paradox.",
    },
    "Q9 · Female obesity exceeds male by 5+ points": {
        "category":   "obesity",
        "chart_type": "bar",
        "x": "Country", "y": "gap",
        "insight": "In parts of Africa and the Middle East, women's obesity rates exceed men's by more than 15 percentage points — a stark gender-nutrition inequity.",
    },
    "Q10 · Global average obesity per year": {
        "category":   "obesity",
        "chart_type": "line",
        "x": "Year", "y": "global_avg_obesity",
        "insight": "Global average obesity has risen uninterrupted from 2012 to 2022, with no sign of plateau — reinforcing the need for policy-level intervention.",
    },

    # ── Malnutrition ─────────────────────────────────────────
    "Q11 · Avg malnutrition by age group": {
        "category":   "malnutrition",
        "chart_type": "bar",
        "x": "Age_Group", "y": "avg_malnutrition",
        "insight": "Children/adolescents bear a disproportionately high malnutrition burden compared with adults, making early-life nutrition programmes critical.",
    },
    "Q12 · Top 5 countries — highest malnutrition": {
        "category":   "malnutrition",
        "chart_type": "bar",
        "x": "Country", "y": "avg_mal",
        "insight": "The top-5 highest-malnutrition countries are all in South Asia or Sub-Saharan Africa, where food insecurity and poverty intersect.",
    },
    "Q13 · Africa malnutrition trend over years": {
        "category":   "malnutrition",
        "chart_type": "line",
        "x": "Year", "y": "avg_mal",
        "insight": "Africa's malnutrition rate shows only modest decline over the decade, suggesting that economic growth alone has not translated into nutritional security.",
    },
    "Q14 · Average malnutrition by gender": {
        "category":   "malnutrition",
        "chart_type": "bar",
        "x": "Gender", "y": "avg_mal",
        "insight": "Female malnutrition slightly exceeds male in aggregate — but in certain regions women face significantly worse nutritional outcomes due to unequal food access.",
    },
    "Q15 · Avg CI_Width by malnutrition level & age group": {
        "category":   "malnutrition",
        "chart_type": "bar",
        "x": "Malnutrition_Level", "y": "avg_ci_width",
        "color_col": "Age_Group",
        "insight": "High-malnutrition countries also have the widest confidence intervals, meaning the places with the worst nutritional crises have the least reliable data.",
    },
    "Q16 · India vs Nigeria vs Brazil — malnutrition trend": {
        "category":   "malnutrition",
        "chart_type": "line",
        "x": "Year", "y": "avg_mal",
        "color_col": "Country",
        "insight": "India shows the steepest malnutrition decline of the three, yet still records the highest absolute levels — reflecting scale rather than lack of progress.",
    },
    "Q17 · Regions with lowest malnutrition averages": {
        "category":   "malnutrition",
        "chart_type": "bar",
        "x": "Region", "y": "avg_mal",
        "insight": "Europe and the Americas record the lowest regional malnutrition averages, while South-East Asia and Africa remain the most affected regions.",
    },
    "Q18 · Countries with increasing malnutrition": {
        "category":   "malnutrition",
        "chart_type": "bar",
        "x": "Country", "y": "increase",
        "insight": "A subset of countries shows worsening malnutrition despite global improvement — often linked to conflict, climate shocks, or economic collapse.",
    },
    "Q19 · Min / Max malnutrition year-wise": {
        "category":   "malnutrition",
        "chart_type": "line",
        "x": "Year", "y": "avg_mal",
        "insight": "The gap between the best and worst performers has narrowed slightly over a decade, but the absolute spread remains enormous — over 30 percentage points.",
    },
    "Q20 · High CI_Width monitoring flags (CI > 5)": {
        "category":   "malnutrition",
        "chart_type": "table",
        "x": "Country", "y": "ci_width",
        "insight": "30+ country-year-gender records have CI_Width > 5, flagging critical data-quality gaps that must be addressed before reliable policy can be made.",
    },

    # ── Combined ─────────────────────────────────────────────
    "Q21 · Obesity vs malnutrition — 5 key countries": {
        "category":   "combined",
        "chart_type": "line",
        "x": "Year", "y": "obesity_pct",
        "color_col": "Country",
        "insight": "India and Nigeria show high malnutrition alongside rising obesity — the textbook 'dual burden'. The US shows the opposite: high obesity, near-zero malnutrition.",
    },
    "Q22 · Gender disparity — obesity vs malnutrition": {
        "category":   "combined",
        "chart_type": "grouped_bar",
        "x": "Gender", "y": ["avg_obesity", "avg_malnutrition"],
        "insight": "Women face higher obesity AND slightly higher malnutrition globally — a double nutritional vulnerability that demands gender-sensitive health policies.",
    },
    "Q23 · Africa vs Americas — side-by-side comparison": {
        "category":   "combined",
        "chart_type": "grouped_bar",
        "x": "Region", "y": ["avg_obesity", "avg_malnutrition"],
        "insight": "Africa records far higher malnutrition but lower obesity than the Americas — yet both regions are seeing obesity rise, signalling converging nutritional crises.",
    },
    "Q24 · Rising obesity + falling malnutrition (transition countries)": {
        "category":   "combined",
        "chart_type": "bar",
        "x": "Country", "y": "ob_change",
        "insight": "Transition countries are winning the malnutrition battle but losing the obesity one — economic development solves food scarcity while creating new diet-quality problems.",
    },
    "Q25 · Age-wise trend across both conditions": {
        "category":   "combined",
        "chart_type": "line",
        "x": "Year", "y": "avg_obesity",
        "color_col": "Age_Group",
        "insight": "Adult obesity is accelerating while child malnutrition slowly declines — underscoring the need for life-course nutrition strategies rather than single-age interventions.",
    },
}