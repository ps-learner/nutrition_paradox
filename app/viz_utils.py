# # =============================================================
# # viz_utils.py — Reusable Plotly chart helpers
# # Place this file at:  app/viz_utils.py
# # Import in streamlit_app.py:
# #   from viz_utils import (
# #       plot_dual_trend, plot_top_countries, plot_gender_gap,
# #       plot_region_boxplot, plot_paradox_scatter, plot_ci_heatmap,
# #       plot_country_comparison, plot_age_group_bar, plot_grouped_bar,
# #       plot_level_pie, plot_choropleth, plot_min_max_band,
# #       auto_chart
# #   )
# # =============================================================

# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go

# # ── Brand colours (match the glowing-box CSS palette) ────────
# OBESITY_COLOR      = "#ef4444"   # red
# MALNUTRITION_COLOR = "#3b82f6"   # blue
# MALE_COLOR         = "#3b82f6"
# FEMALE_COLOR       = "#f59e0b"
# BOTH_COLOR         = "#10b981"
# ADULT_COLOR        = "#667eea"
# CHILD_COLOR        = "#f59e0b"
# LOW_COLOR          = "#10b981"
# MOD_COLOR          = "#f59e0b"
# HIGH_COLOR         = "#ef4444"

# REGION_PALETTE = px.colors.qualitative.Bold
# TEMPLATE       = "plotly_dark"   # dark bg matches glowing-box theme


# # =============================================================
# # EDA CHARTS (used on the EDA page)
# # =============================================================

# def plot_dual_trend(df_ob: pd.DataFrame, df_mn: pd.DataFrame) -> go.Figure:
#     """Overlay obesity + malnutrition global trends — the headline chart."""
#     ob = (df_ob[df_ob["Gender"] == "Both"]
#           .groupby("Year")["Mean_Estimate"].mean().reset_index())
#     mn = (df_mn[df_mn["Gender"] == "Both"]
#           .groupby("Year")["Mean_Estimate"].mean().reset_index())
#     fig = go.Figure()
#     fig.add_scatter(x=ob["Year"], y=ob["Mean_Estimate"],
#                     name="Obesity", mode="lines+markers",
#                     line=dict(color=OBESITY_COLOR, width=3),
#                     marker=dict(size=8))
#     fig.add_scatter(x=mn["Year"], y=mn["Mean_Estimate"],
#                     name="Malnutrition", mode="lines+markers",
#                     line=dict(color=MALNUTRITION_COLOR, width=3),
#                     marker=dict(size=8))
#     fig.update_layout(
#         title="🌍 Global Obesity vs Malnutrition Trend (2012–2022)",
#         xaxis_title="Year", yaxis_title="Global Average (%)",
#         template=TEMPLATE, hovermode="x unified",
#         legend=dict(orientation="h", y=1.1),
#     )
#     return fig


# def plot_top_countries(df: pd.DataFrame, n: int = 10,
#                        condition: str = "Obesity",
#                        year: int = None,
#                        age_group: str = None) -> go.Figure:
#     """Horizontal bar — top N countries by Mean_Estimate."""
#     color = OBESITY_COLOR if condition == "Obesity" else MALNUTRITION_COLOR
#     filt = df[df["Gender"] == "Both"].copy()
#     if year:      filt = filt[filt["Year"] == year]
#     if age_group: filt = filt[filt["Age_Group"] == age_group]
#     top = (filt.groupby("Country")["Mean_Estimate"].mean()
#                .nlargest(n).reset_index()
#                .sort_values("Mean_Estimate"))
#     suffix = f" ({year})" if year else " (2012–2022 avg)"
#     fig = px.bar(top, x="Mean_Estimate", y="Country", orientation="h",
#                  color="Mean_Estimate",
#                  color_continuous_scale=["#1a1a2e", color],
#                  title=f"Top {n} Countries by {condition}{suffix}",
#                  labels={"Mean_Estimate": f"{condition} (%)"})
#     fig.update_layout(template=TEMPLATE, coloraxis_showscale=False)
#     return fig


# def plot_gender_gap(df: pd.DataFrame, condition: str = "Obesity") -> go.Figure:
#     """Grouped bar — Male vs Female average per region."""
#     filt = df[df["Gender"].isin(["Male", "Female"])].copy()
#     grp  = (filt.groupby(["Region", "Gender"])["Mean_Estimate"]
#                 .mean().reset_index())
#     fig  = px.bar(grp, x="Region", y="Mean_Estimate",
#                   color="Gender", barmode="group",
#                   title=f"{condition} by Region and Gender",
#                   labels={"Mean_Estimate": f"Avg {condition} (%)"},
#                   color_discrete_map={"Male": MALE_COLOR,
#                                       "Female": FEMALE_COLOR})
#     fig.update_layout(template=TEMPLATE, xaxis_tickangle=-30,
#                       legend=dict(orientation="h", y=1.1))
#     return fig


# def plot_region_boxplot(df: pd.DataFrame,
#                         condition: str = "Obesity") -> go.Figure:
#     """Box plot — distribution of Mean_Estimate across countries per region."""
#     filt = df[df["Gender"] == "Both"].copy()
#     fig  = px.box(filt, x="Region", y="Mean_Estimate", color="Region",
#                   title=f"{condition} Spread by WHO Region",
#                   labels={"Mean_Estimate": f"{condition} (%)"},
#                   color_discrete_sequence=REGION_PALETTE)
#     fig.update_layout(template=TEMPLATE, xaxis_tickangle=-30,
#                       showlegend=False)
#     return fig


# def plot_paradox_scatter(df_ob: pd.DataFrame,
#                          df_mn: pd.DataFrame,
#                          year: int = 2022) -> go.Figure:
#     """
#     The flagship 'paradox' chart.
#     Each dot = one country; x=obesity, y=malnutrition.
#     Top-right quadrant = dual burden countries.
#     """
#     ob = (df_ob[(df_ob["Gender"] == "Both") & (df_ob["Year"] == year)]
#           .groupby(["Country", "Region"])["Mean_Estimate"]
#           .mean().reset_index(name="Obesity"))
#     mn = (df_mn[(df_mn["Gender"] == "Both") & (df_mn["Year"] == year)]
#           .groupby("Country")["Mean_Estimate"]
#           .mean().reset_index(name="Malnutrition"))
#     merged = ob.merge(mn, on="Country").dropna()

#     ob_med = merged["Obesity"].median()
#     mn_med = merged["Malnutrition"].median()

#     fig = px.scatter(
#         merged, x="Obesity", y="Malnutrition",
#         color="Region", hover_name="Country",
#         title=f"⚖️ The Nutrition Paradox — Obesity vs Malnutrition ({year})",
#         labels={"Obesity": "Obesity (%)", "Malnutrition": "Malnutrition (%)"},
#         color_discrete_sequence=REGION_PALETTE,
#     )
#     fig.add_hline(y=mn_med, line_dash="dot",
#                   line_color="rgba(255,255,255,0.3)", opacity=0.6)
#     fig.add_vline(x=ob_med, line_dash="dot",
#                   line_color="rgba(255,255,255,0.3)", opacity=0.6)
#     fig.add_annotation(x=merged["Obesity"].max() * 0.88,
#                        y=merged["Malnutrition"].max() * 0.92,
#                        text="Dual Burden ↗", showarrow=False,
#                        font=dict(color=HIGH_COLOR, size=12, family="monospace"))
#     fig.add_annotation(x=merged["Obesity"].max() * 0.88,
#                        y=merged["Malnutrition"].min() * 2,
#                        text="High Obesity Only", showarrow=False,
#                        font=dict(color=FEMALE_COLOR, size=11))
#     fig.update_layout(template=TEMPLATE, hovermode="closest",
#                       legend=dict(orientation="h", y=-0.2))
#     return fig


# def plot_ci_heatmap(df: pd.DataFrame,
#                     condition: str = "Obesity") -> go.Figure:
#     """Heatmap — avg CI_Width per Region × Age_Group (data reliability)."""
#     pivot = (df.groupby(["Region", "Age_Group"])["CI_Width"]
#                .mean().unstack().fillna(0).round(2))
#     fig = go.Figure(data=go.Heatmap(
#         z=pivot.values,
#         x=pivot.columns.tolist(),
#         y=pivot.index.tolist(),
#         colorscale="YlOrRd",
#         text=pivot.values,
#         texttemplate="%{text:.1f}",
#         hovertemplate="Region: %{y}<br>Age Group: %{x}<br>"
#                       "Avg CI Width: %{z:.2f}<extra></extra>",
#     ))
#     fig.update_layout(
#         title=f"{condition} Data Reliability — Avg CI Width (Region × Age Group)",
#         xaxis_title="Age Group", yaxis_title="Region",
#         template=TEMPLATE,
#     )
#     return fig


# def plot_country_comparison(df: pd.DataFrame,
#                              countries: list,
#                              condition: str = "Obesity") -> go.Figure:
#     """Multi-line — compare selected countries over time."""
#     filt = (df[df["Country"].isin(countries) & (df["Gender"] == "Both")]
#             .groupby(["Country", "Year"])["Mean_Estimate"]
#             .mean().reset_index())
#     fig = px.line(filt, x="Year", y="Mean_Estimate",
#                   color="Country", markers=True,
#                   title=f"{condition} Trend: " + ", ".join(countries),
#                   labels={"Mean_Estimate": f"{condition} (%)"})
#     fig.update_layout(template=TEMPLATE, hovermode="x unified",
#                       legend=dict(orientation="h", y=1.1))
#     return fig


# def plot_age_group_bar(df: pd.DataFrame,
#                        condition: str = "Obesity") -> go.Figure:
#     """Simple bar — Adults vs Children/Adolescents average."""
#     grp = (df[df["Gender"] == "Both"]
#            .groupby("Age_Group")["Mean_Estimate"]
#            .mean().reset_index())
#     fig = px.bar(grp, x="Age_Group", y="Mean_Estimate",
#                  title=f"Average {condition}: Adults vs Children/Adolescents",
#                  labels={"Mean_Estimate": f"Avg {condition} (%)"},
#                  color="Age_Group",
#                  color_discrete_map={"Adult": ADULT_COLOR,
#                                      "Child/Adolescent": CHILD_COLOR})
#     fig.update_layout(template=TEMPLATE, showlegend=False)
#     return fig


# def plot_grouped_bar(df_ob: pd.DataFrame, df_mn: pd.DataFrame,
#                      group_col: str = "Region") -> go.Figure:
#     """Side-by-side obesity vs malnutrition across a categorical dimension."""
#     ob = (df_ob[df_ob["Gender"] == "Both"]
#           .groupby(group_col)["Mean_Estimate"].mean()
#           .reset_index(name="Obesity"))
#     mn = (df_mn[df_mn["Gender"] == "Both"]
#           .groupby(group_col)["Mean_Estimate"].mean()
#           .reset_index(name="Malnutrition"))
#     merged = ob.merge(mn, on=group_col).sort_values("Obesity", ascending=False)
#     fig = go.Figure(data=[
#         go.Bar(name="Obesity",      x=merged[group_col], y=merged["Obesity"],
#                marker_color=OBESITY_COLOR),
#         go.Bar(name="Malnutrition", x=merged[group_col], y=merged["Malnutrition"],
#                marker_color=MALNUTRITION_COLOR),
#     ])
#     fig.update_layout(barmode="group",
#                       title=f"Obesity vs Malnutrition by {group_col}",
#                       xaxis_title=group_col, yaxis_title="Average (%)",
#                       xaxis_tickangle=-30, template=TEMPLATE,
#                       legend=dict(orientation="h", y=1.1))
#     return fig


# def plot_level_pie(df: pd.DataFrame,
#                    level_col: str,
#                    condition: str = "Obesity") -> go.Figure:
#     """Donut chart — proportion in each level (High/Moderate/Low)."""
#     counts = df[level_col].value_counts().reset_index()
#     counts.columns = ["Level", "Count"]
#     colors = {"High": HIGH_COLOR, "Moderate": MOD_COLOR, "Low": LOW_COLOR}
#     fig = px.pie(counts, names="Level", values="Count", hole=0.45,
#                  title=f"{condition} Level Distribution",
#                  color="Level", color_discrete_map=colors)
#     fig.update_traces(textinfo="percent+label")
#     fig.update_layout(template=TEMPLATE)
#     return fig


# def plot_choropleth(df: pd.DataFrame,
#                     condition: str = "Obesity",
#                     year: int = 2022) -> go.Figure:
#     """World choropleth — Mean_Estimate per country for a given year."""
#     filt = (df[(df["Gender"] == "Both") & (df["Year"] == year)]
#             .groupby("Country")["Mean_Estimate"].mean().reset_index())
#     scale = "Reds" if condition == "Obesity" else "Blues"
#     fig   = px.choropleth(
#         filt, locations="Country", locationmode="country names",
#         color="Mean_Estimate", color_continuous_scale=scale,
#         title=f"Global {condition} Levels ({year})",
#         labels={"Mean_Estimate": f"{condition} (%)"},
#     )
#     fig.update_layout(
#         template=TEMPLATE,
#         geo=dict(showframe=False, showcoastlines=True,
#                  bgcolor="rgba(0,0,0,0)"),
#         margin=dict(l=0, r=0, t=50, b=0),
#     )
#     return fig


# def plot_min_max_band(df: pd.DataFrame,
#                       condition: str = "Malnutrition") -> go.Figure:
#     """
#     Band chart showing Min / Avg / Max per year.
#     Used for Q19 (malnutrition year-wise min/max).
#     """
#     grp = (df[df["Gender"] == "Both"]
#            .groupby("Year")["Mean_Estimate"]
#            .agg(["min", "mean", "max"])
#            .reset_index()
#            .rename(columns={"min": "Min", "mean": "Avg", "max": "Max"}))
#     fig = go.Figure()
#     fig.add_traces([
#         go.Scatter(x=grp["Year"], y=grp["Max"],
#                    name="Max", line=dict(color=HIGH_COLOR, dash="dash")),
#         go.Scatter(x=grp["Year"], y=grp["Avg"],
#                    name="Avg", line=dict(color=MALNUTRITION_COLOR, width=3),
#                    mode="lines+markers", marker_size=7),
#         go.Scatter(x=grp["Year"], y=grp["Min"],
#                    name="Min", line=dict(color=LOW_COLOR, dash="dash")),
#     ])
#     fig.update_layout(
#         title=f"{condition} Min / Avg / Max per Year",
#         xaxis_title="Year", yaxis_title="(%)",
#         template=TEMPLATE, hovermode="x unified",
#         legend=dict(orientation="h", y=1.1),
#     )
#     return fig


# # =============================================================
# # AUTO-CHART — driven by QUERY_META in queries.py
# # Called from the SQL Queries page to render the right chart
# # for whichever query the user selects.
# # =============================================================

# def auto_chart(df: pd.DataFrame, meta: dict,
#                df_ob: pd.DataFrame = None,
#                df_mn: pd.DataFrame = None) -> go.Figure:
#     """
#     Dispatch to the correct Plotly figure based on meta['chart_type'].
#     Falls back to a sensible bar chart if df has only 2 columns.
#     """
#     ct       = meta.get("chart_type", "bar")
#     x_col    = meta.get("x")
#     y_col    = meta.get("y")
#     color_col = meta.get("color_col")
#     category  = meta.get("category", "obesity")

#     bar_color  = OBESITY_COLOR if category == "obesity" else (
#                  MALNUTRITION_COLOR if category == "malnutrition" else "#667eea")

#     if df is None or df.empty:
#         fig = go.Figure()
#         fig.update_layout(title="No data returned", template=TEMPLATE)
#         return fig

#     # ── grouped_bar (combined queries with two y columns) ────
#     if ct == "grouped_bar" and isinstance(y_col, list):
#         fig = go.Figure(data=[
#             go.Bar(name=y_col[0], x=df[x_col], y=df[y_col[0]],
#                    marker_color=OBESITY_COLOR),
#             go.Bar(name=y_col[1], x=df[x_col], y=df[y_col[1]],
#                    marker_color=MALNUTRITION_COLOR),
#         ])
#         fig.update_layout(barmode="group", template=TEMPLATE,
#                           xaxis_tickangle=-30,
#                           legend=dict(orientation="h", y=1.1))
#         return fig

#     # ── line ─────────────────────────────────────────────────
#     if ct == "line":
#         if color_col and color_col in df.columns:
#             fig = px.line(df, x=x_col, y=y_col, color=color_col,
#                           markers=True)
#         else:
#             fig = px.line(df, x=x_col, y=y_col, markers=True,
#                           color_discrete_sequence=[bar_color])
#         fig.update_traces(line_width=2.5, marker_size=7)
#         fig.update_layout(template=TEMPLATE, hovermode="x unified")
#         return fig

#     # ── table (no chart; caller handles display) ─────────────
#     if ct == "table":
#         fig = go.Figure()
#         fig.update_layout(title="See table above", template=TEMPLATE)
#         return fig

#     # ── bar (default) ─────────────────────────────────────────
#     if color_col and color_col in df.columns:
#         fig = px.bar(df, x=x_col, y=y_col, color=color_col,
#                      barmode="group")
#     else:
#         # horizontal bar if many categories
#         if df[x_col].nunique() > 6 if x_col in df.columns else False:
#             fig = px.bar(df.sort_values(y_col),
#                          x=y_col, y=x_col, orientation="h",
#                          color=y_col,
#                          color_continuous_scale=["#1a1a2e", bar_color])
#             fig.update_layout(coloraxis_showscale=False)
#         else:
#             fig = px.bar(df, x=x_col, y=y_col,
#                          color_discrete_sequence=[bar_color])
#     fig.update_layout(template=TEMPLATE, xaxis_tickangle=-30)
#     return fig










"""
viz_utils.py  —  Reusable Plotly chart functions for Nutrition Paradox.
Matches the glowing purple/dark palette of the NASA NEO project.

Place this file at:  NUTRITION_PARADOX/app/viz_utils.py
"""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ── Palette ───────────────────────────────────────────────────────────────
PRIMARY  = "#667eea"
OBESITY  = "#ef4444"
MALNUT   = "#3b82f6"
MALE_C   = "#3b82f6"
FEMALE_C = "#f472b6"
SAFE_C   = "#10b981"
WARN_C   = "#f59e0b"
ADULT_C  = "#8b5cf6"
CHILD_C  = "#f59e0b"
REGION_SEQ = px.colors.qualitative.Pastel

_LAYOUT = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#e2e8f0", family="Inter, sans-serif", size=12),
    margin=dict(l=10, r=10, t=50, b=10),
    hoverlabel=dict(bgcolor="#1e1b4b", font_color="white"),
)

def _apply(fig, **extra):
    fig.update_layout(**{**_LAYOUT, **extra})
    return fig

# 1. Dual trend
def plot_dual_trend(df_ob, df_mn):
    ob = df_ob[df_ob["Gender"]=="Both"].groupby("Year")["Mean_Estimate"].mean().reset_index()
    mn = df_mn[df_mn["Gender"]=="Both"].groupby("Year")["Mean_Estimate"].mean().reset_index()
    fig = go.Figure()
    fig.add_scatter(x=ob["Year"], y=ob["Mean_Estimate"], name="Obesity",
                    line=dict(color=OBESITY, width=3), mode="lines+markers", marker_size=8)
    fig.add_scatter(x=mn["Year"], y=mn["Mean_Estimate"], name="Malnutrition",
                    line=dict(color=MALNUT, width=3), mode="lines+markers",
                    marker=dict(size=8, symbol="diamond"))
    return _apply(fig, title="🌍 Global Obesity vs Malnutrition — 2012 to 2022",
                  xaxis_title="Year", yaxis_title="Global Average (%)", hovermode="x unified",
                  legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))

# 2. Top N countries
def plot_top_countries(df, n=10, condition="Obesity", year=None, age_group=None):
    color = OBESITY if condition == "Obesity" else MALNUT
    filt = df[df["Gender"]=="Both"].copy()
    if year:      filt = filt[filt["Year"]==year]
    if age_group: filt = filt[filt["Age_Group"]==age_group]
    top = filt.groupby("Country")["Mean_Estimate"].mean().nlargest(n).reset_index().sort_values("Mean_Estimate")
    fig = px.bar(top, x="Mean_Estimate", y="Country", orientation="h",
                 color="Mean_Estimate",
                 color_continuous_scale=[[0,"#1e1b4b"],[0.5,color],[1,"#fff"]],
                 labels={"Mean_Estimate":f"{condition} (%)"})
    fig.update_layout(coloraxis_showscale=False)
    year_lbl = f" ({year})" if year else " (avg 2012–2022)"
    return _apply(fig, title=f"🏆 Top {n} Countries by {condition}{year_lbl}")

# 3. Gender gap
def plot_gender_gap(df, condition="Obesity"):
    filt = df[df["Gender"].isin(["Male","Female"])].copy()
    grp  = filt.groupby(["Region","Gender"])["Mean_Estimate"].mean().reset_index()
    fig  = px.bar(grp, x="Region", y="Mean_Estimate", color="Gender", barmode="group",
                  color_discrete_map={"Male":MALE_C,"Female":FEMALE_C},
                  labels={"Mean_Estimate":f"Avg {condition} (%)"})
    fig.update_layout(xaxis_tickangle=-30, legend=dict(orientation="h", yanchor="bottom", y=1.02))
    return _apply(fig, title=f"⚧ {condition} by Region and Gender")

# 4. Box plot
def plot_region_boxplot(df, condition="Obesity"):
    filt = df[df["Gender"]=="Both"].copy()
    fig  = px.box(filt, x="Region", y="Mean_Estimate", color="Region",
                  color_discrete_sequence=REGION_SEQ, labels={"Mean_Estimate":f"{condition} (%)"})
    fig.update_layout(xaxis_tickangle=-30, showlegend=False)
    return _apply(fig, title=f"📦 {condition} Spread by WHO Region")

# 5. Paradox scatter
def plot_paradox_scatter(df_ob, df_mn, year=2022):
    ob = (df_ob[(df_ob["Gender"]=="Both")&(df_ob["Year"]==year)]
          .groupby(["Country","Region"])["Mean_Estimate"].mean().reset_index(name="Obesity"))
    mn = (df_mn[(df_mn["Gender"]=="Both")&(df_mn["Year"]==year)]
          .groupby("Country")["Mean_Estimate"].mean().reset_index(name="Malnutrition"))
    merged = ob.merge(mn, on="Country").dropna()
    ob_med = merged["Obesity"].median()
    mn_med = merged["Malnutrition"].median()
    fig = px.scatter(merged, x="Obesity", y="Malnutrition", color="Region",
                     hover_name="Country", size_max=14,
                     color_discrete_sequence=REGION_SEQ,
                     labels={"Obesity":"Obesity (%)","Malnutrition":"Malnutrition (%)"})
    fig.add_hline(y=mn_med, line_dash="dot", line_color="gray", opacity=0.4)
    fig.add_vline(x=ob_med, line_dash="dot", line_color="gray", opacity=0.4)
    fig.add_annotation(x=merged["Obesity"].quantile(0.85), y=merged["Malnutrition"].quantile(0.85),
                       text="⚠️ Dual Burden", showarrow=False, font=dict(size=11, color="#94a3b8"))
    fig.add_annotation(x=merged["Obesity"].quantile(0.15), y=merged["Malnutrition"].quantile(0.15),
                       text="✅ Low Both",   showarrow=False, font=dict(size=11, color="#94a3b8"))
    return _apply(fig, title=f"⚖️ The Nutrition Paradox — Obesity vs Malnutrition ({year})",
                  hovermode="closest")

# 6. CI heatmap
def plot_ci_heatmap(df, condition="Obesity"):
    pivot = df.groupby(["Region","Age_Group"])["CI_Width"].mean().unstack().fillna(0).round(2)
    fig = go.Figure(data=go.Heatmap(
        z=pivot.values, x=pivot.columns.tolist(), y=pivot.index.tolist(),
        colorscale="Plasma", text=pivot.values, texttemplate="%{text:.1f}",
        hovertemplate="Region: %{y}<br>Age: %{x}<br>Avg CI: %{z:.2f}<extra></extra>",
    ))
    return _apply(fig, title=f"🔬 {condition} Data Reliability — Avg CI Width",
                  xaxis_title="Age Group", yaxis_title="Region")

# 7. Multi-country line
def plot_country_comparison(df, countries, condition="Obesity"):
    filt = (df[df["Country"].isin(countries)&(df["Gender"]=="Both")]
            .groupby(["Country","Year"])["Mean_Estimate"].mean().reset_index())
    fig = px.line(filt, x="Year", y="Mean_Estimate", color="Country",
                  markers=True, labels={"Mean_Estimate":f"{condition} (%)"})
    fig.update_traces(line_width=2.5, marker_size=7)
    fig.update_layout(hovermode="x unified", legend=dict(orientation="h", yanchor="bottom", y=1.02))
    return _apply(fig, title=f"📈 {condition} Trend: " + " vs ".join(countries))

# 8. Age group bar
def plot_age_group_bar(df, condition="Obesity"):
    grp = df[df["Gender"]=="Both"].groupby("Age_Group")["Mean_Estimate"].mean().reset_index()
    fig = px.bar(grp, x="Age_Group", y="Mean_Estimate", color="Age_Group",
                 color_discrete_map={"Adult":ADULT_C,"Child/Adolescent":CHILD_C},
                 labels={"Mean_Estimate":f"Avg {condition} (%)"}, text="Mean_Estimate")
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig.update_layout(showlegend=False)
    return _apply(fig, title=f"👶 {condition}: Adults vs Children / Adolescents")

# 9. Grouped bar comparison
def plot_grouped_bar(df_ob, df_mn, group_col="Region"):
    ob = df_ob[df_ob["Gender"]=="Both"].groupby(group_col)["Mean_Estimate"].mean().reset_index(name="Obesity")
    mn = df_mn[df_mn["Gender"]=="Both"].groupby(group_col)["Mean_Estimate"].mean().reset_index(name="Malnutrition")
    m  = ob.merge(mn, on=group_col).sort_values("Obesity", ascending=False)
    fig = go.Figure(data=[
        go.Bar(name="Obesity",      x=m[group_col], y=m["Obesity"],
               marker_color=OBESITY, text=m["Obesity"].round(1),
               texttemplate="%{text}%", textposition="outside"),
        go.Bar(name="Malnutrition", x=m[group_col], y=m["Malnutrition"],
               marker_color=MALNUT,  text=m["Malnutrition"].round(1),
               texttemplate="%{text}%", textposition="outside"),
    ])
    fig.update_layout(barmode="group", xaxis_tickangle=-30,
                      legend=dict(orientation="h", yanchor="bottom", y=1.02))
    return _apply(fig, title=f"🔗 Obesity vs Malnutrition by {group_col}", yaxis_title="Average (%)")

# 10. Donut
def plot_level_donut(df, level_col, condition="Obesity"):
    counts = df[level_col].value_counts().reset_index()
    counts.columns = ["Level","Count"]
    cmap = {"High":OBESITY,"Moderate":WARN_C,"Low":SAFE_C}
    fig  = px.pie(counts, names="Level", values="Count", hole=0.48,
                  color="Level", color_discrete_map=cmap)
    fig.update_traces(textinfo="percent+label",
                      marker=dict(line=dict(color="#1e1b4b", width=2)))
    return _apply(fig, title=f"🍩 {condition} Level Distribution")

# 11. Choropleth
def plot_choropleth(df, condition="Obesity", year=2022):
    filt = (df[(df["Gender"]=="Both")&(df["Year"]==year)]
            .groupby("Country")["Mean_Estimate"].mean().reset_index())
    cscale = "Reds" if condition=="Obesity" else "Blues"
    fig = px.choropleth(filt, locations="Country", locationmode="country names",
                        color="Mean_Estimate", color_continuous_scale=cscale,
                        labels={"Mean_Estimate":f"{condition} (%)"})
    fig.update_layout(geo=dict(showframe=False, showcoastlines=True, bgcolor="rgba(0,0,0,0)"),
                      margin=dict(l=0,r=0,t=50,b=0))
    return _apply(fig, title=f"🌐 Global {condition} Levels ({year})")

# 12. Min/Max band
def plot_min_max_band(df, condition="Malnutrition"):
    fig = go.Figure()
    fig.add_scatter(x=df["Year"], y=df["max_mal"], name="Max",
                    line=dict(color=OBESITY, dash="dash", width=1.5), mode="lines")
    fig.add_scatter(x=df["Year"], y=df["min_mal"], name="Min",
                    line=dict(color=SAFE_C, dash="dash", width=1.5), mode="lines",
                    fill="tonexty", fillcolor="rgba(59,130,246,0.12)")
    fig.add_scatter(x=df["Year"], y=df["avg_mal"], name="Global Avg",
                    line=dict(color=MALNUT, width=3), mode="lines+markers", marker_size=7)
    fig.update_layout(hovermode="x unified",
                      legend=dict(orientation="h", yanchor="bottom", y=1.02))
    return _apply(fig, title=f"📊 {condition} Min / Avg / Max Band by Year",
                  xaxis_title="Year", yaxis_title=f"{condition} (%)")

# 13. Auto chart
def auto_chart(df, query_name):
    import re
    if df is None or df.empty or len(df.columns) < 2:
        return None
    num_cols = df.select_dtypes(include="number").columns.tolist()
    cat_cols = df.select_dtypes(exclude="number").columns.tolist()
    if not num_cols:
        return None
    y_col = num_cols[0]
    x_col = cat_cols[0] if cat_cols else df.columns[0]

    if "trend" in query_name.lower() or "year" in query_name.lower() or "Year" in df.columns:
        if "Year" in df.columns:
            x_col = "Year"
        if "Country" in df.columns and df["Country"].nunique() > 1:
            fig = px.line(df, x=x_col, y=y_col, color="Country",
                          markers=True, color_discrete_sequence=REGION_SEQ)
        else:
            fig = px.line(df, x=x_col, y=y_col, markers=True,
                          color_discrete_sequence=[PRIMARY], line_shape="spline")
        fig.update_traces(line_width=2.5)
        return _apply(fig, title=f"📈 {query_name}", hovermode="x unified")

    if "reliable" in query_name.lower() or "consistent" in query_name.lower():
        if "type" in df.columns:
            fig = px.bar(df, x="Country", y=y_col, color="type", barmode="group",
                         color_discrete_map={"Least Reliable":OBESITY,"Most Consistent":SAFE_C})
            return _apply(fig, title=f"📊 {query_name}", xaxis_tickangle=-30)

    if len(df) <= 20:
        fig = px.bar(df.sort_values(y_col), x=y_col, y=x_col, orientation="h",
                     color=y_col,
                     color_continuous_scale=[[0,"#1e1b4b"],[0.5,PRIMARY],[1,"#a5b4fc"]],
                     text=y_col)
        fig.update_traces(texttemplate="%{text}", textposition="outside")
        fig.update_layout(coloraxis_showscale=False)
        return _apply(fig, title=f"📊 {query_name}")

    fig = px.bar(df, x=x_col, y=y_col, color_discrete_sequence=[PRIMARY], text=y_col)
    fig.update_traces(texttemplate="%{text}", textposition="outside")
    fig.update_layout(xaxis_tickangle=-30)
    return _apply(fig, title=f"📊 {query_name}")