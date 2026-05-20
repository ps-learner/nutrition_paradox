"""
viz_utils.py — Reusable chart functions for the Nutrition Paradox Streamlit app.

Import in streamlit_app.py:
    from viz_utils import (
        plot_global_trend, plot_top_countries, plot_gender_gap,
        plot_region_boxplot, plot_paradox_scatter, plot_heatmap,
        plot_ci_width, plot_country_comparison, plot_age_group_bar,
        plot_grouped_bar
    )
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# ── Color palette (consistent across all charts) ────────────────────────
OBESITY_COLOR      = "#E24B4A"
MALNUTRITION_COLOR = "#378ADD"
MALE_COLOR         = "#378ADD"
FEMALE_COLOR       = "#D85A30"
BOTH_COLOR         = "#1D9E75"
ADULT_COLOR        = "#534AB7"
CHILD_COLOR        = "#BA7517"

REGION_COLORS = px.colors.qualitative.Set2   # 8 distinct colors for regions


# ── 1. Global trend line (single condition) ─────────────────────────────
def plot_global_trend(df: pd.DataFrame, condition: str = "Obesity") -> go.Figure:
    """
    Line chart: global average Mean_Estimate per year.
    df must have columns: Year, Mean_Estimate, Gender.
    condition: 'Obesity' or 'Malnutrition' — affects title and color.
    """
    color = OBESITY_COLOR if condition == "Obesity" else MALNUTRITION_COLOR
    trend = (
        df[df["Gender"] == "Both"]
        .groupby("Year")["Mean_Estimate"]
        .mean()
        .reset_index()
    )
    fig = px.line(
        trend, x="Year", y="Mean_Estimate",
        markers=True,
        title=f"Global Average {condition} Trend (2012–2022)",
        labels={"Mean_Estimate": f"Avg {condition} (%)"},
        color_discrete_sequence=[color],
    )
    fig.update_traces(line_width=2.5, marker_size=7)
    fig.update_layout(template="plotly_white", hovermode="x unified")
    return fig


# ── 2. Dual-line: obesity vs malnutrition on same chart ─────────────────
def plot_dual_trend(df_ob: pd.DataFrame, df_mn: pd.DataFrame) -> go.Figure:
    """
    Overlay obesity and malnutrition global trends on one chart.
    The 'paradox' trend line — great for the Overview page.
    """
    ob = df_ob[df_ob["Gender"] == "Both"].groupby("Year")["Mean_Estimate"].mean().reset_index()
    mn = df_mn[df_mn["Gender"] == "Both"].groupby("Year")["Mean_Estimate"].mean().reset_index()
    fig = go.Figure()
    fig.add_scatter(
        x=ob["Year"], y=ob["Mean_Estimate"],
        name="Obesity", line=dict(color=OBESITY_COLOR, width=2.5),
        mode="lines+markers", marker_size=7,
    )
    fig.add_scatter(
        x=mn["Year"], y=mn["Mean_Estimate"],
        name="Malnutrition", line=dict(color=MALNUTRITION_COLOR, width=2.5),
        mode="lines+markers", marker_size=7,
    )
    fig.update_layout(
        title="Global Obesity vs Malnutrition — 2012 to 2022",
        xaxis_title="Year",
        yaxis_title="Global Average (%)",
        template="plotly_white",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig


# ── 3. Top N countries — horizontal bar ─────────────────────────────────
def plot_top_countries(
    df: pd.DataFrame,
    n: int = 10,
    condition: str = "Obesity",
    year: int = None,
    age_group: str = None,
) -> go.Figure:
    """
    Horizontal bar chart of top N countries by mean estimate.
    Optionally filter by year and/or age_group.
    """
    color = OBESITY_COLOR if condition == "Obesity" else MALNUTRITION_COLOR
    filtered = df[df["Gender"] == "Both"].copy()
    if year:
        filtered = filtered[filtered["Year"] == year]
    if age_group:
        filtered = filtered[filtered["Age_Group"] == age_group]
    top = (
        filtered.groupby("Country")["Mean_Estimate"]
        .mean()
        .nlargest(n)
        .reset_index()
        .sort_values("Mean_Estimate")   # ascending so highest is at top in h-bar
    )
    year_label = f" ({year})" if year else " (2012–2022 avg)"
    age_label  = f" · {age_group}" if age_group else ""
    fig = px.bar(
        top, x="Mean_Estimate", y="Country",
        orientation="h",
        title=f"Top {n} Countries by {condition}{age_label}{year_label}",
        labels={"Mean_Estimate": f"{condition} (%)"},
        color="Mean_Estimate",
        color_continuous_scale=["#FAEEDA", color],
    )
    fig.update_layout(template="plotly_white", coloraxis_showscale=False)
    return fig


# ── 4. Gender gap bar chart ──────────────────────────────────────────────
def plot_gender_gap(df: pd.DataFrame, condition: str = "Obesity") -> go.Figure:
    """
    Grouped bar: Male vs Female average per region.
    """
    filtered = df[df["Gender"].isin(["Male", "Female"])].copy()
    grouped  = (
        filtered.groupby(["Region", "Gender"])["Mean_Estimate"]
        .mean()
        .reset_index()
    )
    fig = px.bar(
        grouped, x="Region", y="Mean_Estimate",
        color="Gender", barmode="group",
        title=f"{condition} by Region and Gender",
        labels={"Mean_Estimate": f"Avg {condition} (%)"},
        color_discrete_map={"Male": MALE_COLOR, "Female": FEMALE_COLOR},
    )
    fig.update_layout(
        template="plotly_white",
        xaxis_tickangle=-30,
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
    )
    return fig


# ── 5. Box plot — spread by region ──────────────────────────────────────
def plot_region_boxplot(df: pd.DataFrame, condition: str = "Obesity") -> go.Figure:
    """
    Box plot showing distribution of Mean_Estimate across countries per region.
    Reveals outliers and variability at a glance.
    """
    filtered = df[df["Gender"] == "Both"].copy()
    fig = px.box(
        filtered, x="Region", y="Mean_Estimate",
        color="Region",
        title=f"{condition} Spread by WHO Region",
        labels={"Mean_Estimate": f"{condition} (%)"},
        color_discrete_sequence=REGION_COLORS,
    )
    fig.update_layout(
        template="plotly_white",
        xaxis_tickangle=-30,
        showlegend=False,
    )
    return fig


# ── 6. Paradox scatter — obesity vs malnutrition per country ────────────
def plot_paradox_scatter(
    df_ob: pd.DataFrame,
    df_mn: pd.DataFrame,
    year: int = 2022,
) -> go.Figure:
    """
    The headline chart. Each dot is a country; x=obesity, y=malnutrition.
    Quadrants reveal the 'dual burden' countries (top-right).
    """
    ob = (
        df_ob[(df_ob["Gender"] == "Both") & (df_ob["Year"] == year)]
        .groupby(["Country", "Region"])["Mean_Estimate"]
        .mean()
        .reset_index(name="Obesity")
    )
    mn = (
        df_mn[(df_mn["Gender"] == "Both") & (df_mn["Year"] == year)]
        .groupby("Country")["Mean_Estimate"]
        .mean()
        .reset_index(name="Malnutrition")
    )
    merged = ob.merge(mn, on="Country").dropna()

    # quadrant reference lines
    ob_med = merged["Obesity"].median()
    mn_med = merged["Malnutrition"].median()

    fig = px.scatter(
        merged, x="Obesity", y="Malnutrition",
        color="Region", hover_name="Country",
        size_max=12,
        title=f"The Nutrition Paradox — Obesity vs Malnutrition by Country ({year})",
        labels={"Obesity": "Obesity (%)", "Malnutrition": "Malnutrition (%)"},
        color_discrete_sequence=REGION_COLORS,
    )
    # Quadrant lines
    fig.add_hline(y=mn_med, line_dash="dot", line_color="gray", opacity=0.5)
    fig.add_vline(x=ob_med, line_dash="dot", line_color="gray", opacity=0.5)
    # Quadrant labels
    fig.add_annotation(x=merged["Obesity"].max() * 0.9, y=merged["Malnutrition"].max() * 0.9,
                       text="Dual Burden", showarrow=False, font=dict(color="#E24B4A", size=11))
    fig.add_annotation(x=merged["Obesity"].max() * 0.9, y=merged["Malnutrition"].min() * 1.2,
                       text="High Obesity", showarrow=False, font=dict(color="#BA7517", size=11))
    fig.update_layout(template="plotly_white", hovermode="closest")
    return fig


# ── 7. Confidence interval heatmap ──────────────────────────────────────
def plot_ci_heatmap(df: pd.DataFrame, condition: str = "Obesity") -> go.Figure:
    """
    Heatmap: average CI_Width per Region × Age_Group.
    Highlights where data is least reliable.
    """
    pivot = (
        df.groupby(["Region", "Age_Group"])["CI_Width"]
        .mean()
        .unstack()
        .fillna(0)
        .round(2)
    )
    fig = go.Figure(
        data=go.Heatmap(
            z=pivot.values,
            x=pivot.columns.tolist(),
            y=pivot.index.tolist(),
            colorscale="YlOrRd",
            text=pivot.values,
            texttemplate="%{text:.1f}",
            hovertemplate="Region: %{y}<br>Age Group: %{x}<br>Avg CI Width: %{z:.2f}<extra></extra>",
        )
    )
    fig.update_layout(
        title=f"{condition} Data Reliability — Avg CI Width (Region × Age Group)",
        xaxis_title="Age Group",
        yaxis_title="Region",
        template="plotly_white",
    )
    return fig


# ── 8. Country trend comparison (multi-country line) ────────────────────
def plot_country_comparison(
    df: pd.DataFrame,
    countries: list,
    condition: str = "Obesity",
) -> go.Figure:
    """
    Multi-line chart comparing selected countries over time.
    countries: list of country name strings.
    """
    filtered = df[
        df["Country"].isin(countries) & (df["Gender"] == "Both")
    ].groupby(["Country", "Year"])["Mean_Estimate"].mean().reset_index()

    fig = px.line(
        filtered, x="Year", y="Mean_Estimate",
        color="Country", markers=True,
        title=f"{condition} Trend: " + ", ".join(countries),
        labels={"Mean_Estimate": f"{condition} (%)"},
    )
    fig.update_layout(
        template="plotly_white",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
    )
    return fig


# ── 9. Age group comparison bar ─────────────────────────────────────────
def plot_age_group_bar(df: pd.DataFrame, condition: str = "Obesity") -> go.Figure:
    """
    Simple bar: average Mean_Estimate for Adults vs Children/Adolescents.
    """
    grouped = (
        df[df["Gender"] == "Both"]
        .groupby("Age_Group")["Mean_Estimate"]
        .mean()
        .reset_index()
    )
    fig = px.bar(
        grouped, x="Age_Group", y="Mean_Estimate",
        title=f"Average {condition}: Adults vs Children/Adolescents",
        labels={"Mean_Estimate": f"Avg {condition} (%)"},
        color="Age_Group",
        color_discrete_map={"Adult": ADULT_COLOR, "Child/Adolescent": CHILD_COLOR},
    )
    fig.update_layout(template="plotly_white", showlegend=False)
    return fig


# ── 10. Side-by-side obesity vs malnutrition grouped bar ─────────────────
def plot_grouped_bar(
    df_ob: pd.DataFrame,
    df_mn: pd.DataFrame,
    group_col: str = "Region",
) -> go.Figure:
    """
    Grouped bar comparing obesity and malnutrition averages
    across a categorical dimension (Region, Gender, Age_Group).
    """
    ob = (
        df_ob[df_ob["Gender"] == "Both"]
        .groupby(group_col)["Mean_Estimate"]
        .mean()
        .reset_index(name="Obesity")
    )
    mn = (
        df_mn[df_mn["Gender"] == "Both"]
        .groupby(group_col)["Mean_Estimate"]
        .mean()
        .reset_index(name="Malnutrition")
    )
    merged = ob.merge(mn, on=group_col).sort_values("Obesity", ascending=False)

    fig = go.Figure(data=[
        go.Bar(name="Obesity",      x=merged[group_col], y=merged["Obesity"],
               marker_color=OBESITY_COLOR),
        go.Bar(name="Malnutrition", x=merged[group_col], y=merged["Malnutrition"],
               marker_color=MALNUTRITION_COLOR),
    ])
    fig.update_layout(
        barmode="group",
        title=f"Obesity vs Malnutrition by {group_col}",
        xaxis_title=group_col,
        yaxis_title="Average (%)",
        xaxis_tickangle=-30,
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
    )
    return fig


# ── 11. Obesity level pie / donut ────────────────────────────────────────
def plot_level_pie(df: pd.DataFrame, level_col: str, condition: str = "Obesity") -> go.Figure:
    """
    Donut chart: proportion of records in each level (High/Moderate/Low).
    level_col: 'Obesity_Level' or 'Malnutrition_Level'
    """
    counts = df[level_col].value_counts().reset_index()
    counts.columns = ["Level", "Count"]
    colors = {"High": "#E24B4A", "Moderate": "#EF9F27", "Low": "#1D9E75"}
    fig = px.pie(
        counts, names="Level", values="Count",
        hole=0.45,
        title=f"{condition} Level Distribution",
        color="Level",
        color_discrete_map=colors,
    )
    fig.update_traces(textinfo="percent+label")
    fig.update_layout(template="plotly_white", showlegend=True)
    return fig


# ── 12. Choropleth world map ──────────────────────────────────────────────
def plot_choropleth(
    df: pd.DataFrame,
    condition: str = "Obesity",
    year: int = 2022,
) -> go.Figure:
    """
    World choropleth map coloured by Mean_Estimate.
    Requires the raw ISO-3 country codes; re-joins on Country name if needed.
    Best used if you preserve the original SpatialDim column as 'ISO3'.
    """
    filtered = df[
        (df["Gender"] == "Both") & (df["Year"] == year)
    ].groupby("Country")["Mean_Estimate"].mean().reset_index()

    color = "Reds" if condition == "Obesity" else "Blues"
    fig = px.choropleth(
        filtered, locations="Country", locationmode="country names",
        color="Mean_Estimate",
        color_continuous_scale=color,
        title=f"Global {condition} Levels ({year})",
        labels={"Mean_Estimate": f"{condition} (%)"},
    )
    fig.update_layout(
        template="plotly_white",
        geo=dict(showframe=False, showcoastlines=True),
        margin=dict(l=0, r=0, t=50, b=0),
    )
    return fig