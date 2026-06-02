# import streamlit as st
# import sqlite3
# import pandas as pd
# import numpy as np

# import plotly.express as px
# import plotly.graph_objects as go

# from pathlib import Path
# from streamlit_option_menu import option_menu

# from sql.queries import QUERIES, QUERY_INSIGHTS

# # ============================================================
# # PAGE CONFIG
# # ============================================================

# st.set_page_config(
#     page_title="⚖️ Nutrition Paradox",
#     page_icon="⚖️",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # ============================================================
# # PATHS
# # ============================================================

# BASE_DIR = Path(__file__).resolve().parent.parent
# DB_PATH = BASE_DIR / "nutrition.db"

# # ============================================================
# # DATABASE
# # ============================================================

# @st.cache_resource
# def get_connection():
#     return sqlite3.connect(DB_PATH, check_same_thread=False)

# @st.cache_data
# def run_query(query):
#     conn = get_connection()
#     return pd.read_sql(query, conn)

# # ============================================================
# # CUSTOM CSS
# # ============================================================

# st.markdown("""
# <style>

# @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

# html, body, [class*="css"] {
#     font-family: 'Poppins', sans-serif;
# }

# .stApp{
#     background:
#         linear-gradient(135deg, rgba(77,163,255,0.12), rgba(46,204,113,0.10)),
#         linear-gradient(45deg, rgba(255,90,95,0.06), rgba(255,255,255,0.96));
#     background-attachment: fixed;
# }

# section[data-testid="stSidebar"]{
#     background: rgba(255,255,255,0.18);
#     backdrop-filter: blur(20px);
#     border-right: 1px solid rgba(255,255,255,0.20);
#     box-shadow: 0 0 25px rgba(77,163,255,0.15);
# }

# .hero-title{
#     font-size: 4rem;
#     font-weight: 800;
#     text-align:center;
#     background: linear-gradient(to right,#4DA3FF,#2ECC71,#FF5A5F);
#     -webkit-background-clip:text;
#     -webkit-text-fill-color:transparent;
#     margin-bottom:0;
# }

# .hero-subtitle{
#     text-align:center;
#     color:#4b5563;
#     font-size:1.2rem;
#     margin-bottom:2rem;
# }

# .metric-card{
#     background: rgba(255,255,255,0.25);
#     border-radius:22px;
#     padding:25px;
#     text-align:center;
#     backdrop-filter: blur(18px);
#     border:1px solid rgba(255,255,255,0.2);
#     box-shadow:0 0 30px rgba(77,163,255,0.18);
#     transition:0.3s ease;
# }

# .metric-card:hover{
#     transform: translateY(-6px) scale(1.02);
#     box-shadow:0 0 40px rgba(46,204,113,0.35);
# }

# .metric-title{
#     font-size:1rem;
#     color:#374151;
#     font-weight:600;
# }

# .metric-value{
#     font-size:2rem;
#     font-weight:700;
#     color:#111827;
# }

# .section-title{
#     font-size:2rem;
#     font-weight:700;
#     margin-top:15px;
#     margin-bottom:20px;
# }

# .glass-card{
#     background: rgba(255,255,255,0.20);
#     border-radius:25px;
#     padding:25px;
#     backdrop-filter: blur(18px);
#     border:1px solid rgba(255,255,255,0.25);
#     box-shadow:0 0 25px rgba(77,163,255,0.18);
#     margin-bottom:25px;
# }

# .insight-box{
#     background: linear-gradient(135deg,#4DA3FF,#2ECC71);
#     border-radius:22px;
#     padding:22px;
#     color:white;
#     box-shadow:0 0 25px rgba(46,204,113,0.30);
#     margin-top:25px;
# }

# .stButton > button{
#     background: linear-gradient(to right,#4DA3FF,#2ECC71);
#     color:white;
#     border:none;
#     border-radius:12px;
#     padding:12px 22px;
#     font-weight:600;
# }

# .stButton > button:hover{
#     transform: scale(1.04);
#     box-shadow:0 0 25px rgba(77,163,255,0.35);
# }

# </style>
# """, unsafe_allow_html=True)

# # ============================================================
# # SIDEBAR
# # ============================================================

# with st.sidebar:

#     st.markdown("## ⚖️ Nutrition Paradox")

#     selected = option_menu(
#         menu_title=None,
#         options=[
#             "Home Dashboard",
#             "Obesity Analytics",
#             "Malnutrition Analytics",
#             "Combined Analysis",
#             "SQL Query Explorer",
#             "EDA Visualizations",
#             "Insights & Recommendations",
#             "About Project"
#         ],
#         icons=[
#             "house",
#             "bar-chart",
#             "heart-pulse",
#             "globe",
#             "database",
#             "graph-up",
#             "lightbulb",
#             "info-circle"
#         ],
#         default_index=0
#     )

#     st.markdown("---")

#     st.markdown("### 🎛 Global Filters")

#     region = st.selectbox("Region", ["All"])
#     gender = st.selectbox("Gender", ["All","Male","Female","Both"])
#     age = st.selectbox("Age Group", ["All","Adults","Children"])

# # ============================================================
# # HOME DASHBOARD
# # ============================================================

# if selected == "Home Dashboard":

#     st.markdown("""
#     <div class="hero-title">⚖️ Nutrition Paradox</div>
#     <div class="hero-subtitle">
#     Exploring the coexistence of obesity and malnutrition globally
#     </div>
#     """, unsafe_allow_html=True)

#     obesity_avg = run_query("""
#     SELECT ROUND(AVG(Mean_Estimate),2) val
#     FROM obesity
#     """).iloc[0,0]

#     malnutrition_avg = run_query("""
#     SELECT ROUND(AVG(Mean_Estimate),2) val
#     FROM malnutrition
#     """).iloc[0,0]

#     top_region = run_query("""
#     SELECT Region, AVG(Mean_Estimate) val
#     FROM obesity
#     GROUP BY Region
#     ORDER BY val DESC
#     LIMIT 1
#     """).iloc[0,0]

#     c1,c2,c3,c4 = st.columns(4)

#     cards = [
#         ("🍔 Avg Obesity", f"{obesity_avg}%"),
#         ("🥗 Avg Malnutrition", f"{malnutrition_avg}%"),
#         ("🌍 Most Affected", top_region),
#         ("📊 Coverage", "Global")
#     ]

#     for col, card in zip([c1,c2,c3,c4], cards):

#         with col:
#             st.markdown(f"""
#             <div class="metric-card">
#                 <div class="metric-title">{card[0]}</div>
#                 <div class="metric-value">{card[1]}</div>
#             </div>
#             """, unsafe_allow_html=True)

#     st.markdown("## 🌎 Global Obesity Map")

#     map_df = run_query("""
#     SELECT Country,
#            AVG(Mean_Estimate) AS Obesity
#     FROM obesity
#     GROUP BY Country
#     """)

#     fig = px.choropleth(
#         map_df,
#         locations="Country",
#         locationmode="country names",
#         color="Obesity",
#         color_continuous_scale=[
#             "#DCEEFF",
#             "#4DA3FF",
#             "#2ECC71",
#             "#FF5A5F"
#         ]
#     )

#     fig.update_layout(
#         paper_bgcolor="rgba(0,0,0,0)",
#         plot_bgcolor="rgba(0,0,0,0)"
#     )

#     st.plotly_chart(fig, use_container_width=True)

# # ============================================================
# # OBESITY ANALYTICS
# # ============================================================

# elif selected == "Obesity Analytics":

#     st.markdown("""
#     <div class="section-title">🍔 Obesity Analytics</div>
#     """, unsafe_allow_html=True)

#     df = run_query("""
#     SELECT Region,
#            AVG(Mean_Estimate) Avg_Obesity
#     FROM obesity
#     GROUP BY Region
#     """)

#     fig = px.bar(
#         df,
#         x="Region",
#         y="Avg_Obesity",
#         color="Avg_Obesity",
#         text="Avg_Obesity",
#         color_continuous_scale="Blues"
#     )

#     fig.update_layout(
#         paper_bgcolor="rgba(0,0,0,0)"
#     )

#     st.plotly_chart(fig, use_container_width=True)

# # ============================================================
# # MALNUTRITION ANALYTICS
# # ============================================================

# elif selected == "Malnutrition Analytics":

#     st.markdown("""
#     <div class="section-title">🥗 Malnutrition Analytics</div>
#     """, unsafe_allow_html=True)

#     df = run_query("""
#     SELECT Region,
#            AVG(Mean_Estimate) Avg_Malnutrition
#     FROM malnutrition
#     GROUP BY Region
#     """)

#     fig = px.bar(
#         df,
#         x="Region",
#         y="Avg_Malnutrition",
#         color="Avg_Malnutrition",
#         text="Avg_Malnutrition",
#         color_continuous_scale="Reds"
#     )

#     st.plotly_chart(fig, use_container_width=True)

# # ============================================================
# # COMBINED ANALYSIS
# # ============================================================

# elif selected == "Combined Analysis":

#     st.markdown("""
#     <div class="section-title">🌍 Combined Analysis</div>
#     """, unsafe_allow_html=True)

#     df = run_query("""
#     SELECT o.Region,
#            AVG(o.Mean_Estimate) Obesity,
#            AVG(m.Mean_Estimate) Malnutrition
#     FROM obesity o
#     JOIN malnutrition m
#     ON o.Country = m.Country
#     GROUP BY o.Region
#     """)

#     fig = go.Figure()

#     fig.add_trace(go.Bar(
#         x=df["Region"],
#         y=df["Obesity"],
#         name="Obesity"
#     ))

#     fig.add_trace(go.Bar(
#         x=df["Region"],
#         y=df["Malnutrition"],
#         name="Malnutrition"
#     ))

#     fig.update_layout(
#         barmode="group",
#         paper_bgcolor="rgba(0,0,0,0)"
#     )

#     st.plotly_chart(fig, use_container_width=True)

# # ============================================================
# # SQL QUERY EXPLORER
# # ============================================================

# elif selected == "SQL Query Explorer":

#     st.markdown("""
#     <div class="hero-title">🧠 SQL Query Explorer</div>
#     <div class="hero-subtitle">
#     Explore all 25 SQL queries interactively
#     </div>
#     """, unsafe_allow_html=True)

#     category = st.selectbox(
#         "📂 Query Category",
#         [
#             "All Queries",
#             "Obesity Queries",
#             "Malnutrition Queries",
#             "Combined Queries"
#         ]
#     )

#     filtered_queries = {}

#     for key, value in QUERIES.items():

#         if category == "All Queries":
#             filtered_queries[key] = value

#         elif category == "Obesity Queries" and key.startswith("OBESITY"):
#             filtered_queries[key] = value

#         elif category == "Malnutrition Queries" and key.startswith("MALNUTRITION"):
#             filtered_queries[key] = value

#         elif category == "Combined Queries" and key.startswith("COMBINED"):
#             filtered_queries[key] = value

#     col1,col2 = st.columns([3,1])

#     with col1:

#         selected_query = st.selectbox(
#             "🔍 Select SQL Query",
#             list(filtered_queries.keys())
#         )

#     with col2:

#         auto_chart = st.checkbox(
#             "📊 Auto Chart",
#             value=True
#         )

#     with st.expander("🧾 SQL Code"):

#         st.code(
#             filtered_queries[selected_query],
#             language="sql"
#         )

#     if st.button("▶ Execute Query"):

#         df = run_query(filtered_queries[selected_query])

#         st.success(f"✅ Returned {len(df)} rows")

#         st.dataframe(df, use_container_width=True)

#         csv = df.to_csv(index=False)

#         st.download_button(
#             "📥 Download CSV",
#             csv,
#             file_name="nutrition_results.csv",
#             mime="text/csv"
#         )

#         if auto_chart:

#             numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

#             if len(numeric_cols) > 0:

#                 num_col = numeric_cols[0]

#                 cat_cols = [c for c in df.columns if c != num_col]

#                 if len(cat_cols) > 0:

#                     fig = px.bar(
#                         df,
#                         x=cat_cols[0],
#                         y=num_col,
#                         color=num_col,
#                         text=num_col,
#                         color_continuous_scale=[
#                             "#4DA3FF",
#                             "#2ECC71",
#                             "#FF5A5F"
#                         ]
#                     )

#                     fig.update_layout(
#                         paper_bgcolor="rgba(0,0,0,0)",
#                         plot_bgcolor="rgba(0,0,0,0)"
#                     )

#                     st.plotly_chart(fig, use_container_width=True)

#         st.markdown(f"""
#         <div class="insight-box">
#         <h3>💡 Insight Summary</h3>
#         <p>{QUERY_INSIGHTS.get(selected_query, "Nutrition insight generated.")}</p>
#         </div>
#         """, unsafe_allow_html=True)

# # ============================================================
# # EDA VISUALIZATIONS
# # ============================================================

# elif selected == "EDA Visualizations":

#     st.markdown("""
#     <div class="section-title">📈 EDA Visualizations</div>
#     """, unsafe_allow_html=True)

#     df = run_query("""
#     SELECT Mean_Estimate
#     FROM obesity
#     """)

#     fig = px.histogram(
#         df,
#         x="Mean_Estimate",
#         nbins=30,
#         color_discrete_sequence=["#4DA3FF"]
#     )

#     st.plotly_chart(fig, use_container_width=True)

# # ============================================================
# # INSIGHTS PAGE
# # ============================================================

# elif selected == "Insights & Recommendations":

#     st.markdown("""
#     <div class="section-title">
#     💡 Insights & Recommendations
#     </div>
#     """, unsafe_allow_html=True)

#     st.markdown("""
#     <div class="insight-box">

#     <h3>🌍 Key Findings</h3>

#     <ul>
#         <li>Several regions face both obesity and malnutrition simultaneously.</li>
#         <li>Gender disparities are significant across many countries.</li>
#         <li>Childhood obesity is increasing globally.</li>
#         <li>Undernutrition persists in low-income regions.</li>
#     </ul>

#     </div>
#     """, unsafe_allow_html=True)

# # ============================================================
# # ABOUT PAGE
# # ============================================================

# elif selected == "About Project":

#     st.markdown("""
#     <div class="section-title">
#     📘 About Project
#     </div>
#     """, unsafe_allow_html=True)

#     st.markdown("""
#     <div class="glass-card">

#     ### ⚖️ Nutrition Paradox

#     This project explores obesity and malnutrition using WHO datasets.

#     ### 🧠 Tech Stack

#     - Python
#     - Streamlit
#     - SQLite
#     - Plotly
#     - Pandas

#     ### 🌍 Goal

#     Identify vulnerable regions and health inequalities globally.

#     </div>
#     """, unsafe_allow_html=True)

# # ============================================================
# # FOOTER
# # ============================================================

# st.markdown("---")

# st.markdown("""
# <center>
# Built with Streamlit | Nutrition Analytics Platform
# </center>
# """, unsafe_allow_html=True)



















































































"""
streamlit_app.py  —  Nutrition Paradox: A Global View on Obesity & Malnutrition
Run from project root:  streamlit run app/streamlit_app.py

Folder structure:
    NUTRITION_PARADOX/
    ├── app/
    │   ├── sql/queries.py      ← QUERIES + QUERY_META
    │   ├── db_utils.py
    │   ├── viz_utils.py
    │   └── streamlit_app.py   ← this file
    ├── nutrition.db
    └── requirements.txt
"""

# import os, sys
# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go
# import streamlit as st

# # ── Make app/ importable regardless of launch directory ──────────────────
# sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# from sql.queries import QUERIES, QUERY_META
# from db_utils    import run_query, load_obesity, load_malnutrition, get_dashboard_stats
# from viz_utils   import (
#     plot_dual_trend, plot_top_countries, plot_gender_gap,
#     plot_region_boxplot, plot_paradox_scatter, plot_ci_heatmap,
#     plot_country_comparison, plot_age_group_bar, plot_grouped_bar,
#     plot_level_donut, plot_choropleth, plot_min_max_band,
# )

# # ═══════════════════════════════════════════════════════════════════════════
# # PAGE CONFIG
# # ═══════════════════════════════════════════════════════════════════════════
# st.set_page_config(
#     page_title="⚖️ Nutrition Paradox",
#     page_icon="⚖️",
#     layout="wide",
#     initial_sidebar_state="expanded",
# )

# # ═══════════════════════════════════════════════════════════════════════════
# # CSS  — same glowing-box style as NASA NEO project
# # ═══════════════════════════════════════════════════════════════════════════
# st.markdown("""
# <style>
# @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
# html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

# .stApp{
#     background:
#         linear-gradient(135deg, rgba(77,163,255,0.12), rgba(46,204,113,0.10)),
#         linear-gradient(45deg, rgba(255,90,95,0.06), rgba(255,255,255,0.96));
#     background-attachment: fixed;
# }

# .main-header {
#     font-size: 2.8rem; font-weight: 700; text-align: center;
#     background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#     -webkit-background-clip: text; -webkit-text-fill-color: transparent;
#     background-clip: text; padding: 10px 0 4px; line-height: 1.2;
# }
# .sub-header {
#     text-align: center; color: #94a3b8; font-size: 1rem; margin-bottom: 6px;
# }

# /* ── Glowing insight boxes ── */
# .insight-box {
#     background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#     padding: 18px 22px; border-radius: 12px; color: white; margin: 14px 0;
#     box-shadow: 0 0 18px rgba(102,126,234,0.45);
# }
# .insight-box h3  { margin: 0 0 8px; font-size: 1rem; font-weight: 600; letter-spacing:.02em; }
# .insight-box p   { margin: 0; font-size: 0.88rem; line-height: 1.6; opacity: 0.95; }

# .insight-box-red {
#     background: linear-gradient(135deg, #ef4444 0%, #b91c1c 100%);
#     padding: 18px 22px; border-radius: 12px; color: white; margin: 14px 0;
#     box-shadow: 0 0 18px rgba(239,68,68,0.40);
# }
# .insight-box-red h3 { margin: 0 0 8px; font-size: 1rem; font-weight: 600; }
# .insight-box-red p  { margin: 0; font-size: 0.88rem; line-height: 1.6; opacity: 0.95; }

# .insight-box-blue {
#     background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
#     padding: 18px 22px; border-radius: 12px; color: white; margin: 14px 0;
#     box-shadow: 0 0 18px rgba(59,130,246,0.40);
# }
# .insight-box-blue h3 { margin: 0 0 8px; font-size: 1rem; font-weight: 600; }
# .insight-box-blue p  { margin: 0; font-size: 0.88rem; line-height: 1.6; opacity: 0.95; }

# .insight-box-green {
#     background: linear-gradient(135deg, #10b981 0%, #065f46 100%);
#     padding: 18px 22px; border-radius: 12px; color: white; margin: 14px 0;
#     box-shadow: 0 0 18px rgba(16,185,129,0.40);
# }
# .insight-box-green h3 { margin: 0 0 8px; font-size: 1rem; font-weight: 600; }
# .insight-box-green p  { margin: 0; font-size: 0.88rem; line-height: 1.6; opacity: 0.95; }

# /* ── Page title strip ── */
# .page-title {
#     background: linear-gradient(90deg, rgba(102,126,234,0.15) 0%, transparent 100%);
#     border-left: 4px solid #667eea; padding: 10px 16px;
#     border-radius: 0 8px 8px 0; margin-bottom: 20px;
# }
# .page-title h2 { margin: 0; font-size: 1.4rem; color: #e2e8f0; }
# .page-title p  { margin: 2px 0 0; font-size: 0.82rem; color: #94a3b8; }

# .section-divider { border: none; border-top: 1px solid rgba(102,126,234,0.25); margin: 20px 0; }

# /* ── Sidebar ── */
# [data-testid="stSidebar"] {
#     background: linear-gradient(180deg, #0f0c29 0%, #1a1a3e 50%, #0f0c29 100%);
# }
# [data-testid="stSidebar"] .stMarkdown { color: #94a3b8; }
# [data-testid="stSidebar"] hr { border-color: rgba(102,126,234,0.25); }

# button[data-baseweb="tab"][aria-selected="true"] {
#     color: #667eea !important;
#     border-bottom: 2px solid #667eea !important;
# }
# </style>
# """, unsafe_allow_html=True)

# # ═══════════════════════════════════════════════════════════════════════════
# # PRE-BUILT QUERY GROUPS  using QUERY_META["category"]
# # (no regex — clean and reliable)
# # ═══════════════════════════════════════════════════════════════════════════
# OBESITY_QUERIES    = {k: v for k, v in QUERIES.items()
#                       if QUERY_META.get(k, {}).get("category") == "obesity"}
# MALN_QUERIES       = {k: v for k, v in QUERIES.items()
#                       if QUERY_META.get(k, {}).get("category") == "malnutrition"}
# COMBINED_QUERIES   = {k: v for k, v in QUERIES.items()
#                       if QUERY_META.get(k, {}).get("category") == "combined"}

# # ═══════════════════════════════════════════════════════════════════════════
# # CHART BUILDER  using QUERY_META (chart_type / x / y / color_col)
# # ═══════════════════════════════════════════════════════════════════════════
# _DARK = dict(
#     template="plotly_dark",
#     paper_bgcolor="rgba(0,0,0,0)",
#     plot_bgcolor="rgba(0,0,0,0)",
#     font=dict(color="#e2e8f0", family="Inter, sans-serif", size=12),
#     margin=dict(l=10, r=10, t=50, b=10),
#     hoverlabel=dict(bgcolor="#1e1b4b", font_color="white"),
# )

# _CAT_COLOR = {
#     "obesity":      "#ef4444",
#     "malnutrition": "#3b82f6",
#     "combined":     "#10b981",
# }

# def _meta_chart(df: pd.DataFrame, query_name: str):
#     """
#     Build the best Plotly figure for a query result using QUERY_META.
#     Returns None for chart_type='table' (already shown as DataFrame).
#     """
#     meta       = QUERY_META.get(query_name, {})
#     chart_type = meta.get("chart_type", "bar")
#     x_col      = meta.get("x")
#     y_col      = meta.get("y")          # str or list[str]
#     color_col  = meta.get("color_col")
#     category   = meta.get("category", "obesity")
#     base_color = _CAT_COLOR.get(category, "#667eea")

#     if chart_type == "table":
#         return None

#     if df is None or df.empty:
#         return None

#     # ── Validate columns exist ────────────────────────────────────────
#     y_cols = y_col if isinstance(y_col, list) else [y_col]
#     missing = [c for c in ([x_col] + y_cols + ([color_col] if color_col else []))
#                if c and c not in df.columns]
#     if missing:
#         # Graceful fallback: pick first num + first cat column
#         num = df.select_dtypes(include="number").columns.tolist()
#         cat = df.select_dtypes(exclude="number").columns.tolist()
#         if not num:
#             return None
#         x_col, y_col, color_col = (cat[0] if cat else df.columns[0]), num[0], None
#         chart_type = "bar"
#         y_cols = [y_col]

#     # ── LINE ──────────────────────────────────────────────────────────
#     if chart_type == "line":
#         if color_col and color_col in df.columns:
#             fig = px.line(df, x=x_col, y=y_cols[0], color=color_col,
#                           markers=True,
#                           color_discrete_sequence=px.colors.qualitative.Pastel)
#         else:
#             fig = px.line(df, x=x_col, y=y_cols[0], markers=True,
#                           color_discrete_sequence=[base_color])
#         fig.update_traces(line_width=3, marker_size=8)
#         fig.update_layout(**_DARK, hovermode="x unified",
#                           yaxis_title=y_cols[0].replace("_", " ").title(),
#                           legend=dict(orientation="h", yanchor="bottom", y=1.02))
#         return fig

#     # ── GROUPED_BAR (y is a list, e.g. ["avg_obesity","avg_malnutrition"]) ─
#     if chart_type == "grouped_bar":
#         fig = go.Figure()
#         colors_gb = ["#ef4444", "#3b82f6", "#10b981", "#f59e0b"]
#         for i, yc in enumerate(y_cols):
#             if yc in df.columns:
#                 fig.add_bar(x=df[x_col], y=df[yc],
#                             name=yc.replace("_", " ").title(),
#                             marker_color=colors_gb[i % len(colors_gb)],
#                             text=df[yc].round(1),
#                             texttemplate="%{text}%", textposition="outside")
#         fig.update_layout(**_DARK, barmode="group",
#                           xaxis_tickangle=-20, yaxis_title="Average (%)",
#                           legend=dict(orientation="h", yanchor="bottom", y=1.02))
#         return fig

#     # ── BAR (default) ────────────────────────────────────────────────
#     if color_col and color_col in df.columns:
#         # categorical color
#         fig = px.bar(df, x=x_col, y=y_cols[0], color=color_col, barmode="group",
#                      text=y_cols[0],
#                      color_discrete_sequence=px.colors.qualitative.Pastel)
#     else:
#         fig = px.bar(
#             df.sort_values(y_cols[0], ascending=True) if len(df) <= 20 else df,
#             x=y_cols[0] if len(df) <= 20 else x_col,
#             y=x_col     if len(df) <= 20 else y_cols[0],
#             orientation="h" if len(df) <= 20 else "v",
#             color=y_cols[0],
#             color_continuous_scale=[[0, "#1e1b4b"], [0.5, base_color], [1, "#fff"]],
#             text=y_cols[0],
#         )
#         fig.update_layout(coloraxis_showscale=False)
#     fig.update_traces(texttemplate="%{text}", textposition="outside")
#     fig.update_layout(**_DARK, xaxis_tickangle=-25 if len(df) > 6 else 0,
#                       yaxis_title=y_cols[0].replace("_", " ").title())
#     return fig

# # ═══════════════════════════════════════════════════════════════════════════
# # INSIGHT BOX  — reads from QUERY_META["insight"] + ["category"]
# # ═══════════════════════════════════════════════════════════════════════════
# def insight_box(query_name: str) -> None:
#     meta     = QUERY_META.get(query_name, {})
#     text     = meta.get("insight", "")
#     category = meta.get("category", "")
#     if not text:
#         return
#     if category == "obesity":
#         box_cls, label = "insight-box-red",   "🔴 Obesity Insight"
#     elif category == "malnutrition":
#         box_cls, label = "insight-box-blue",  "🔵 Malnutrition Insight"
#     elif category == "combined":
#         box_cls, label = "insight-box-green", "🔗 Combined Insight"
#     else:
#         box_cls, label = "insight-box",       "💡 Key Insight"
#     st.markdown(f"""
#     <div class="{box_cls}">
#         <h3>{label}</h3>
#         <p>{text}</p>
#     </div>""", unsafe_allow_html=True)

# # ═══════════════════════════════════════════════════════════════════════════
# # QUERY SECTION RENDERER  (used on all 3 query pages)
# # ═══════════════════════════════════════════════════════════════════════════
# def render_query_section(query_name: str) -> None:
#     """
#     SQL expander → Run button → success badge → DataFrame →
#     Download CSV → glowing insight box → QUERY_META-driven chart.
#     """
#     sql  = QUERIES[query_name]
#     meta = QUERY_META.get(query_name, {})

#     with st.expander("📝 View SQL", expanded=False):
#         st.code(sql, language="sql")

#     run = st.button("▶️ Run Query", key=f"run__{query_name}", type="primary")

#     if run:
#         with st.spinner("Querying database…"):
#             df, err = run_query(sql)
#         if err:
#             st.error(f"❌ Error: {err}")
#             return

#         st.success(f"✅ {len(df):,} rows returned")
#         st.dataframe(df, use_container_width=True,
#                      height=min(380, 55 + 35 * len(df)))

#         col_dl, _ = st.columns([1, 5])
#         col_dl.download_button(
#             "📥 Download CSV", df.to_csv(index=False),
#             file_name=f"{query_name[:40].strip()}.csv", mime="text/csv",
#         )

#         # Insight box
#         insight_box(query_name)

#         # Chart (skipped if chart_type == "table")
#         if meta.get("chart_type") != "table":
#             fig = _meta_chart(df, query_name)
#             if fig:
#                 st.plotly_chart(fig, use_container_width=True)

# # ═══════════════════════════════════════════════════════════════════════════
# # SIDEBAR NAVIGATION
# # ═══════════════════════════════════════════════════════════════════════════
# with st.sidebar:
#     st.markdown("""
#     <div style='text-align:center; padding:10px 0 6px;'>
#         <span style='font-size:2.4rem'>⚖️</span>
#         <div style='font-size:1.05rem; font-weight:700; color:#667eea; margin-top:4px;'>
#             Nutrition Paradox
#         </div>
#         <div style='font-size:0.75rem; color:#64748b; margin-top:2px;'>
#             WHO Global Health Analytics
#         </div>
#     </div>""", unsafe_allow_html=True)
#     st.markdown("<hr/>", unsafe_allow_html=True)

#     page = st.radio(
#         "Navigate",
#         [
#             "🏠 Overview",
#             "📊 EDA — Exploratory Analysis",
#             "🔴 Obesity Queries",
#             "🔵 Malnutrition Queries",
#             "🔗 Combined Queries",
#             "🌍 Country Deep-Dive",
#         ],
#         label_visibility="collapsed",
#     )

#     st.markdown("<hr/>", unsafe_allow_html=True)
#     st.markdown("""
#     <div style='font-size:0.75rem; color:#64748b; padding:4px 0;'>
#         <b style='color:#94a3b8'>Data source:</b> WHO GHO API<br>
#         <b style='color:#94a3b8'>Period:</b> 2012 – 2022<br>
#         <b style='color:#94a3b8'>Indicators:</b> BMI-based<br>
#         <b style='color:#94a3b8'>Engine:</b> SQLite + Streamlit
#     </div>""", unsafe_allow_html=True)


# # ═══════════════════════════════════════════════════════════════════════════
# # PAGE 1 — OVERVIEW
# # ═══════════════════════════════════════════════════════════════════════════
# if page == "🏠 Overview":

#     st.markdown('<h1 class="main-header">⚖️ Nutrition Paradox</h1>', unsafe_allow_html=True)
#     st.markdown('<p class="sub-header">A Global View on Obesity & Malnutrition — WHO Data 2012–2022</p>',
#                 unsafe_allow_html=True)
#     st.markdown("---")

#     stats = get_dashboard_stats()
#     c1, c2, c3, c4, c5 = st.columns(5)
#     c1.metric("📋 Obesity Records",       f"{stats['obesity_records']:,}")
#     c2.metric("📋 Malnutrition Records",  f"{stats['malnutrition_records']:,}")
#     c3.metric("🌐 Countries Tracked",     f"{stats['countries']:,}")
#     c4.metric("⚠️ Dual Burden Nations",   f"{stats['dual_burden_count']:,}",
#               help="Countries where both avg obesity AND malnutrition > 10%")
#     c5.metric("📅 Years Covered",         stats["years_covered"])

#     st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)

#     col_a, col_b = st.columns(2)
#     with col_a:
#         st.markdown(f"""
#         <div class="insight-box-red">
#             <h3>🔴 Highest Obesity (2022)</h3>
#             <p><strong>{stats['highest_ob_country']}</strong> leads with
#             <strong>{stats['highest_ob_pct']:.1f}%</strong> adult obesity —
#             driven by high-calorie diets, sedentary lifestyles and rapid urbanisation.</p>
#         </div>""", unsafe_allow_html=True)
#     with col_b:
#         st.markdown(f"""
#         <div class="insight-box-blue">
#             <h3>🔵 Highest Malnutrition (2022)</h3>
#             <p><strong>{stats['highest_mn_country']}</strong> records the highest adult
#             undernutrition at <strong>{stats['highest_mn_pct']:.1f}%</strong> —
#             a stark reminder that food insecurity persists alongside rising obesity globally.</p>
#         </div>""", unsafe_allow_html=True)

#     st.markdown(f"""
#     <div class="insight-box">
#         <h3>💡 The Paradox — {stats['dual_burden_count']} countries carry both burdens simultaneously</h3>
#         <p>Rising obesity and persistent malnutrition are not opposing problems — they coexist in the
#         same countries, often in the same communities. This dual burden is driven by the shift toward
#         cheap, calorie-dense, nutrient-poor food systems, and demands integrated health policy responses.</p>
#     </div>""", unsafe_allow_html=True)

#     st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)

#     ob = load_obesity()
#     mn = load_malnutrition()

#     col1, col2 = st.columns(2)
#     with col1:
#         st.subheader("📈 Global Trend — Obesity vs Malnutrition")
#         if not ob.empty and not mn.empty:
#             st.plotly_chart(plot_dual_trend(ob, mn), use_container_width=True)
#     with col2:
#         st.subheader("🍩 Obesity Level Distribution")
#         if not ob.empty and "Obesity_Level" in ob.columns:
#             st.plotly_chart(plot_level_donut(ob, "Obesity_Level", "Obesity"),
#                             use_container_width=True)

#     st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)
#     st.subheader("⚖️ The Nutrition Paradox — Every Dot is a Country (2022)")
#     if not ob.empty and not mn.empty:
#         st.plotly_chart(plot_paradox_scatter(ob, mn, year=2022), use_container_width=True)
#     st.markdown("""
#     <div class="insight-box">
#         <h3>📌 How to read this chart</h3>
#         <p>Each dot is a country. The <strong>top-right quadrant</strong> represents the
#         <em>dual burden</em> — countries above the median on BOTH obesity and malnutrition.
#         Use the region legend to filter. Countries in this quadrant need integrated,
#         not siloed, public health strategies.</p>
#     </div>""", unsafe_allow_html=True)

#     st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)
#     col3, col4 = st.columns(2)
#     with col3:
#         st.subheader("🌐 Global Obesity Map (2022)")
#         if not ob.empty:
#             st.plotly_chart(plot_choropleth(ob, "Obesity", 2022), use_container_width=True)
#     with col4:
#         st.subheader("🌐 Global Malnutrition Map (2022)")
#         if not mn.empty:
#             st.plotly_chart(plot_choropleth(mn, "Malnutrition", 2022), use_container_width=True)


# # ═══════════════════════════════════════════════════════════════════════════
# # PAGE 2 — EDA
# # ═══════════════════════════════════════════════════════════════════════════
# elif page == "📊 EDA — Exploratory Analysis":

#     st.markdown("""
#     <div class="page-title">
#         <h2>📊 Exploratory Data Analysis</h2>
#         <p>Distribution checks, regional trends, gender gaps and data-quality diagnostics</p>
#     </div>""", unsafe_allow_html=True)

#     ob = load_obesity()
#     mn = load_malnutrition()
#     if ob.empty or mn.empty:
#         st.error("⚠️ Data not loaded. Make sure nutrition.db exists and tables are populated.")
#         st.stop()

#     tab1, tab2, tab3, tab4 = st.tabs(
#         ["🔴 Obesity EDA", "🔵 Malnutrition EDA", "🔗 Side-by-Side", "🔬 Data Quality"]
#     )

#     # ── Tab 1: Obesity ──────────────────────────────────────────────────
#     with tab1:
#         st.markdown("""
#         <div class="insight-box-red">
#             <h3>🔴 Obesity Dataset Overview</h3>
#             <p>Adult obesity (BMI ≥ 30) and child/adolescent overweight (BMI +2SD) — 2012 to 2022.</p>
#         </div>""", unsafe_allow_html=True)

#         c1, c2, c3 = st.columns(3)
#         c1.metric("Total Rows",      f"{len(ob):,}")
#         c2.metric("Unique Countries", ob["Country"].nunique())
#         c3.metric("Null Values",      int(ob.isnull().sum().sum()))

#         st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)
#         null_df = ob.isnull().sum().reset_index()
#         null_df.columns = ["Column", "Null Count"]
#         null_df = null_df[null_df["Null Count"] > 0]
#         if null_df.empty:
#             st.success("✅ No missing values in the obesity dataset.")
#         else:
#             st.dataframe(null_df, use_container_width=True)

#         col1, col2 = st.columns(2)
#         with col1:
#             st.subheader("📈 Global Obesity Trend")
#             trend = ob[ob["Gender"]=="Both"].groupby("Year")["Mean_Estimate"].mean().reset_index()
#             fig = px.line(trend, x="Year", y="Mean_Estimate", markers=True,
#                           color_discrete_sequence=["#ef4444"])
#             fig.update_traces(line_width=3, marker_size=8)
#             fig.update_layout(**_DARK, yaxis_title="Avg Obesity (%)", hovermode="x unified")
#             st.plotly_chart(fig, use_container_width=True)
#         with col2:
#             st.subheader("📦 Regional Spread")
#             st.plotly_chart(plot_region_boxplot(ob, "Obesity"), use_container_width=True)

#         col3, col4 = st.columns(2)
#         with col3:
#             st.subheader("⚧ Gender Gap by Region")
#             st.plotly_chart(plot_gender_gap(ob, "Obesity"), use_container_width=True)
#         with col4:
#             st.subheader("👶 Adults vs Children")
#             st.plotly_chart(plot_age_group_bar(ob, "Obesity"), use_container_width=True)

#         st.subheader("🔥 CI Width Heatmap — Region × Age")
#         st.plotly_chart(plot_ci_heatmap(ob, "Obesity"), use_container_width=True)

#     # ── Tab 2: Malnutrition ─────────────────────────────────────────────
#     with tab2:
#         st.markdown("""
#         <div class="insight-box-blue">
#             <h3>🔵 Malnutrition Dataset Overview</h3>
#             <p>Adult underweight (BMI < 18.5) and child thinness (BMI −2SD) — 2012 to 2022.</p>
#         </div>""", unsafe_allow_html=True)

#         c1, c2, c3 = st.columns(3)
#         c1.metric("Total Rows",      f"{len(mn):,}")
#         c2.metric("Unique Countries", mn["Country"].nunique())
#         c3.metric("Null Values",      int(mn.isnull().sum().sum()))

#         st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)

#         col1, col2 = st.columns(2)
#         with col1:
#             st.subheader("📈 Global Malnutrition Trend")
#             trend_mn = mn[mn["Gender"]=="Both"].groupby("Year")["Mean_Estimate"].mean().reset_index()
#             fig = px.line(trend_mn, x="Year", y="Mean_Estimate", markers=True,
#                           color_discrete_sequence=["#3b82f6"])
#             fig.update_traces(line_width=3, marker_size=8)
#             fig.update_layout(**_DARK, yaxis_title="Avg Malnutrition (%)", hovermode="x unified")
#             st.plotly_chart(fig, use_container_width=True)
#         with col2:
#             st.subheader("📦 Regional Spread")
#             st.plotly_chart(plot_region_boxplot(mn, "Malnutrition"), use_container_width=True)

#         col3, col4 = st.columns(2)
#         with col3:
#             st.subheader("⚧ Gender Gap by Region")
#             st.plotly_chart(plot_gender_gap(mn, "Malnutrition"), use_container_width=True)
#         with col4:
#             st.subheader("👶 Adults vs Children")
#             st.plotly_chart(plot_age_group_bar(mn, "Malnutrition"), use_container_width=True)

#         st.subheader("🔥 CI Width Heatmap — Region × Age")
#         st.plotly_chart(plot_ci_heatmap(mn, "Malnutrition"), use_container_width=True)

#     # ── Tab 3: Side-by-side ─────────────────────────────────────────────
#     with tab3:
#         st.subheader("🔗 Obesity vs Malnutrition by Region")
#         st.plotly_chart(plot_grouped_bar(ob, mn, "Region"), use_container_width=True)
#         st.subheader("⚧ Gender Disparity Across Both Conditions")
#         st.plotly_chart(plot_grouped_bar(ob, mn, "Gender"), use_container_width=True)
#         st.subheader("⚖️ Paradox Scatter — Select Year")
#         yr = st.slider("Year", 2012, 2022, 2022, key="eda_yr")
#         st.plotly_chart(plot_paradox_scatter(ob, mn, year=yr), use_container_width=True)

#     # ── Tab 4: Data Quality ─────────────────────────────────────────────
#     with tab4:
#         st.markdown("""
#         <div class="insight-box">
#             <h3>📌 CI Width = UpperBound − LowerBound</h3>
#             <p>A wider confidence interval means a less reliable estimate. Regions with
#             high CI Width AND high disease burden are where intervention is most needed
#             — and hardest to target accurately.</p>
#         </div>""", unsafe_allow_html=True)

#         col1, col2 = st.columns(2)
#         with col1:
#             st.markdown("**Obesity CI Width Heatmap**")
#             st.plotly_chart(plot_ci_heatmap(ob, "Obesity"), use_container_width=True)
#         with col2:
#             st.markdown("**Malnutrition CI Width Heatmap**")
#             st.plotly_chart(plot_ci_heatmap(mn, "Malnutrition"), use_container_width=True)

#         st.subheader("📋 Descriptive Statistics")
#         col1, col2 = st.columns(2)
#         with col1:
#             st.markdown("**Obesity**")
#             st.dataframe(ob[["Mean_Estimate","LowerBound","UpperBound","CI_Width"]]
#                          .describe().round(2), use_container_width=True)
#         with col2:
#             st.markdown("**Malnutrition**")
#             st.dataframe(mn[["Mean_Estimate","LowerBound","UpperBound","CI_Width"]]
#                          .describe().round(2), use_container_width=True)


# # ═══════════════════════════════════════════════════════════════════════════
# # PAGE 3 — OBESITY QUERIES
# # ═══════════════════════════════════════════════════════════════════════════
# elif page == "🔴 Obesity Queries":

#     st.markdown("""
#     <div class="page-title">
#         <h2>🔴 Obesity Queries — Q1 to Q10</h2>
#         <p>10 SQL queries on the obesity table — each with a chart and glowing insight box</p>
#     </div>""", unsafe_allow_html=True)

#     col1, col2 = st.columns([3, 1])
#     with col1:
#         selected_q = st.selectbox("Select Query", list(OBESITY_QUERIES.keys()),
#                                   key="ob_sel")
#     with col2:
#         st.markdown("<br/>", unsafe_allow_html=True)
#         run_all = st.checkbox("Run all 10", key="ob_all")

#     st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)

#     if run_all:
#         for qn in OBESITY_QUERIES:
#             st.markdown(f"### {qn}")
#             render_query_section(qn)
#             st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)
#     else:
#         st.markdown(f"### {selected_q}")
#         render_query_section(selected_q)

#     st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)
#     st.markdown("""
#     <div class="page-title">
#         <h2>📊 Additional Obesity Charts</h2>
#         <p>Pre-rendered from the full obesity dataset</p>
#     </div>""", unsafe_allow_html=True)

#     ob = load_obesity()
#     if not ob.empty:
#         col1, col2 = st.columns(2)
#         with col1:
#             yr = st.selectbox("Filter by year", [None] + list(range(2012, 2023)),
#                               format_func=lambda x: "All years" if x is None else str(x),
#                               key="ob_yr")
#             st.plotly_chart(plot_top_countries(ob, 10, "Obesity", yr),
#                             use_container_width=True)
#         with col2:
#             st.plotly_chart(plot_gender_gap(ob, "Obesity"), use_container_width=True)
#         st.plotly_chart(plot_choropleth(ob, "Obesity", 2022), use_container_width=True)


# # ═══════════════════════════════════════════════════════════════════════════
# # PAGE 4 — MALNUTRITION QUERIES
# # ═══════════════════════════════════════════════════════════════════════════
# elif page == "🔵 Malnutrition Queries":

#     st.markdown("""
#     <div class="page-title">
#         <h2>🔵 Malnutrition Queries — Q11 to Q20</h2>
#         <p>10 SQL queries on the malnutrition table — each with a chart and glowing insight box</p>
#     </div>""", unsafe_allow_html=True)

#     col1, col2 = st.columns([3, 1])
#     with col1:
#         selected_q = st.selectbox("Select Query", list(MALN_QUERIES.keys()),
#                                   key="mn_sel")
#     with col2:
#         st.markdown("<br/>", unsafe_allow_html=True)
#         run_all_mn = st.checkbox("Run all 10", key="mn_all")

#     st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)

#     if run_all_mn:
#         for qn in MALN_QUERIES:
#             st.markdown(f"### {qn}")
#             render_query_section(qn)
#             st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)
#     else:
#         st.markdown(f"### {selected_q}")
#         render_query_section(selected_q)

#     st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)
#     st.markdown("""
#     <div class="page-title">
#         <h2>📊 Additional Malnutrition Charts</h2>
#         <p>Pre-rendered from the full malnutrition dataset</p>
#     </div>""", unsafe_allow_html=True)

#     mn = load_malnutrition()
#     if not mn.empty:
#         col1, col2 = st.columns(2)
#         with col1:
#             st.plotly_chart(plot_top_countries(mn, 10, "Malnutrition"),
#                             use_container_width=True)
#         with col2:
#             st.plotly_chart(plot_gender_gap(mn, "Malnutrition"), use_container_width=True)

#         mn19, _ = run_query(QUERIES["Q19 · Min / Max malnutrition year-wise"])
#         if mn19 is not None:
#             st.plotly_chart(plot_min_max_band(mn19, "Malnutrition"), use_container_width=True)
#         st.plotly_chart(plot_choropleth(mn, "Malnutrition", 2022), use_container_width=True)


# # ═══════════════════════════════════════════════════════════════════════════
# # PAGE 5 — COMBINED QUERIES
# # ═══════════════════════════════════════════════════════════════════════════
# elif page == "🔗 Combined Queries":

#     st.markdown("""
#     <div class="page-title">
#         <h2>🔗 Combined Queries — Q21 to Q25</h2>
#         <p>5 JOIN queries that reveal the nutrition paradox across countries, regions and demographics</p>
#     </div>""", unsafe_allow_html=True)

#     st.markdown("""
#     <div class="insight-box">
#         <h3>💡 Why these queries matter</h3>
#         <p>These five queries JOIN the obesity and malnutrition tables — uncovering countries that
#         face both burdens simultaneously, how gender shapes both conditions, and which nations are
#         in active nutritional transition from undernutrition to overnutrition.</p>
#     </div>""", unsafe_allow_html=True)

#     col1, col2 = st.columns([3, 1])
#     with col1:
#         selected_q = st.selectbox("Select Query", list(COMBINED_QUERIES.keys()),
#                                   key="comb_sel")
#     with col2:
#         st.markdown("<br/>", unsafe_allow_html=True)
#         run_all_c = st.checkbox("Run all 5", key="comb_all")

#     st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)

#     if run_all_c:
#         for qn in COMBINED_QUERIES:
#             st.markdown(f"### {qn}")
#             render_query_section(qn)
#             st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)
#     else:
#         st.markdown(f"### {selected_q}")
#         render_query_section(selected_q)

#     # ── Q24 spotlight ─────────────────────────────────────────────────
#     st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)
#     st.markdown("""
#     <div class="page-title">
#         <h2>🔁 Nutritional Transition Countries</h2>
#         <p>Q24 — Obesity rising AND malnutrition falling simultaneously</p>
#     </div>""", unsafe_allow_html=True)

#     df24, _ = run_query(QUERIES["Q24 · Rising obesity + falling malnutrition (transition countries)"])
#     if df24 is not None and len(df24):
#         fig24 = go.Figure(data=[
#             go.Bar(name="↑ Obesity Rise",      x=df24["Country"], y=df24["ob_change"],
#                    marker_color="#ef4444",
#                    text=df24["ob_change"].round(1),
#                    texttemplate="+%{text}%", textposition="outside"),
#             go.Bar(name="↓ Malnutrition Drop", x=df24["Country"], y=df24["mn_drop"],
#                    marker_color="#10b981",
#                    text=df24["mn_drop"].round(1),
#                    texttemplate="-%{text}%", textposition="outside"),
#         ])
#         fig24.update_layout(**_DARK,
#                             barmode="group",
#                             title="Countries in Nutritional Transition (2012–2022)",
#                             xaxis_tickangle=-35, yaxis_title="Change in %",
#                             legend=dict(orientation="h", yanchor="bottom", y=1.02))
#         st.plotly_chart(fig24, use_container_width=True)

#     st.markdown("""
#     <div class="insight-box-green">
#         <h3>🔗 The Transition Story</h3>
#         <p>Transition countries are winning the malnutrition battle but losing the obesity one.
#         Economic development solves chronic food scarcity but introduces new diet-quality problems
#         as cheaper, calorie-dense processed foods replace traditional diets. Brazil's trajectory —
#         the largest malnutrition drop alongside a moderate obesity rise — reflects its sustained
#         social protection programmes (Bolsa Família).</p>
#     </div>""", unsafe_allow_html=True)

#     ob = load_obesity()
#     mn = load_malnutrition()
#     if not ob.empty and not mn.empty:
#         st.subheader("📊 Obesity vs Malnutrition by Region")
#         st.plotly_chart(plot_grouped_bar(ob, mn, "Region"), use_container_width=True)
#         st.subheader("⚧ Gender Disparity — Both Conditions")
#         st.plotly_chart(plot_grouped_bar(ob, mn, "Gender"), use_container_width=True)


# # ═══════════════════════════════════════════════════════════════════════════
# # PAGE 6 — COUNTRY DEEP-DIVE
# # ═══════════════════════════════════════════════════════════════════════════
# elif page == "🌍 Country Deep-Dive":

#     st.markdown("""
#     <div class="page-title">
#         <h2>🌍 Country Deep-Dive</h2>
#         <p>Full obesity & malnutrition profile for any country across all years, genders and age groups</p>
#     </div>""", unsafe_allow_html=True)

#     ob = load_obesity()
#     mn = load_malnutrition()

#     all_countries = sorted(
#         set(ob["Country"].dropna().unique()) | set(mn["Country"].dropna().unique())
#     )

#     col_sel, col_age = st.columns([3, 1])
#     with col_sel:
#         country = st.selectbox(
#             "Choose a country", all_countries,
#             index=all_countries.index("India") if "India" in all_countries else 0,
#         )
#     with col_age:
#         age_filter = st.selectbox("Age group",
#                                   ["All", "Adult", "Child/Adolescent"],
#                                   key="dd_age")

#     ob_c = ob[ob["Country"] == country].copy()
#     mn_c = mn[mn["Country"] == country].copy()
#     if age_filter != "All":
#         ob_c = ob_c[ob_c["Age_Group"] == age_filter]
#         mn_c = mn_c[mn_c["Age_Group"] == age_filter]

#     st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)

#     ob22 = ob_c[(ob_c["Year"]==2022)&(ob_c["Gender"]=="Both")]["Mean_Estimate"].mean()
#     mn22 = mn_c[(mn_c["Year"]==2022)&(mn_c["Gender"]=="Both")]["Mean_Estimate"].mean()
#     ob12 = ob_c[(ob_c["Year"]==2012)&(ob_c["Gender"]=="Both")]["Mean_Estimate"].mean()
#     mn12 = mn_c[(mn_c["Year"]==2012)&(mn_c["Gender"]=="Both")]["Mean_Estimate"].mean()

#     c1, c2, c3, c4 = st.columns(4)
#     c1.metric("🔴 Obesity 2022",      f"{ob22:.1f}%" if not pd.isna(ob22) else "N/A",
#               delta=f"{ob22-ob12:+.1f}% since 2012" if not (pd.isna(ob22) or pd.isna(ob12)) else None)
#     c2.metric("🔵 Malnutrition 2022", f"{mn22:.1f}%" if not pd.isna(mn22) else "N/A",
#               delta=f"{mn22-mn12:+.1f}% since 2012" if not (pd.isna(mn22) or pd.isna(mn12)) else None)
#     c3.metric("🌐 Region",  ob_c["Region"].mode()[0] if not ob_c.empty else "—")
#     c4.metric("📅 Data Points", f"{len(ob_c)+len(mn_c):,}")

#     # Dynamic insight box based on actual country numbers
#     if not (pd.isna(ob22) or pd.isna(mn22)):
#         if ob22 > 15 and mn22 > 10:
#             st.markdown(f"""
#             <div class="insight-box">
#                 <h3>⚠️ Dual Burden — {country}</h3>
#                 <p><strong>{country}</strong> shows elevated obesity (<strong>{ob22:.1f}%</strong>)
#                 alongside significant malnutrition (<strong>{mn22:.1f}%</strong>) — a dual-burden
#                 nation requiring integrated, not siloed, public health policy.</p>
#             </div>""", unsafe_allow_html=True)
#         elif ob22 > 25:
#             st.markdown(f"""
#             <div class="insight-box-red">
#                 <h3>🔴 High Obesity Alert — {country}</h3>
#                 <p>Obesity at <strong>{ob22:.1f}%</strong> in 2022 is well above the global average.
#                 Priority: dietary education, urban food environment reform, physical activity promotion.</p>
#             </div>""", unsafe_allow_html=True)
#         elif mn22 > 20:
#             st.markdown(f"""
#             <div class="insight-box-blue">
#                 <h3>🔵 High Malnutrition Alert — {country}</h3>
#                 <p>Malnutrition at <strong>{mn22:.1f}%</strong> signals persistent food insecurity.
#                 Priority: social protection programmes, school feeding, agricultural investment.</p>
#             </div>""", unsafe_allow_html=True)
#         else:
#             st.markdown(f"""
#             <div class="insight-box-green">
#                 <h3>✅ Relatively Balanced — {country}</h3>
#                 <p>Obesity at <strong>{ob22:.1f}%</strong> and malnutrition at
#                 <strong>{mn22:.1f}%</strong> are both below major alert thresholds in 2022.
#                 Continued monitoring recommended.</p>
#             </div>""", unsafe_allow_html=True)

#     st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)

#     col1, col2 = st.columns(2)
#     with col1:
#         st.subheader(f"🔴 Obesity Trend — {country}")
#         ob_t = (ob_c[ob_c["Gender"]=="Both"]
#                 .groupby("Year")["Mean_Estimate"].mean().reset_index())
#         if not ob_t.empty:
#             fig = px.line(ob_t, x="Year", y="Mean_Estimate", markers=True,
#                           color_discrete_sequence=["#ef4444"])
#             fig.update_traces(line_width=3, marker_size=9)
#             fig.update_layout(**_DARK, yaxis_title="Obesity (%)", hovermode="x unified")
#             st.plotly_chart(fig, use_container_width=True)
#         else:
#             st.info("No obesity data for this selection.")

#     with col2:
#         st.subheader(f"🔵 Malnutrition Trend — {country}")
#         mn_t = (mn_c[mn_c["Gender"]=="Both"]
#                 .groupby("Year")["Mean_Estimate"].mean().reset_index())
#         if not mn_t.empty:
#             fig2 = px.line(mn_t, x="Year", y="Mean_Estimate", markers=True,
#                            color_discrete_sequence=["#3b82f6"])
#             fig2.update_traces(line_width=3, marker_size=9)
#             fig2.update_layout(**_DARK, yaxis_title="Malnutrition (%)", hovermode="x unified")
#             st.plotly_chart(fig2, use_container_width=True)
#         else:
#             st.info("No malnutrition data for this selection.")

#     st.subheader(f"⚧ Gender Breakdown — {country}")
#     col3, col4 = st.columns(2)
#     with col3:
#         ob_g = (ob_c[ob_c["Gender"].isin(["Male","Female"])]
#                 .groupby(["Year","Gender"])["Mean_Estimate"].mean().reset_index())
#         if not ob_g.empty:
#             fig3 = px.line(ob_g, x="Year", y="Mean_Estimate", color="Gender",
#                            markers=True,
#                            color_discrete_map={"Male":"#3b82f6","Female":"#f472b6"})
#             fig3.update_layout(**_DARK, title="Obesity by Gender", hovermode="x unified")
#             st.plotly_chart(fig3, use_container_width=True)
#     with col4:
#         mn_g = (mn_c[mn_c["Gender"].isin(["Male","Female"])]
#                 .groupby(["Year","Gender"])["Mean_Estimate"].mean().reset_index())
#         if not mn_g.empty:
#             fig4 = px.line(mn_g, x="Year", y="Mean_Estimate", color="Gender",
#                            markers=True,
#                            color_discrete_map={"Male":"#3b82f6","Female":"#f472b6"})
#             fig4.update_layout(**_DARK, title="Malnutrition by Gender", hovermode="x unified")
#             st.plotly_chart(fig4, use_container_width=True)

#     st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)
#     st.subheader(f"📋 Raw Data — {country}")
#     tab_ob, tab_mn = st.tabs(["Obesity Records", "Malnutrition Records"])
#     with tab_ob:
#         if not ob_c.empty:
#             st.dataframe(ob_c.sort_values(["Year","Gender"]),
#                          use_container_width=True, height=350)
#             st.download_button("📥 Download", ob_c.to_csv(index=False),
#                                file_name=f"{country}_obesity.csv")
#         else:
#             st.info("No obesity records for this filter.")
#     with tab_mn:
#         if not mn_c.empty:
#             st.dataframe(mn_c.sort_values(["Year","Gender"]),
#                          use_container_width=True, height=350)
#             st.download_button("📥 Download", mn_c.to_csv(index=False),
#                                file_name=f"{country}_malnutrition.csv")
#         else:
#             st.info("No malnutrition records for this filter.")

# # ═══════════════════════════════════════════════════════════════════════════
# # FOOTER
# # ═══════════════════════════════════════════════════════════════════════════
# st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)
# st.markdown("""
# <div style='text-align:center; color:#64748b; font-size:0.8rem; padding:8px 0 16px;'>
#     <strong style='color:#667eea'>⚖️ Nutrition Paradox</strong> &nbsp;|&nbsp;
#     Data: WHO Global Health Observatory API &nbsp;|&nbsp;
#     Period: 2012–2022 &nbsp;|&nbsp;
#     Built with Streamlit · Plotly · SQLite · Python
# </div>""", unsafe_allow_html=True)










































































import os, sys
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ── Make app/ importable regardless of launch directory ──────────────────
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sql.queries import QUERIES, QUERY_META
from db_utils    import run_query, load_obesity, load_malnutrition, get_dashboard_stats
from viz_utils   import (
    plot_dual_trend, plot_top_countries, plot_gender_gap,
    plot_region_boxplot, plot_paradox_scatter, plot_ci_heatmap,
    plot_country_comparison, plot_age_group_bar, plot_grouped_bar,
    plot_level_donut, plot_choropleth, plot_min_max_band,
)

# ═══════════════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="⚖️ Nutrition Paradox",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════════════════════════════
# CSS  — same glowing-box style as NASA NEO project
# ═══════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }


.stApp{
    background:
        linear-gradient(
            135deg,
            #1e293b 0%,
            #243447 50%,
            #334155 100%
        );

    background-attachment: fixed;
}

.main-header{
    font-size:4rem;
    font-weight:800;
    text-align:center;

    background:
        linear-gradient(
            90deg,
            #4DA3FF,
            #2ECC71,
            #4DA3FF
        );

    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    background-clip:text;

    margin-bottom:0;
    line-height:1.1;
}
            
.metric-card{
    background: rgba(255,255,255,0.05);

    backdrop-filter: blur(20px);

    border:1px solid rgba(255,255,255,0.08);

    border-radius:20px;

    padding:22px;

    text-align:center;

    transition:all .3s ease;

    box-shadow:
        0 8px 24px rgba(0,0,0,0.30);
}

.metric-card:hover{
    transform:translateY(-5px);

    box-shadow:
        0 15px 35px rgba(77,163,255,0.25);
}

.metric-title{
    color:#94a3b8;
    font-size:0.95rem;
    font-weight:600;
}

.metric-value{
    color:white;
    font-size:2rem;
    font-weight:700;
}
            
.glass-card{
    background: rgba(255,255,255,0.04);

    backdrop-filter: blur(20px);

    border:1px solid rgba(255,255,255,0.08);

    border-radius:24px;

    padding:24px;

    margin-bottom:24px;

    box-shadow:
        0 8px 24px rgba(0,0,0,0.25);
}

.insight-box{
    background:
        linear-gradient(
            135deg,
            #4DA3FF,
            #2ECC71
        );

    padding:20px 24px;

    border-radius:16px;

    color:white;

    box-shadow:
        0 10px 24px rgba(46,204,113,0.20);

    transition:all 0.3s ease;
}

.insight-box:hover{
    transform:translateY(-5px);
    box-shadow:
        0 18px 40px rgba(46,204,113,0.30);
}

.insight-box-red{
    transition:all .3s ease;
}

.insight-box-red:hover{
    transform:translateY(-5px);
}

.insight-box-blue{
    transition:all .3s ease;
}

.insight-box-blue:hover{
    transform:translateY(-5px);
}

.insight-box-green{
    transition:all .3s ease;
}

.insight-box-green:hover{
    transform:translateY(-5px);
}

           
.sub-header{
    text-align:center;
    color:#94a3b8;
    font-size:1.15rem;
    margin-bottom:2rem;
}

/* ── Glowing insight boxes ── */
.insight-box {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 18px 22px; border-radius: 12px; color: white; margin: 14px 0;
    box-shadow: 0 0 18px rgba(102,126,234,0.45);
}
.insight-box h3  { margin: 0 0 8px; font-size: 1rem; font-weight: 600; letter-spacing:.02em; }
.insight-box p   { margin: 0; font-size: 0.88rem; line-height: 1.6; opacity: 0.95; }

.insight-box-red {
    background: linear-gradient(135deg, #ef4444 0%, #b91c1c 100%);
    padding: 18px 22px; border-radius: 12px; color: white; margin: 14px 0;
    box-shadow: 0 0 18px rgba(239,68,68,0.40);
}
.insight-box-red h3 { margin: 0 0 8px; font-size: 1rem; font-weight: 600; }
.insight-box-red p  { margin: 0; font-size: 0.88rem; line-height: 1.6; opacity: 0.95; }

.insight-box-blue {
    background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
    padding: 18px 22px; border-radius: 12px; color: white; margin: 14px 0;
    box-shadow: 0 0 18px rgba(59,130,246,0.40);
}
.insight-box-blue h3 { margin: 0 0 8px; font-size: 1rem; font-weight: 600; }
.insight-box-blue p  { margin: 0; font-size: 0.88rem; line-height: 1.6; opacity: 0.95; }

.insight-box-green {
    background: linear-gradient(135deg, #10b981 0%, #065f46 100%);
    padding: 18px 22px; border-radius: 12px; color: white; margin: 14px 0;
    box-shadow: 0 0 18px rgba(16,185,129,0.40);
}
.insight-box-green h3 { margin: 0 0 8px; font-size: 1rem; font-weight: 600; }
.insight-box-green p  { margin: 0; font-size: 0.88rem; line-height: 1.6; opacity: 0.95; }

            
.insight-box{
    background:
        linear-gradient(
            135deg,
            #4DA3FF,
            #2ECC71
        );

    padding:20px 24px;

    border-radius:16px;

    color:white;

    box-shadow:
        0 10px 24px rgba(46,204,113,0.20);

    transition:all 0.3s ease;
}

.insight-box:hover{
    transform:translateY(-5px);
    box-shadow:
        0 18px 40px rgba(46,204,113,0.30);
}

.insight-box-red{
    transition:all .3s ease;
}

.insight-box-red:hover{
    transform:translateY(-5px);
}

.insight-box-blue{
    transition:all .3s ease;
}

.insight-box-blue:hover{
    transform:translateY(-5px);
}

.insight-box-green{
    transition:all .3s ease;
}

.insight-box-green:hover{
    transform:translateY(-5px);
}

            .insight-box,
.insight-box-blue,
.insight-box-red,
.insight-box-green{

    transition:all .3s ease;
}

.insight-box:hover,
.insight-box-blue:hover,
.insight-box-red:hover,
.insight-box-green:hover{

    transform:translateY(-5px);

    box-shadow:
        0 18px 35px rgba(0,0,0,0.25);
}           


# /* ── Page title strip ── */       
.page-title{
    background:
        linear-gradient(
            90deg,
            rgba(77,163,255,0.15),
            transparent
        );

    border-left:4px solid #4DA3FF;

    padding:12px 18px;

    border-radius:0 10px 10px 0;
}

.page-title h2{
    color:#f8fafc;
}

.page-title p{
    color:#94a3b8;
}
            
.section-divider { border: none; border-top: 1px solid rgba(102,126,234,0.25); margin: 20px 0; }

/* ── Sidebar ── */
[data-testid="stSidebar"]{
    background:
        linear-gradient(
            180deg,
            #020617 0%,
            #0f172a 50%,
            #020617 100%
        );

    border-right:
        1px solid rgba(255,255,255,0.05);
}
[data-testid="stSidebar"] .stMarkdown { color: #94a3b8; }
[data-testid="stSidebar"] hr { border-color: rgba(102,126,234,0.25); }

button[data-baseweb="tab"][aria-selected="true"] {
    color: #667eea !important;
    border-bottom: 2px solid #667eea !important;
}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
# PRE-BUILT QUERY GROUPS  using QUERY_META["category"]
# (no regex — clean and reliable)
# ═══════════════════════════════════════════════════════════════════════════
OBESITY_QUERIES    = {k: v for k, v in QUERIES.items()
                      if QUERY_META.get(k, {}).get("category") == "obesity"}
MALN_QUERIES       = {k: v for k, v in QUERIES.items()
                      if QUERY_META.get(k, {}).get("category") == "malnutrition"}
COMBINED_QUERIES   = {k: v for k, v in QUERIES.items()
                      if QUERY_META.get(k, {}).get("category") == "combined"}

# ═══════════════════════════════════════════════════════════════════════════
# CHART BUILDER  using QUERY_META (chart_type / x / y / color_col)
# ═══════════════════════════════════════════════════════════════════════════
_DARK = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#e2e8f0", family="Inter, sans-serif", size=12),
    margin=dict(l=10, r=10, t=50, b=10),
    hoverlabel=dict(bgcolor="#1e1b4b", font_color="white"),
)

_CAT_COLOR = {
    "obesity":      "#ef4444",
    "malnutrition": "#3b82f6",
    "combined":     "#10b981",
}

def _meta_chart(df: pd.DataFrame, query_name: str):
    """
    Build the best Plotly figure for a query result using QUERY_META.
    Returns None for chart_type='table' (already shown as DataFrame).
    """
    meta       = QUERY_META.get(query_name, {})
    chart_type = meta.get("chart_type", "bar")
    x_col      = meta.get("x")
    y_col      = meta.get("y")          # str or list[str]
    color_col  = meta.get("color_col")
    category   = meta.get("category", "obesity")
    base_color = _CAT_COLOR.get(category, "#667eea")

    if chart_type == "table":
        return None

    if df is None or df.empty:
        return None

    # ── Validate columns exist ────────────────────────────────────────
    y_cols = y_col if isinstance(y_col, list) else [y_col]
    missing = [c for c in ([x_col] + y_cols + ([color_col] if color_col else []))
               if c and c not in df.columns]
    if missing:
        # Graceful fallback: pick first num + first cat column
        num = df.select_dtypes(include="number").columns.tolist()
        cat = df.select_dtypes(exclude="number").columns.tolist()
        if not num:
            return None
        x_col, y_col, color_col = (cat[0] if cat else df.columns[0]), num[0], None
        chart_type = "bar"
        y_cols = [y_col]

    # ── LINE ──────────────────────────────────────────────────────────
    if chart_type == "line":
        if color_col and color_col in df.columns:
            fig = px.line(df, x=x_col, y=y_cols[0], color=color_col,
                          markers=True,
                          color_discrete_sequence=px.colors.qualitative.Pastel)
        else:
            fig = px.line(df, x=x_col, y=y_cols[0], markers=True,
                          color_discrete_sequence=[base_color])
        fig.update_traces(line_width=3, marker_size=8)
        fig.update_layout(**_DARK, hovermode="x unified",
                          yaxis_title=y_cols[0].replace("_", " ").title(),
                          legend=dict(orientation="h", yanchor="bottom", y=1.02))
        return fig

    # ── GROUPED_BAR (y is a list, e.g. ["avg_obesity","avg_malnutrition"]) ─
    if chart_type == "grouped_bar":
        fig = go.Figure()
        colors_gb = ["#ef4444", "#3b82f6", "#10b981", "#f59e0b"]
        for i, yc in enumerate(y_cols):
            if yc in df.columns:
                fig.add_bar(x=df[x_col], y=df[yc],
                            name=yc.replace("_", " ").title(),
                            marker_color=colors_gb[i % len(colors_gb)],
                            text=df[yc].round(1),
                            texttemplate="%{text}%", textposition="outside")
        fig.update_layout(**_DARK, barmode="group",
                          xaxis_tickangle=-20, yaxis_title="Average (%)",
                          legend=dict(orientation="h", yanchor="bottom", y=1.02))
        return fig

    # ── BAR (default) ────────────────────────────────────────────────
    if color_col and color_col in df.columns:
        # categorical color
        fig = px.bar(df, x=x_col, y=y_cols[0], color=color_col, barmode="group",
                     text=y_cols[0],
                     color_discrete_sequence=px.colors.qualitative.Pastel)
    else:
        fig = px.bar(
            df.sort_values(y_cols[0], ascending=True) if len(df) <= 20 else df,
            x=y_cols[0] if len(df) <= 20 else x_col,
            y=x_col     if len(df) <= 20 else y_cols[0],
            orientation="h" if len(df) <= 20 else "v",
            color=y_cols[0],
            color_continuous_scale=[[0, "#1e1b4b"], [0.5, base_color], [1, "#fff"]],
            text=y_cols[0],
        )
        fig.update_layout(coloraxis_showscale=False)
    fig.update_traces(texttemplate="%{text}", textposition="outside")
    fig.update_layout(**_DARK, xaxis_tickangle=-25 if len(df) > 6 else 0,
                      yaxis_title=y_cols[0].replace("_", " ").title())
    return fig

# ═══════════════════════════════════════════════════════════════════════════
# INSIGHT BOX  — reads from QUERY_META["insight"] + ["category"]
# ═══════════════════════════════════════════════════════════════════════════
def insight_box(query_name: str) -> None:
    meta     = QUERY_META.get(query_name, {})
    text     = meta.get("insight", "")
    category = meta.get("category", "")
    if not text:
        return
    if category == "obesity":
        box_cls, label = "insight-box-red",   "🔴 Obesity Insight"
    elif category == "malnutrition":
        box_cls, label = "insight-box-blue",  "🔵 Malnutrition Insight"
    elif category == "combined":
        box_cls, label = "insight-box-green", "🔗 Combined Insight"
    else:
        box_cls, label = "insight-box",       "💡 Key Insight"
    st.markdown(f"""
    <div class="{box_cls}">
        <h3>{label}</h3>
        <p>{text}</p>
    </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
# QUERY SECTION RENDERER  (used on all 3 query pages)
# ═══════════════════════════════════════════════════════════════════════════
def render_query_section(query_name: str) -> None:
    """
    SQL expander → Run button → success badge → DataFrame →
    Download CSV → glowing insight box → QUERY_META-driven chart.
    """
    sql  = QUERIES[query_name]
    meta = QUERY_META.get(query_name, {})

    with st.expander("📝 View SQL", expanded=False):
        st.code(sql, language="sql")

    run = st.button("▶️ Run Query", key=f"run__{query_name}", type="primary")

    if run:
        with st.spinner("Querying database…"):
            df, err = run_query(sql)
        if err:
            st.error(f"❌ Error: {err}")
            return

        st.success(f"✅ {len(df):,} rows returned")
        st.dataframe(df, use_container_width=True,
                     height=min(380, 55 + 35 * len(df)))

        col_dl, _ = st.columns([1, 5])
        col_dl.download_button(
            "📥 Download CSV", df.to_csv(index=False),
            file_name=f"{query_name[:40].strip()}.csv", mime="text/csv",
        )

        # Insight box
        insight_box(query_name)

        # Chart (skipped if chart_type == "table")
        if meta.get("chart_type") != "table":
            fig = _meta_chart(df, query_name)
            if fig:
                st.plotly_chart(fig, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════
# SIDEBAR NAVIGATION
# ═══════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:10px 0 6px;'>
        <span style='font-size:2.4rem'>⚖️</span>
        <div style='font-size:1.05rem; font-weight:700; color:#667eea; margin-top:4px;'>
            Nutrition Paradox
        </div>
        <div style='font-size:0.75rem; color:#64748b; margin-top:2px;'>
            WHO Global Health Analytics
        </div>
    </div>""", unsafe_allow_html=True)
    st.markdown("<hr/>", unsafe_allow_html=True)

    page = st.radio(
        "Navigate",
        [
            "🏠 Overview",
            "📊 EDA — Exploratory Analysis",
            "🔴 Obesity Queries",
            "🔵 Malnutrition Queries",
            "🔗 Combined Queries",
            "🌍 Country Deep-Dive",
        ],
        label_visibility="collapsed",
    )

    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:0.75rem; color:#64748b; padding:4px 0;'>
        <b style='color:#94a3b8'>Data source:</b> WHO GHO API<br>
        <b style='color:#94a3b8'>Period:</b> 2012 – 2022<br>
        <b style='color:#94a3b8'>Indicators:</b> BMI-based<br>
        <b style='color:#94a3b8'>Engine:</b> SQLite + Streamlit
    </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# PAGE 1 — OVERVIEW
# ═══════════════════════════════════════════════════════════════════════════
if page == "🏠 Overview":

    st.markdown('<h1 class="main-header">⚖️ Nutrition Paradox</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">A Global View on Obesity & Malnutrition — WHO Data 2012–2022</p>',
                unsafe_allow_html=True)
    st.markdown("---")

    stats = get_dashboard_stats()
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("📋 Obesity Records",       f"{stats['obesity_records']:,}")
    c2.metric("📋 Malnutrition Records",  f"{stats['malnutrition_records']:,}")
    c3.metric("🌐 Countries Tracked",     f"{stats['countries']:,}")
    c4.metric("⚠️ Dual Burden Nations",   f"{stats['dual_burden_count']:,}",
              help="Countries where both avg obesity AND malnutrition > 10%")
    c5.metric("📅 Years Covered",         stats["years_covered"])

    st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(f"""
        <div class="insight-box-red">
            <h3>🔴 Highest Obesity (2022)</h3>
            <p><strong>{stats['highest_ob_country']}</strong> leads with
            <strong>{stats['highest_ob_pct']:.1f}%</strong> adult obesity —
            driven by high-calorie diets, sedentary lifestyles and rapid urbanisation.</p>
        </div>""", unsafe_allow_html=True)
    with col_b:
        st.markdown(f"""
        <div class="insight-box-blue">
            <h3>🔵 Highest Malnutrition (2022)</h3>
            <p><strong>{stats['highest_mn_country']}</strong> records the highest adult
            undernutrition at <strong>{stats['highest_mn_pct']:.1f}%</strong> —
            a stark reminder that food insecurity persists alongside rising obesity globally.</p>
        </div>""", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="insight-box">
        <h3>💡 The Paradox — {stats['dual_burden_count']} countries carry both burdens simultaneously</h3>
        <p>Rising obesity and persistent malnutrition are not opposing problems — they coexist in the
        same countries, often in the same communities. This dual burden is driven by the shift toward
        cheap, calorie-dense, nutrient-poor food systems, and demands integrated health policy responses.</p>
    </div>""", unsafe_allow_html=True)

    st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)

    ob = load_obesity()
    mn = load_malnutrition()

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📈 Global Trend — Obesity vs Malnutrition")
        if not ob.empty and not mn.empty:
            st.plotly_chart(plot_dual_trend(ob, mn), use_container_width=True)
    with col2:
        st.subheader("🍩 Obesity Level Distribution")
        if not ob.empty and "Obesity_Level" in ob.columns:
            st.plotly_chart(plot_level_donut(ob, "Obesity_Level", "Obesity"),
                            use_container_width=True)

    st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)
    st.subheader("⚖️ The Nutrition Paradox — Every Dot is a Country (2022)")
    if not ob.empty and not mn.empty:
        st.plotly_chart(plot_paradox_scatter(ob, mn, year=2022), use_container_width=True)
    st.markdown("""
    <div class="insight-box">
        <h3>📌 How to read this chart</h3>
        <p>Each dot is a country. The <strong>top-right quadrant</strong> represents the
        <em>dual burden</em> — countries above the median on BOTH obesity and malnutrition.
        Use the region legend to filter. Countries in this quadrant need integrated,
        not siloed, public health strategies.</p>
    </div>""", unsafe_allow_html=True)

    st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)
    col3, col4 = st.columns(2)
    with col3:
        st.subheader("🌐 Global Obesity Map (2022)")
        if not ob.empty:
            st.plotly_chart(plot_choropleth(ob, "Obesity", 2022), use_container_width=True)
    with col4:
        st.subheader("🌐 Global Malnutrition Map (2022)")
        if not mn.empty:
            st.plotly_chart(plot_choropleth(mn, "Malnutrition", 2022), use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════
# PAGE 2 — EDA
# ═══════════════════════════════════════════════════════════════════════════
elif page == "📊 EDA — Exploratory Analysis":

    st.markdown("""
    <div class="page-title">
        <h2>📊 Exploratory Data Analysis</h2>
        <p>Distribution checks, regional trends, gender gaps and data-quality diagnostics</p>
    </div>""", unsafe_allow_html=True)

    ob = load_obesity()
    mn = load_malnutrition()
    if ob.empty or mn.empty:
        st.error("⚠️ Data not loaded. Make sure nutrition.db exists and tables are populated.")
        st.stop()

    tab1, tab2, tab3, tab4 = st.tabs(
        ["🔴 Obesity EDA", "🔵 Malnutrition EDA", "🔗 Side-by-Side", "🔬 Data Quality"]
    )

    # ── Tab 1: Obesity ──────────────────────────────────────────────────
    with tab1:
        st.markdown("""
        <div class="insight-box-red">
            <h3>🔴 Obesity Dataset Overview</h3>
            <p>Adult obesity (BMI ≥ 30) and child/adolescent overweight (BMI +2SD) — 2012 to 2022.</p>
        </div>""", unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        c1.metric("Total Rows",      f"{len(ob):,}")
        c2.metric("Unique Countries", ob["Country"].nunique())
        c3.metric("Null Values",      int(ob.isnull().sum().sum()))

        st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)
        null_df = ob.isnull().sum().reset_index()
        null_df.columns = ["Column", "Null Count"]
        null_df = null_df[null_df["Null Count"] > 0]
        if null_df.empty:
            st.success("✅ No missing values in the obesity dataset.")
        else:
            st.dataframe(null_df, use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📈 Global Obesity Trend")
            trend = ob[ob["Gender"]=="Both"].groupby("Year")["Mean_Estimate"].mean().reset_index()
            fig = px.line(trend, x="Year", y="Mean_Estimate", markers=True,
                          color_discrete_sequence=["#ef4444"])
            fig.update_traces(line_width=3, marker_size=8)
            fig.update_layout(**_DARK, yaxis_title="Avg Obesity (%)", hovermode="x unified")
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            st.subheader("📦 Regional Spread")
            st.plotly_chart(plot_region_boxplot(ob, "Obesity"), use_container_width=True)

        col3, col4 = st.columns(2)
        with col3:
            st.subheader("⚧ Gender Gap by Region")
            st.plotly_chart(plot_gender_gap(ob, "Obesity"), use_container_width=True)
        with col4:
            st.subheader("👶 Adults vs Children")
            st.plotly_chart(plot_age_group_bar(ob, "Obesity"), use_container_width=True)

        st.subheader("🔥 CI Width Heatmap — Region × Age")
        st.plotly_chart(
        plot_ci_heatmap(ob, "Obesity"),
        use_container_width=True,
        key="obesity_heatmap_tab1"
        )

    # ── Tab 2: Malnutrition ─────────────────────────────────────────────
    with tab2:
        st.markdown("""
        <div class="insight-box-blue">
            <h3>🔵 Malnutrition Dataset Overview</h3>
            <p>Adult underweight (BMI < 18.5) and child thinness (BMI −2SD) — 2012 to 2022.</p>
        </div>""", unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        c1.metric("Total Rows",      f"{len(mn):,}")
        c2.metric("Unique Countries", mn["Country"].nunique())
        c3.metric("Null Values",      int(mn.isnull().sum().sum()))

        st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📈 Global Malnutrition Trend")
            trend_mn = mn[mn["Gender"]=="Both"].groupby("Year")["Mean_Estimate"].mean().reset_index()
            fig = px.line(trend_mn, x="Year", y="Mean_Estimate", markers=True,
                          color_discrete_sequence=["#3b82f6"])
            fig.update_traces(line_width=3, marker_size=8)
            fig.update_layout(**_DARK, yaxis_title="Avg Malnutrition (%)", hovermode="x unified")
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            st.subheader("📦 Regional Spread")
            st.plotly_chart(plot_region_boxplot(mn, "Malnutrition"), use_container_width=True)

        col3, col4 = st.columns(2)
        with col3:
            st.subheader("⚧ Gender Gap by Region")
            st.plotly_chart(plot_gender_gap(mn, "Malnutrition"), use_container_width=True)
        with col4:
            st.subheader("👶 Adults vs Children")
            st.plotly_chart(plot_age_group_bar(mn, "Malnutrition"), use_container_width=True)

        st.subheader("🔥 CI Width Heatmap — Region × Age")
        st.plotly_chart(
        plot_ci_heatmap(mn, "Malnutrition"),
        use_container_width=True,
        key="malnutrition_heatmap_tab2"
        )

    # ── Tab 3: Side-by-side ─────────────────────────────────────────────
    with tab3:
        st.subheader("🔗 Obesity vs Malnutrition by Region")
        st.plotly_chart(plot_grouped_bar(ob, mn, "Region"), use_container_width=True)
        st.subheader("⚧ Gender Disparity Across Both Conditions")
        st.plotly_chart(plot_grouped_bar(ob, mn, "Gender"), use_container_width=True)
        st.subheader("⚖️ Paradox Scatter — Select Year")
        yr = st.slider("Year", 2012, 2022, 2022, key="eda_yr")
        st.plotly_chart(plot_paradox_scatter(ob, mn, year=yr), use_container_width=True)

    # ── Tab 4: Data Quality ─────────────────────────────────────────────
    with tab4:
        st.markdown("""
        <div class="insight-box">
            <h3>📌 CI Width = UpperBound − LowerBound</h3>
            <p>A wider confidence interval means a less reliable estimate. Regions with
            high CI Width AND high disease burden are where intervention is most needed
            — and hardest to target accurately.</p>
        </div>""", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Obesity CI Width Heatmap**")
            st.plotly_chart(
        plot_ci_heatmap(ob, "Obesity"),
        use_container_width=True,
        key="obesity_heatmap_tab4"
        )
        with col2:
            st.markdown("**Malnutrition CI Width Heatmap**")
            st.plotly_chart(
        plot_ci_heatmap(mn, "Malnutrition"),
        use_container_width=True,
        key="malnutrition_heatmap_tab4"
        )

        st.subheader("📋 Descriptive Statistics")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Obesity**")
            st.dataframe(ob[["Mean_Estimate","LowerBound","UpperBound","CI_Width"]]
                         .describe().round(2), use_container_width=True)
        with col2:
            st.markdown("**Malnutrition**")
            st.dataframe(mn[["Mean_Estimate","LowerBound","UpperBound","CI_Width"]]
                         .describe().round(2), use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════
# PAGE 3 — OBESITY QUERIES
# ═══════════════════════════════════════════════════════════════════════════
elif page == "🔴 Obesity Queries":

    st.markdown("""
    <div class="page-title">
        <h2>🔴 Obesity Queries — Q1 to Q10</h2>
        <p>10 SQL queries on the obesity table — each with a chart and glowing insight box</p>
    </div>""", unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])
    with col1:
        selected_q = st.selectbox("Select Query", list(OBESITY_QUERIES.keys()),
                                  key="ob_sel")
    with col2:
        st.markdown("<br/>", unsafe_allow_html=True)
        run_all = st.checkbox("Run all 10", key="ob_all")

    st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)

    if run_all:
        for qn in OBESITY_QUERIES:
            st.markdown(f"### {qn}")
            render_query_section(qn)
            st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)
    else:
        st.markdown(f"### {selected_q}")
        render_query_section(selected_q)

    st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)
    st.markdown("""
    <div class="page-title">
        <h2>📊 Additional Obesity Charts</h2>
        <p>Pre-rendered from the full obesity dataset</p>
    </div>""", unsafe_allow_html=True)

    ob = load_obesity()
    if not ob.empty:
        col1, col2 = st.columns(2)
        with col1:
            yr = st.selectbox("Filter by year", [None] + list(range(2012, 2023)),
                              format_func=lambda x: "All years" if x is None else str(x),
                              key="ob_yr")
            st.plotly_chart(plot_top_countries(ob, 10, "Obesity", yr),
                            use_container_width=True)
        with col2:
            st.plotly_chart(plot_gender_gap(ob, "Obesity"), use_container_width=True)
        st.plotly_chart(plot_choropleth(ob, "Obesity", 2022), use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════
# PAGE 4 — MALNUTRITION QUERIES
# ═══════════════════════════════════════════════════════════════════════════
elif page == "🔵 Malnutrition Queries":

    st.markdown("""
    <div class="page-title">
        <h2>🔵 Malnutrition Queries — Q11 to Q20</h2>
        <p>10 SQL queries on the malnutrition table — each with a chart and glowing insight box</p>
    </div>""", unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])
    with col1:
        selected_q = st.selectbox("Select Query", list(MALN_QUERIES.keys()),
                                  key="mn_sel")
    with col2:
        st.markdown("<br/>", unsafe_allow_html=True)
        run_all_mn = st.checkbox("Run all 10", key="mn_all")

    st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)

    if run_all_mn:
        for qn in MALN_QUERIES:
            st.markdown(f"### {qn}")
            render_query_section(qn)
            st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)
    else:
        st.markdown(f"### {selected_q}")
        render_query_section(selected_q)

    st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)
    st.markdown("""
    <div class="page-title">
        <h2>📊 Additional Malnutrition Charts</h2>
        <p>Pre-rendered from the full malnutrition dataset</p>
    </div>""", unsafe_allow_html=True)

    mn = load_malnutrition()
    if not mn.empty:
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(plot_top_countries(mn, 10, "Malnutrition"),
                            use_container_width=True)
        with col2:
            st.plotly_chart(plot_gender_gap(mn, "Malnutrition"), use_container_width=True)

        mn19, _ = run_query(QUERIES["Q19 · Min / Max malnutrition year-wise"])
        if mn19 is not None:
            st.plotly_chart(plot_min_max_band(mn19, "Malnutrition"), use_container_width=True)
        st.plotly_chart(plot_choropleth(mn, "Malnutrition", 2022), use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════
# PAGE 5 — COMBINED QUERIES
# ═══════════════════════════════════════════════════════════════════════════
elif page == "🔗 Combined Queries":

    st.markdown("""
    <div class="page-title">
        <h2>🔗 Combined Queries — Q21 to Q25</h2>
        <p>5 JOIN queries that reveal the nutrition paradox across countries, regions and demographics</p>
    </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class="insight-box">
        <h3>💡 Why these queries matter</h3>
        <p>These five queries JOIN the obesity and malnutrition tables — uncovering countries that
        face both burdens simultaneously, how gender shapes both conditions, and which nations are
        in active nutritional transition from undernutrition to overnutrition.</p>
    </div>""", unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])
    with col1:
        selected_q = st.selectbox("Select Query", list(COMBINED_QUERIES.keys()),
                                  key="comb_sel")
    with col2:
        st.markdown("<br/>", unsafe_allow_html=True)
        run_all_c = st.checkbox("Run all 5", key="comb_all")

    st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)

    if run_all_c:
        for qn in COMBINED_QUERIES:
            st.markdown(f"### {qn}")
            render_query_section(qn)
            st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)
    else:
        st.markdown(f"### {selected_q}")
        render_query_section(selected_q)

    # ── Q24 spotlight ─────────────────────────────────────────────────
    st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)
    st.markdown("""
    <div class="page-title">
        <h2>🔁 Nutritional Transition Countries</h2>
        <p>Q24 — Obesity rising AND malnutrition falling simultaneously</p>
    </div>""", unsafe_allow_html=True)

    df24, _ = run_query(QUERIES["Q24 · Rising obesity + falling malnutrition (transition countries)"])
    if df24 is not None and len(df24):
        fig24 = go.Figure(data=[
            go.Bar(name="↑ Obesity Rise",      x=df24["Country"], y=df24["ob_change"],
                   marker_color="#ef4444",
                   text=df24["ob_change"].round(1),
                   texttemplate="+%{text}%", textposition="outside"),
            go.Bar(name="↓ Malnutrition Drop", x=df24["Country"], y=df24["mn_drop"],
                   marker_color="#10b981",
                   text=df24["mn_drop"].round(1),
                   texttemplate="-%{text}%", textposition="outside"),
        ])
        fig24.update_layout(**_DARK,
                            barmode="group",
                            title="Countries in Nutritional Transition (2012–2022)",
                            xaxis_tickangle=-35, yaxis_title="Change in %",
                            legend=dict(orientation="h", yanchor="bottom", y=1.02))
        st.plotly_chart(fig24, use_container_width=True)

    st.markdown("""
    <div class="insight-box-green">
        <h3>🔗 The Transition Story</h3>
        <p>Transition countries are winning the malnutrition battle but losing the obesity one.
        Economic development solves chronic food scarcity but introduces new diet-quality problems
        as cheaper, calorie-dense processed foods replace traditional diets. Brazil's trajectory —
        the largest malnutrition drop alongside a moderate obesity rise — reflects its sustained
        social protection programmes (Bolsa Família).</p>
    </div>""", unsafe_allow_html=True)

    ob = load_obesity()
    mn = load_malnutrition()
    if not ob.empty and not mn.empty:
        st.subheader("📊 Obesity vs Malnutrition by Region")
        st.plotly_chart(plot_grouped_bar(ob, mn, "Region"), use_container_width=True)
        st.subheader("⚧ Gender Disparity — Both Conditions")
        st.plotly_chart(plot_grouped_bar(ob, mn, "Gender"), use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════
# PAGE 6 — COUNTRY DEEP-DIVE
# ═══════════════════════════════════════════════════════════════════════════
elif page == "🌍 Country Deep-Dive":

    st.markdown("""
    <div class="page-title">
        <h2>🌍 Country Deep-Dive</h2>
        <p>Full obesity & malnutrition profile for any country across all years, genders and age groups</p>
    </div>""", unsafe_allow_html=True)

    ob = load_obesity()
    mn = load_malnutrition()

    all_countries = sorted(
        set(ob["Country"].dropna().unique()) | set(mn["Country"].dropna().unique())
    )

    col_sel, col_age = st.columns([3, 1])
    with col_sel:
        country = st.selectbox(
            "Choose a country", all_countries,
            index=all_countries.index("India") if "India" in all_countries else 0,
        )
    with col_age:
        age_filter = st.selectbox("Age group",
                                  ["All", "Adult", "Child/Adolescent"],
                                  key="dd_age")

    ob_c = ob[ob["Country"] == country].copy()
    mn_c = mn[mn["Country"] == country].copy()
    if age_filter != "All":
        ob_c = ob_c[ob_c["Age_Group"] == age_filter]
        mn_c = mn_c[mn_c["Age_Group"] == age_filter]

    st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)

    ob22 = ob_c[(ob_c["Year"]==2022)&(ob_c["Gender"]=="Both")]["Mean_Estimate"].mean()
    mn22 = mn_c[(mn_c["Year"]==2022)&(mn_c["Gender"]=="Both")]["Mean_Estimate"].mean()
    ob12 = ob_c[(ob_c["Year"]==2012)&(ob_c["Gender"]=="Both")]["Mean_Estimate"].mean()
    mn12 = mn_c[(mn_c["Year"]==2012)&(mn_c["Gender"]=="Both")]["Mean_Estimate"].mean()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🔴 Obesity 2022",      f"{ob22:.1f}%" if not pd.isna(ob22) else "N/A",
              delta=f"{ob22-ob12:+.1f}% since 2012" if not (pd.isna(ob22) or pd.isna(ob12)) else None)
    c2.metric("🔵 Malnutrition 2022", f"{mn22:.1f}%" if not pd.isna(mn22) else "N/A",
              delta=f"{mn22-mn12:+.1f}% since 2012" if not (pd.isna(mn22) or pd.isna(mn12)) else None)
    c3.metric("🌐 Region",  ob_c["Region"].iloc[0] if not ob_c.empty and not ob_c["Region"].isna().all() else "—")
    c4.metric("📅 Data Points", f"{len(ob_c)+len(mn_c):,}")

    # Dynamic insight box based on actual country numbers
    if not (pd.isna(ob22) or pd.isna(mn22)):
        if ob22 > 15 and mn22 > 10:
            st.markdown(f"""
            <div class="insight-box">
                <h3>⚠️ Dual Burden — {country}</h3>
                <p><strong>{country}</strong> shows elevated obesity (<strong>{ob22:.1f}%</strong>)
                alongside significant malnutrition (<strong>{mn22:.1f}%</strong>) — a dual-burden
                nation requiring integrated, not siloed, public health policy.</p>
            </div>""", unsafe_allow_html=True)
        elif ob22 > 25:
            st.markdown(f"""
            <div class="insight-box-red">
                <h3>🔴 High Obesity Alert — {country}</h3>
                <p>Obesity at <strong>{ob22:.1f}%</strong> in 2022 is well above the global average.
                Priority: dietary education, urban food environment reform, physical activity promotion.</p>
            </div>""", unsafe_allow_html=True)
        elif mn22 > 20:
            st.markdown(f"""
            <div class="insight-box-blue">
                <h3>🔵 High Malnutrition Alert — {country}</h3>
                <p>Malnutrition at <strong>{mn22:.1f}%</strong> signals persistent food insecurity.
                Priority: social protection programmes, school feeding, agricultural investment.</p>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="insight-box-green">
                <h3>✅ Relatively Balanced — {country}</h3>
                <p>Obesity at <strong>{ob22:.1f}%</strong> and malnutrition at
                <strong>{mn22:.1f}%</strong> are both below major alert thresholds in 2022.
                Continued monitoring recommended.</p>
            </div>""", unsafe_allow_html=True)

    st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader(f"🔴 Obesity Trend — {country}")
        ob_t = (ob_c[ob_c["Gender"]=="Both"]
                .groupby("Year")["Mean_Estimate"].mean().reset_index())
        if not ob_t.empty:
            fig = px.line(ob_t, x="Year", y="Mean_Estimate", markers=True,
                          color_discrete_sequence=["#ef4444"])
            fig.update_traces(line_width=3, marker_size=9)
            fig.update_layout(**_DARK, yaxis_title="Obesity (%)", hovermode="x unified")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No obesity data for this selection.")

    with col2:
        st.subheader(f"🔵 Malnutrition Trend — {country}")
        mn_t = (mn_c[mn_c["Gender"]=="Both"]
                .groupby("Year")["Mean_Estimate"].mean().reset_index())
        if not mn_t.empty:
            fig2 = px.line(mn_t, x="Year", y="Mean_Estimate", markers=True,
                           color_discrete_sequence=["#3b82f6"])
            fig2.update_traces(line_width=3, marker_size=9)
            fig2.update_layout(**_DARK, yaxis_title="Malnutrition (%)", hovermode="x unified")
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No malnutrition data for this selection.")

    st.subheader(f"⚧ Gender Breakdown — {country}")
    col3, col4 = st.columns(2)
    with col3:
        ob_g = (ob_c[ob_c["Gender"].isin(["Male","Female"])]
                .groupby(["Year","Gender"])["Mean_Estimate"].mean().reset_index())
        if not ob_g.empty:
            fig3 = px.line(ob_g, x="Year", y="Mean_Estimate", color="Gender",
                           markers=True,
                           color_discrete_map={"Male":"#3b82f6","Female":"#f472b6"})
            fig3.update_layout(**_DARK, title="Obesity by Gender", hovermode="x unified")
            st.plotly_chart(fig3, use_container_width=True)
    with col4:
        mn_g = (mn_c[mn_c["Gender"].isin(["Male","Female"])]
                .groupby(["Year","Gender"])["Mean_Estimate"].mean().reset_index())
        if not mn_g.empty:
            fig4 = px.line(mn_g, x="Year", y="Mean_Estimate", color="Gender",
                           markers=True,
                           color_discrete_map={"Male":"#3b82f6","Female":"#f472b6"})
            fig4.update_layout(**_DARK, title="Malnutrition by Gender", hovermode="x unified")
            st.plotly_chart(fig4, use_container_width=True)

    st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)
    st.subheader(f"📋 Raw Data — {country}")
    tab_ob, tab_mn = st.tabs(["Obesity Records", "Malnutrition Records"])
    with tab_ob:
        if not ob_c.empty:
            st.dataframe(ob_c.sort_values(["Year","Gender"]),
                         use_container_width=True, height=350)
            st.download_button("📥 Download", ob_c.to_csv(index=False),
                               file_name=f"{country}_obesity.csv")
        else:
            st.info("No obesity records for this filter.")
    with tab_mn:
        if not mn_c.empty:
            st.dataframe(mn_c.sort_values(["Year","Gender"]),
                         use_container_width=True, height=350)
            st.download_button("📥 Download", mn_c.to_csv(index=False),
                               file_name=f"{country}_malnutrition.csv")
        else:
            st.info("No malnutrition records for this filter.")

# ═══════════════════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════════════════
st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align:center; color:#64748b; font-size:0.8rem; padding:8px 0 16px;'>
    <strong style='color:#667eea'>⚖️ Nutrition Paradox</strong> &nbsp;|&nbsp;
    Data: WHO Global Health Observatory API &nbsp;|&nbsp;
    Period: 2012–2022 &nbsp;|&nbsp;
    Built with Streamlit · Plotly · SQLite · Python
</div>""", unsafe_allow_html=True)
