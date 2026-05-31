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

Folder structure expected:
    NUTRITION_PARADOX/
    ├── app/
    │   ├── sql/queries.py
    │   ├── db_utils.py
    │   ├── viz_utils.py
    │   └── streamlit_app.py   ← this file
    ├── data/processed/
    ├── notebooks/
    └── nutrition.db
"""

import os, sys, re
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ── Make app/ importable regardless of launch directory ──────────────────
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sql.queries import QUERIES, QUERY_INSIGHTS
from db_utils    import run_query, load_obesity, load_malnutrition, get_dashboard_stats
from viz_utils   import (
    plot_dual_trend, plot_top_countries, plot_gender_gap,
    plot_region_boxplot, plot_paradox_scatter, plot_ci_heatmap,
    plot_country_comparison, plot_age_group_bar, plot_grouped_bar,
    plot_level_donut, plot_choropleth, plot_min_max_band, auto_chart,
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
# GLOBAL CSS  —  same glowing-box style as NASA NEO project
# ═══════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
/* ── Typography & base ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* ── Main header ── */
.main-header {
    font-size: 2.8rem;
    font-weight: 700;
    text-align: center;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    padding: 10px 0 4px;
    line-height: 1.2;
}
.sub-header {
    text-align: center;
    color: #94a3b8;
    font-size: 1rem;
    margin-bottom: 6px;
}

/* ── Glowing insight box (same gradient as NASA project) ── */
.insight-box {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 18px 22px;
    border-radius: 12px;
    color: white;
    margin: 14px 0;
    box-shadow: 0 0 18px rgba(102,126,234,0.45);
}
.insight-box h3 {
    margin: 0 0 8px;
    font-size: 1rem;
    font-weight: 600;
    letter-spacing: .02em;
}
.insight-box p { margin: 0; font-size: 0.88rem; line-height: 1.6; opacity: 0.95; }

/* ── Obesity insight (red glow) ── */
.insight-box-red {
    background: linear-gradient(135deg, #ef4444 0%, #b91c1c 100%);
    padding: 18px 22px;
    border-radius: 12px;
    color: white;
    margin: 14px 0;
    box-shadow: 0 0 18px rgba(239,68,68,0.40);
}
.insight-box-red h3 { margin: 0 0 8px; font-size: 1rem; font-weight: 600; }
.insight-box-red p  { margin: 0; font-size: 0.88rem; line-height: 1.6; opacity: 0.95; }

/* ── Malnutrition insight (blue glow) ── */
.insight-box-blue {
    background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
    padding: 18px 22px;
    border-radius: 12px;
    color: white;
    margin: 14px 0;
    box-shadow: 0 0 18px rgba(59,130,246,0.40);
}
.insight-box-blue h3 { margin: 0 0 8px; font-size: 1rem; font-weight: 600; }
.insight-box-blue p  { margin: 0; font-size: 0.88rem; line-height: 1.6; opacity: 0.95; }

/* ── Combined insight (green glow) ── */
.insight-box-green {
    background: linear-gradient(135deg, #10b981 0%, #065f46 100%);
    padding: 18px 22px;
    border-radius: 12px;
    color: white;
    margin: 14px 0;
    box-shadow: 0 0 18px rgba(16,185,129,0.40);
}
.insight-box-green h3 { margin: 0 0 8px; font-size: 1rem; font-weight: 600; }
.insight-box-green p  { margin: 0; font-size: 0.88rem; line-height: 1.6; opacity: 0.95; }

/* ── Metric cards ── */
.metric-card {
    background: rgba(30,27,75,0.6);
    border: 1px solid rgba(102,126,234,0.3);
    border-left: 4px solid #667eea;
    padding: 16px 18px;
    border-radius: 10px;
    margin: 6px 0;
    box-shadow: 0 0 12px rgba(102,126,234,0.15);
}
.metric-card h4 { margin: 0 0 4px; color: #94a3b8; font-size: 0.78rem; text-transform: uppercase; letter-spacing: .06em; }
.metric-card p  { margin: 0; font-size: 1.6rem; font-weight: 700; color: #e2e8f0; }

/* ── Section divider ── */
.section-divider {
    border: none;
    border-top: 1px solid rgba(102,126,234,0.25);
    margin: 20px 0;
}

/* ── Page title strip ── */
.page-title {
    background: linear-gradient(90deg, rgba(102,126,234,0.15) 0%, transparent 100%);
    border-left: 4px solid #667eea;
    padding: 10px 16px;
    border-radius: 0 8px 8px 0;
    margin-bottom: 20px;
}
.page-title h2 { margin: 0; font-size: 1.4rem; color: #e2e8f0; }
.page-title p  { margin: 2px 0 0; font-size: 0.82rem; color: #94a3b8; }

/* ── SQL code block ── */
.stCode { border-radius: 8px !important; }

/* ── Dataframe styling ── */
.dataframe-container { border-radius: 8px; overflow: hidden; }

/* ── Tab active style override ── */
button[data-baseweb="tab"][aria-selected="true"] {
    color: #667eea !important;
    border-bottom: 2px solid #667eea !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f0c29 0%, #1a1a3e 50%, #0f0c29 100%);
}
[data-testid="stSidebar"] .stMarkdown { color: #94a3b8; }
[data-testid="stSidebar"] hr { border-color: rgba(102,126,234,0.25); }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
# COLOR CONSTANTS  (shared with charts)
# ═══════════════════════════════════════════════════════════════════════════
COLORS = {
    "primary": "#667eea",
    "danger":  "#ef4444",
    "safe":    "#10b981",
    "warning": "#f59e0b",
    "info":    "#3b82f6",
    "purple":  "#764ba2",
}

# ═══════════════════════════════════════════════════════════════════════════
# HELPER: render insight box by query category
# ═══════════════════════════════════════════════════════════════════════════
def _q_num(k: str) -> int:
    m = re.match(r"Q(\d+)", k)
    return int(m.group(1)) if m else 0


def insight_box(query_name: str, emoji: str = "💡") -> None:
    """Render the glowing insight callout for the given query."""
    text = QUERY_INSIGHTS.get(query_name, "")
    if not text:
        return
    n = _q_num(query_name)
    if 1 <= n <= 10:
        box_cls = "insight-box-red"
        label   = "🔴 Obesity Insight"
    elif 11 <= n <= 20:
        box_cls = "insight-box-blue"
        label   = "🔵 Malnutrition Insight"
    elif 21 <= n <= 25:
        box_cls = "insight-box-green"
        label   = "🔗 Combined Insight"
    else:
        box_cls = "insight-box"
        label   = f"{emoji} Key Insight"
    st.markdown(f"""
    <div class="{box_cls}">
        <h3>{label}</h3>
        <p>{text}</p>
    </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# HELPER: render a single query section (used on all 3 query pages)
# ═══════════════════════════════════════════════════════════════════════════
def render_query_section(query_name: str, box_color: str = "red") -> None:
    """
    Renders: SQL expander → Run button → results table →
             download CSV → insight box → auto chart.
    """
    sql = QUERIES[query_name]

    with st.expander("📝 View SQL", expanded=False):
        st.code(sql, language="sql")

    col_btn, col_dl = st.columns([1, 5])
    run = col_btn.button("▶️ Run Query", key=f"run_{query_name}", type="primary")

    if run:
        with st.spinner("Querying database…"):
            df, err = run_query(sql)
        if err:
            st.error(f"❌ {err}")
            return
        st.success(f"✅ {len(df):,} rows returned")
        st.dataframe(df, use_container_width=True, height=min(350, 55 + 35 * len(df)))
        # Download
        st.download_button(
            "📥 Download CSV",
            df.to_csv(index=False),
            file_name=f"{query_name[:30]}.csv",
            mime="text/csv",
        )
        # Insight box
        insight_box(query_name)
        # Auto chart
        fig = auto_chart(df, query_name)
        if fig:
            st.plotly_chart(fig, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════
# SIDEBAR NAVIGATION
# ═══════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 10px 0 6px;'>
        <span style='font-size:2.4rem'>⚖️</span>
        <div style='font-size:1.05rem; font-weight:700; color:#667eea; margin-top:4px;'>
            Nutrition Paradox
        </div>
        <div style='font-size:0.75rem; color:#64748b; margin-top:2px;'>
            WHO Global Health Analytics
        </div>
    </div>
    """, unsafe_allow_html=True)
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
    <div style='font-size:0.75rem; color:#64748b; padding: 4px 0;'>
        <b style='color:#94a3b8'>Data source:</b> WHO GHO API<br>
        <b style='color:#94a3b8'>Period:</b> 2012 – 2022<br>
        <b style='color:#94a3b8'>Indicators:</b> BMI-based<br>
        <b style='color:#94a3b8'>Engine:</b> SQLite + Streamlit
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# PAGE 1 — OVERVIEW
# ═══════════════════════════════════════════════════════════════════════════
if page == "🏠 Overview":

    st.markdown('<h1 class="main-header">⚖️ Nutrition Paradox</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">A Global View on Obesity & Malnutrition — WHO Data 2012–2022</p>', unsafe_allow_html=True)
    st.markdown("---")

    # ── KPI metric row ────────────────────────────────────────────────────
    stats = get_dashboard_stats()
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("📋 Obesity Records",      f"{stats['obesity_records']:,}")
    c2.metric("📋 Malnutrition Records", f"{stats['malnutrition_records']:,}")
    c3.metric("🌐 Countries Tracked",    f"{stats['countries']:,}")
    c4.metric("⚠️ Dual Burden Nations",  f"{stats['dual_burden_count']:,}",
              help="Countries where both obesity AND malnutrition average > 10 %")
    c5.metric("📅 Years Covered",        stats["years_covered"])

    st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)

    # ── Featured insight boxes ────────────────────────────────────────────
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
        <p>Rising obesity and persistent malnutrition are not opposing problems — they coexist in the same
        countries, often in the same communities. This dual burden is driven by the shift toward cheap,
        calorie-dense, nutrient-poor food systems, and demands integrated, not siloed, health policy responses.</p>
    </div>""", unsafe_allow_html=True)

    st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)

    # ── Charts row 1 ─────────────────────────────────────────────────────
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

    # ── The paradox scatter ───────────────────────────────────────────────
    st.subheader("⚖️ The Nutrition Paradox — Every Dot is a Country (2022)")
    if not ob.empty and not mn.empty:
        st.plotly_chart(plot_paradox_scatter(ob, mn, year=2022),
                        use_container_width=True)
    st.markdown("""
    <div class="insight-box">
        <h3>📌 How to read this chart</h3>
        <p>Each dot is a country. The <strong>top-right quadrant</strong> (above both median lines)
        represents the <em>dual burden</em> — countries where obesity AND malnutrition both
        exceed their global medians. The <strong>bottom-left</strong> shows countries with
        low burdens on both dimensions. Use the legend to filter by WHO region.</p>
    </div>""", unsafe_allow_html=True)

    st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)

    # ── Charts row 2 ─────────────────────────────────────────────────────
    col3, col4 = st.columns(2)
    with col3:
        st.subheader("🌐 Global Obesity Map (2022)")
        if not ob.empty:
            st.plotly_chart(plot_choropleth(ob, "Obesity", 2022),
                            use_container_width=True)
    with col4:
        st.subheader("🌐 Global Malnutrition Map (2022)")
        if not mn.empty:
            st.plotly_chart(plot_choropleth(mn, "Malnutrition", 2022),
                            use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════
# PAGE 2 — EDA
# ═══════════════════════════════════════════════════════════════════════════
elif page == "📊 EDA — Exploratory Analysis":

    st.markdown("""
    <div class="page-title">
        <h2>📊 Exploratory Data Analysis</h2>
        <p>Distribution checks, trend visualisations and demographic deep-dives</p>
    </div>""", unsafe_allow_html=True)

    ob = load_obesity()
    mn = load_malnutrition()

    if ob.empty or mn.empty:
        st.error("⚠️ Data not loaded. Make sure nutrition.db exists and tables are populated.")
        st.stop()

    tab1, tab2, tab3, tab4 = st.tabs(
        ["🔴 Obesity EDA", "🔵 Malnutrition EDA", "🔗 Side-by-Side", "🔬 Data Quality"]
    )

    # ── Tab 1: Obesity EDA ─────────────────────────────────────────────
    with tab1:
        st.markdown("""
        <div class="insight-box-red">
            <h3>🔴 Obesity Dataset Overview</h3>
            <p>Exploring distribution, regional spread, gender gaps and age-group differences
            across <strong>adult and child/adolescent</strong> obesity data from 2012 to 2022.</p>
        </div>""", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        col1.metric("Total Rows",     f"{len(ob):,}")
        col2.metric("Unique Countries", ob["Country"].nunique())

        st.markdown("##### Columns & Data Types")
        dtype_df = pd.DataFrame({"Column": ob.dtypes.index, "Type": ob.dtypes.values.astype(str)})
        st.dataframe(dtype_df, use_container_width=True, height=300)

        st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)

        # Missing values
        st.markdown("##### Missing Values")
        null_df = ob.isnull().sum().reset_index()
        null_df.columns = ["Column", "Null Count"]
        null_df = null_df[null_df["Null Count"] > 0]
        if null_df.empty:
            st.success("✅ No missing values in the obesity dataset.")
        else:
            st.dataframe(null_df, use_container_width=True)

        st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📈 Global Obesity Trend")
            trend = (ob[ob["Gender"] == "Both"]
                     .groupby("Year")["Mean_Estimate"].mean().reset_index())
            fig = px.line(trend, x="Year", y="Mean_Estimate", markers=True,
                          color_discrete_sequence=["#ef4444"])
            fig.update_traces(line_width=3, marker_size=8)
            fig.update_layout(template="plotly_dark",
                               paper_bgcolor="rgba(0,0,0,0)",
                               plot_bgcolor="rgba(0,0,0,0)",
                               yaxis_title="Avg Obesity (%)",
                               hovermode="x unified")
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("📦 Regional Spread (Box Plot)")
            st.plotly_chart(plot_region_boxplot(ob, "Obesity"), use_container_width=True)

        col3, col4 = st.columns(2)
        with col3:
            st.subheader("⚧ Gender Gap by Region")
            st.plotly_chart(plot_gender_gap(ob, "Obesity"), use_container_width=True)
        with col4:
            st.subheader("👶 Adults vs Children")
            st.plotly_chart(plot_age_group_bar(ob, "Obesity"), use_container_width=True)

        st.subheader("🔥 Obesity Level Heatmap — Region × Age Group")
        st.plotly_chart(plot_ci_heatmap(ob, "Obesity"), use_container_width=True)

    # ── Tab 2: Malnutrition EDA ────────────────────────────────────────
    with tab2:
        st.markdown("""
        <div class="insight-box-blue">
            <h3>🔵 Malnutrition Dataset Overview</h3>
            <p>Exploring distribution, regional burden and demographic vulnerability patterns
            across <strong>adult underweight and child thinness</strong> data from 2012 to 2022.</p>
        </div>""", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        col1.metric("Total Rows",     f"{len(mn):,}")
        col2.metric("Unique Countries", mn["Country"].nunique())

        st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📈 Global Malnutrition Trend")
            trend_mn = (mn[mn["Gender"] == "Both"]
                        .groupby("Year")["Mean_Estimate"].mean().reset_index())
            fig = px.line(trend_mn, x="Year", y="Mean_Estimate", markers=True,
                          color_discrete_sequence=["#3b82f6"])
            fig.update_traces(line_width=3, marker_size=8)
            fig.update_layout(template="plotly_dark",
                               paper_bgcolor="rgba(0,0,0,0)",
                               plot_bgcolor="rgba(0,0,0,0)",
                               yaxis_title="Avg Malnutrition (%)",
                               hovermode="x unified")
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("📦 Regional Spread (Box Plot)")
            st.plotly_chart(plot_region_boxplot(mn, "Malnutrition"), use_container_width=True)

        col3, col4 = st.columns(2)
        with col3:
            st.subheader("⚧ Gender Gap by Region")
            st.plotly_chart(plot_gender_gap(mn, "Malnutrition"), use_container_width=True)
        with col4:
            st.subheader("👶 Adults vs Children")
            st.plotly_chart(plot_age_group_bar(mn, "Malnutrition"), use_container_width=True)

        st.subheader("🔥 Malnutrition CI Width — Region × Age")
        st.plotly_chart(plot_ci_heatmap(mn, "Malnutrition"), use_container_width=True)

    # ── Tab 3: Side-by-side ────────────────────────────────────────────
    with tab3:
        st.subheader("🔗 Obesity vs Malnutrition — Side-by-Side")
        st.plotly_chart(plot_grouped_bar(ob, mn, "Region"), use_container_width=True)
        st.plotly_chart(plot_grouped_bar(ob, mn, "Gender"), use_container_width=True)
        st.subheader("⚖️ The Paradox Scatter")
        year_sel = st.slider("Select Year", 2012, 2022, 2022, key="eda_scatter_year")
        st.plotly_chart(plot_paradox_scatter(ob, mn, year=year_sel), use_container_width=True)

    # ── Tab 4: Data Quality ────────────────────────────────────────────
    with tab4:
        st.subheader("🔬 Data Reliability (CI Width Analysis)")
        st.markdown("""
        <div class="insight-box">
            <h3>📌 What is CI Width?</h3>
            <p><strong>CI Width = UpperBound − LowerBound</strong>.
            A wider confidence interval means the estimate is less reliable.
            Regions with high CI Width AND high disease burden are where
            data-driven interventions are most urgently needed — and hardest to target.</p>
        </div>""", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Obesity CI Width Heatmap**")
            st.plotly_chart(plot_ci_heatmap(ob, "Obesity"), use_container_width=True)
        with col2:
            st.markdown("**Malnutrition CI Width Heatmap**")
            st.plotly_chart(plot_ci_heatmap(mn, "Malnutrition"), use_container_width=True)

        st.subheader("📋 Descriptive Statistics")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Obesity**")
            st.dataframe(ob[["Mean_Estimate", "LowerBound", "UpperBound", "CI_Width"]]
                         .describe().round(2), use_container_width=True)
        with col2:
            st.markdown("**Malnutrition**")
            st.dataframe(mn[["Mean_Estimate", "LowerBound", "UpperBound", "CI_Width"]]
                         .describe().round(2), use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════
# PAGE 3 — OBESITY QUERIES
# ═══════════════════════════════════════════════════════════════════════════
elif page == "🔴 Obesity Queries":

    st.markdown("""
    <div class="page-title">
        <h2>🔴 Obesity Queries — Q1 to Q10</h2>
        <p>All 10 SQL queries on the obesity table with auto-visualization and per-query insights</p>
    </div>""", unsafe_allow_html=True)

    # ── Query selector ─────────────────────────────────────────────────
    OBESITY_QUERIES = {k: v for k, v in QUERIES.items()
                       if k.startswith("Q") and 1 <= _q_num(k) <= 10}

    col1, col2 = st.columns([3, 1])
    with col1:
        selected_q = st.selectbox("Select Query", list(OBESITY_QUERIES.keys()),
                                  key="ob_query_select")
    with col2:
        st.markdown("<br/>", unsafe_allow_html=True)
        run_all = st.checkbox("Show all 10 queries", key="ob_run_all")

    st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)

    if run_all:
        for q_name in OBESITY_QUERIES:
            st.markdown(f"### {q_name}")
            render_query_section(q_name)
            st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)
    else:
        st.markdown(f"### {selected_q}")
        render_query_section(selected_q)

    # ── Extra EDA charts relevant to obesity ──────────────────────────
    st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)
    st.markdown("""
    <div class="page-title">
        <h2>📊 Additional Obesity Visualisations</h2>
        <p>Pre-rendered charts from the full obesity dataset</p>
    </div>""", unsafe_allow_html=True)

    ob = load_obesity()
    if not ob.empty:
        col1, col2 = st.columns(2)
        with col1:
            year_f = st.selectbox("Filter year", [None] + list(range(2012, 2023)),
                                  format_func=lambda x: "All years" if x is None else str(x),
                                  key="ob_top_year")
            st.plotly_chart(plot_top_countries(ob, n=10, condition="Obesity", year=year_f),
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
        <p>All 10 SQL queries on the malnutrition table with auto-visualization and per-query insights</p>
    </div>""", unsafe_allow_html=True)

    MALN_QUERIES = {k: v for k, v in QUERIES.items()
                    if k.startswith("Q") and 11 <= _q_num(k) <= 20}

    col1, col2 = st.columns([3, 1])
    with col1:
        selected_q = st.selectbox("Select Query", list(MALN_QUERIES.keys()),
                                  key="mn_query_select")
    with col2:
        st.markdown("<br/>", unsafe_allow_html=True)
        run_all_mn = st.checkbox("Show all 10 queries", key="mn_run_all")

    st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)

    if run_all_mn:
        for q_name in MALN_QUERIES:
            st.markdown(f"### {q_name}")
            render_query_section(q_name)
            st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)
    else:
        st.markdown(f"### {selected_q}")
        render_query_section(selected_q)

    st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)
    st.markdown("""
    <div class="page-title">
        <h2>📊 Additional Malnutrition Visualisations</h2>
        <p>Pre-rendered charts from the full malnutrition dataset</p>
    </div>""", unsafe_allow_html=True)

    mn = load_malnutrition()
    if not mn.empty:
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(plot_top_countries(mn, n=10, condition="Malnutrition"),
                            use_container_width=True)
        with col2:
            st.plotly_chart(plot_gender_gap(mn, "Malnutrition"), use_container_width=True)

        # Q19-style min/max band
        mn19, err = run_query(QUERIES["Q19 · Min / Max malnutrition year-wise"])
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
        <p>Cross-table JOIN queries that reveal the nutrition paradox at country and regional level</p>
    </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class="insight-box">
        <h3>💡 Why Combined Queries Matter</h3>
        <p>These five queries JOIN the obesity and malnutrition tables — revealing countries that
        face both burdens simultaneously, how gender shapes both conditions, and how the world is
        transitioning from undernutrition to overnutrition. These are the queries that turn
        data into policy-relevant insight.</p>
    </div>""", unsafe_allow_html=True)

    COMBINED_QUERIES = {k: v for k, v in QUERIES.items()
                        if k.startswith("Q") and 21 <= _q_num(k) <= 25}

    selected_q = st.selectbox("Select Query", list(COMBINED_QUERIES.keys()),
                               key="comb_query_select")
    run_all_c  = st.checkbox("Show all 5 combined queries", key="comb_run_all")

    st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)

    if run_all_c:
        for q_name in COMBINED_QUERIES:
            st.markdown(f"### {q_name}")
            render_query_section(q_name)
            st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)
    else:
        st.markdown(f"### {selected_q}")
        render_query_section(selected_q)

    # ── Q24 — Transition countries highlight ─────────────────────────
    st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)
    st.markdown("""
    <div class="page-title">
        <h2>🔁 Nutritional Transition — Obesity Rising, Malnutrition Falling</h2>
        <p>Based on Q24 — these countries are undergoing the fastest nutrition transition</p>
    </div>""", unsafe_allow_html=True)

    df24, _ = run_query(QUERIES["Q24 · Countries where obesity rises & malnutrition falls"])
    if df24 is not None and len(df24):
        fig = go.Figure(data=[
            go.Bar(name="↑ Obesity Rise",       x=df24["Country"], y=df24["ob_change"],
                   marker_color="#ef4444", text=df24["ob_change"].round(1),
                   texttemplate="+%{text}%", textposition="outside"),
            go.Bar(name="↓ Malnutrition Drop",  x=df24["Country"], y=df24["mn_drop"],
                   marker_color="#10b981", text=df24["mn_drop"].round(1),
                   texttemplate="-%{text}%", textposition="outside"),
        ])
        fig.update_layout(
            barmode="group", template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            title="Countries in Nutritional Transition (2012–2022)",
            xaxis_tickangle=-35, yaxis_title="Change in %",
            legend=dict(orientation="h", yanchor="bottom", y=1.02),
            margin=dict(t=60, b=10),
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("""
        <div class="insight-box-green">
            <h3>🔗 Combined Insight — The Transition Story</h3>
            <p>Countries in this chart are following a well-documented epidemiological trajectory:
            as incomes rise, populations shift from chronic food scarcity to calorie excess.
            Brazil's trajectory — largest malnutrition drop alongside a moderate obesity rise —
            reflects its social protection programs (Bolsa Família). Countries with large obesity
            rises and small malnutrition drops may be skipping the dietary quality improvement
            that should accompany development.</p>
        </div>""", unsafe_allow_html=True)

    # ── Grouped bar: both conditions side-by-side by region ──────────
    ob = load_obesity()
    mn = load_malnutrition()
    if not ob.empty and not mn.empty:
        st.subheader("📊 Obesity vs Malnutrition by Region — Side-by-Side")
        st.plotly_chart(plot_grouped_bar(ob, mn, "Region"), use_container_width=True)
        st.subheader("⚧ Gender Disparity Across Both Conditions")
        st.plotly_chart(plot_grouped_bar(ob, mn, "Gender"), use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════
# PAGE 6 — COUNTRY DEEP-DIVE
# ═══════════════════════════════════════════════════════════════════════════
elif page == "🌍 Country Deep-Dive":

    st.markdown("""
    <div class="page-title">
        <h2>🌍 Country Deep-Dive</h2>
        <p>Select any country to see its full obesity & malnutrition profile across all years,
        genders, and age groups</p>
    </div>""", unsafe_allow_html=True)

    ob = load_obesity()
    mn = load_malnutrition()

    all_countries = sorted(
        set(ob["Country"].dropna().unique()) | set(mn["Country"].dropna().unique())
    )

    col_sel, col_year = st.columns([3, 1])
    with col_sel:
        selected_country = st.selectbox(
            "Choose a country",
            all_countries,
            index=all_countries.index("India") if "India" in all_countries else 0,
        )
    with col_year:
        age_filter = st.selectbox("Age group", ["Both (all)", "Adult", "Child/Adolescent"],
                                  key="dd_age")

    age_map = {"Both (all)": None, "Adult": "Adult", "Child/Adolescent": "Child/Adolescent"}
    age_sel = age_map[age_filter]

    ob_c = ob[ob["Country"] == selected_country].copy()
    mn_c = mn[mn["Country"] == selected_country].copy()
    if age_sel:
        ob_c = ob_c[ob_c["Age_Group"] == age_sel]
        mn_c = mn_c[mn_c["Age_Group"] == age_sel]

    st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)

    # ── Country KPIs ──────────────────────────────────────────────────
    ob_2022 = ob_c[(ob_c["Year"] == 2022) & (ob_c["Gender"] == "Both")]["Mean_Estimate"].mean()
    mn_2022 = mn_c[(mn_c["Year"] == 2022) & (mn_c["Gender"] == "Both")]["Mean_Estimate"].mean()
    ob_2012 = ob_c[(ob_c["Year"] == 2012) & (ob_c["Gender"] == "Both")]["Mean_Estimate"].mean()
    mn_2012 = mn_c[(mn_c["Year"] == 2012) & (mn_c["Gender"] == "Both")]["Mean_Estimate"].mean()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🔴 Obesity 2022",      f"{ob_2022:.1f}%"  if not pd.isna(ob_2022) else "N/A",
              delta=f"{ob_2022 - ob_2012:+.1f}% since 2012" if not pd.isna(ob_2012) else None)
    c2.metric("🔵 Malnutrition 2022", f"{mn_2022:.1f}%"  if not pd.isna(mn_2022) else "N/A",
              delta=f"{mn_2022 - mn_2012:+.1f}% since 2012" if not pd.isna(mn_2012) else None)
    c3.metric("🌐 Region", ob_c["Region"].mode()[0] if not ob_c.empty else "—")
    c4.metric("📅 Data Points", f"{len(ob_c) + len(mn_c):,}")

    # ── Insight box based on country stats ───────────────────────────
    if not pd.isna(ob_2022) and not pd.isna(mn_2022):
        if ob_2022 > 15 and mn_2022 > 10:
            st.markdown(f"""
            <div class="insight-box">
                <h3>⚠️ Dual Burden Detected — {selected_country}</h3>
                <p><strong>{selected_country}</strong> shows elevated obesity
                (<strong>{ob_2022:.1f}%</strong>) alongside significant malnutrition
                (<strong>{mn_2022:.1f}%</strong>) — a dual burden country that requires
                integrated public health strategies addressing both over- and undernutrition
                simultaneously, rather than treating them as separate problems.</p>
            </div>""", unsafe_allow_html=True)
        elif ob_2022 > 25:
            st.markdown(f"""
            <div class="insight-box-red">
                <h3>🔴 High Obesity Alert — {selected_country}</h3>
                <p>Obesity at <strong>{ob_2022:.1f}%</strong> in 2022 is significantly above the
                global average. Policy focus should target dietary education, urban food
                environments, and physical activity promotion.</p>
            </div>""", unsafe_allow_html=True)
        elif mn_2022 > 20:
            st.markdown(f"""
            <div class="insight-box-blue">
                <h3>🔵 High Malnutrition Alert — {selected_country}</h3>
                <p>Malnutrition at <strong>{mn_2022:.1f}%</strong> in 2022 signals persistent
                food insecurity. Immediate intervention via social protection programs, school
                feeding schemes, and agricultural development is recommended.</p>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="insight-box-green">
                <h3>✅ Relatively Balanced — {selected_country}</h3>
                <p>Obesity at <strong>{ob_2022:.1f}%</strong> and malnutrition at
                <strong>{mn_2022:.1f}%</strong> are both below major alert thresholds.
                Continued monitoring is recommended to prevent upward trends in either direction.</p>
            </div>""", unsafe_allow_html=True)

    st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)

    # ── Trend charts ──────────────────────────────────────────────────
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(f"🔴 Obesity Trend — {selected_country}")
        ob_trend = (ob_c[ob_c["Gender"] == "Both"]
                    .groupby("Year")["Mean_Estimate"].mean().reset_index())
        if not ob_trend.empty:
            fig = px.line(ob_trend, x="Year", y="Mean_Estimate", markers=True,
                          color_discrete_sequence=["#ef4444"])
            fig.update_traces(line_width=3, marker_size=9)
            fig.update_layout(template="plotly_dark",
                               paper_bgcolor="rgba(0,0,0,0)",
                               plot_bgcolor="rgba(0,0,0,0)",
                               yaxis_title="Obesity (%)", hovermode="x unified")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No obesity data for this selection.")

    with col2:
        st.subheader(f"🔵 Malnutrition Trend — {selected_country}")
        mn_trend = (mn_c[mn_c["Gender"] == "Both"]
                    .groupby("Year")["Mean_Estimate"].mean().reset_index())
        if not mn_trend.empty:
            fig2 = px.line(mn_trend, x="Year", y="Mean_Estimate", markers=True,
                           color_discrete_sequence=["#3b82f6"])
            fig2.update_traces(line_width=3, marker_size=9)
            fig2.update_layout(template="plotly_dark",
                                paper_bgcolor="rgba(0,0,0,0)",
                                plot_bgcolor="rgba(0,0,0,0)",
                                yaxis_title="Malnutrition (%)", hovermode="x unified")
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No malnutrition data for this selection.")

    # ── Gender breakdown ──────────────────────────────────────────────
    st.subheader(f"⚧ Gender Breakdown — {selected_country}")
    col3, col4 = st.columns(2)
    with col3:
        ob_g = (ob_c[ob_c["Gender"].isin(["Male", "Female"])]
                .groupby(["Year", "Gender"])["Mean_Estimate"].mean().reset_index())
        if not ob_g.empty:
            fig3 = px.line(ob_g, x="Year", y="Mean_Estimate", color="Gender",
                           markers=True,
                           color_discrete_map={"Male": "#3b82f6", "Female": "#f472b6"})
            fig3.update_layout(template="plotly_dark",
                                paper_bgcolor="rgba(0,0,0,0)",
                                plot_bgcolor="rgba(0,0,0,0)",
                                title="Obesity by Gender", hovermode="x unified")
            st.plotly_chart(fig3, use_container_width=True)

    with col4:
        mn_g = (mn_c[mn_c["Gender"].isin(["Male", "Female"])]
                .groupby(["Year", "Gender"])["Mean_Estimate"].mean().reset_index())
        if not mn_g.empty:
            fig4 = px.line(mn_g, x="Year", y="Mean_Estimate", color="Gender",
                           markers=True,
                           color_discrete_map={"Male": "#3b82f6", "Female": "#f472b6"})
            fig4.update_layout(template="plotly_dark",
                                paper_bgcolor="rgba(0,0,0,0)",
                                plot_bgcolor="rgba(0,0,0,0)",
                                title="Malnutrition by Gender", hovermode="x unified")
            st.plotly_chart(fig4, use_container_width=True)

    # ── Raw data table ────────────────────────────────────────────────
    st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)
    st.subheader(f"📋 Raw Data — {selected_country}")
    tab_ob, tab_mn = st.tabs(["Obesity Records", "Malnutrition Records"])
    with tab_ob:
        if not ob_c.empty:
            st.dataframe(ob_c.sort_values(["Year", "Gender"]), use_container_width=True, height=350)
            st.download_button("📥 Download Obesity Data",
                               ob_c.to_csv(index=False),
                               file_name=f"{selected_country}_obesity.csv")
        else:
            st.info("No obesity records for this country / age filter.")
    with tab_mn:
        if not mn_c.empty:
            st.dataframe(mn_c.sort_values(["Year", "Gender"]), use_container_width=True, height=350)
            st.download_button("📥 Download Malnutrition Data",
                               mn_c.to_csv(index=False),
                               file_name=f"{selected_country}_malnutrition.csv")
        else:
            st.info("No malnutrition records for this country / age filter.")


# ═══════════════════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════════════════
st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align:center; color:#64748b; font-size:0.8rem; padding: 8px 0 16px;'>
    <strong style='color:#667eea'>⚖️ Nutrition Paradox</strong> &nbsp;|&nbsp;
    Data: WHO Global Health Observatory API &nbsp;|&nbsp;
    Period: 2012–2022 &nbsp;|&nbsp;
    Built with Streamlit · Plotly · SQLite · Python
</div>
""", unsafe_allow_html=True)