import streamlit as st
import sqlite3, pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="⚖️ Nutrition Paradox",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

DB = "nutrition.db"

@st.cache_data
def run_query(sql):
    conn = sqlite3.connect(DB)
    df = pd.read_sql_query(sql, conn)
    conn.close()
    return df

@st.cache_data
def load_table(table):
    return run_query(f"SELECT * FROM {table}")

# ── Sidebar navigation ─────────────────────────────────────────
with st.sidebar:
    st.image("https://www.who.int/images/default-source/infographics/who-logo.png", width=120)
    st.markdown("## ⚖️ Nutrition Paradox")
    st.markdown("*WHO Global Health Analytics*")
    page = option_menu(
        menu_title=None,
        options=["🏠 Overview","📊 EDA","🔴 Obesity Queries",
                 "🔵 Malnutrition Queries","🔗 Combined Queries",
                 "🌍 Country Deep-Dive"],
        icons=["house","bar-chart","circle","circle","link","globe"],
        default_index=0
    )

# ── Pages ─────────────────────────────────────────────────────
if page == "🏠 Overview":
    st.title("⚖️ Nutrition Paradox: A Global View")
    st.markdown("""
    > *The world faces a dual burden: while obesity rates rise, 
    malnutrition persists — often in the same countries.*
    """)
    col1, col2, col3, col4 = st.columns(4)
    ob = load_table("obesity")
    mn = load_table("malnutrition")
    col1.metric("Obesity Records",   f"{len(ob):,}")
    col2.metric("Malnutrition Records", f"{len(mn):,}")
    col3.metric("Countries",  ob["Country"].nunique())
    col4.metric("Years Covered", "2012–2022")

    # Paradox scatter (recruiter wow chart)
    st.subheader("The Paradox — Obesity vs Malnutrition by Country (2022)")
    ob22 = ob[(ob.Year==2022)&(ob.Gender=="Both")].groupby("Country")["Mean_Estimate"].mean().reset_index(name="Obesity")
    mn22 = mn[(mn.Year==2022)&(mn.Gender=="Both")].groupby(["Country","Region"])["Mean_Estimate"].mean().reset_index(name="Malnutrition")
    scatter_df = ob22.merge(mn22, on="Country").dropna()
    fig = px.scatter(scatter_df, x="Obesity", y="Malnutrition",
                     color="Region", hover_name="Country", size_max=12,
                     title="Countries face both challenges simultaneously",
                     labels={"Obesity":"Obesity %","Malnutrition":"Malnutrition %"})
    st.plotly_chart(fig, use_container_width=True)

elif page == "📊 EDA":
    st.title("Exploratory Data Analysis")
    ob = load_table("obesity")
    mn = load_table("malnutrition")
    tab1, tab2 = st.tabs(["Obesity", "Malnutrition"])
    with tab1:
        st.subheader("Global Obesity Trend")
        trend = ob[ob.Gender=="Both"].groupby("Year")["Mean_Estimate"].mean().reset_index()
        fig = px.line(trend, x="Year", y="Mean_Estimate", markers=True,
                      color_discrete_sequence=["#E24B4A"])
        st.plotly_chart(fig, use_container_width=True)
        st.subheader("Distribution by Region (Box Plot)")
        fig2 = px.box(ob[ob.Gender=="Both"], x="Region", y="Mean_Estimate",
                      color="Region", title="Obesity spread by WHO region")
        st.plotly_chart(fig2, use_container_width=True)
    with tab2:
        st.subheader("Global Malnutrition Trend")
        trend2 = mn[mn.Gender=="Both"].groupby("Year")["Mean_Estimate"].mean().reset_index()
        fig3 = px.line(trend2, x="Year", y="Mean_Estimate", markers=True,
                       color_discrete_sequence=["#378ADD"])
        st.plotly_chart(fig3, use_container_width=True)

elif page == "🔴 Obesity Queries":
    st.title("Obesity: SQL Query Results")
    queries = {
        "Q1 · Top 5 regions (2022)": """
            SELECT Region, ROUND(AVG(Mean_Estimate),2) AS avg_obesity
            FROM obesity WHERE Year=2022 AND Gender='Both'
            GROUP BY Region ORDER BY avg_obesity DESC LIMIT 5""",
        "Q2 · Top 5 countries": """
            SELECT Country, ROUND(AVG(Mean_Estimate),2) AS avg_obesity
            FROM obesity WHERE Gender='Both'
            GROUP BY Country ORDER BY avg_obesity DESC LIMIT 5""",
        # ... add remaining 8 queries
    }
    selected = st.selectbox("Select Query", list(queries.keys()))
    df_result = run_query(queries[selected])
    col1, col2 = st.columns(2)
    with col1: st.dataframe(df_result, use_container_width=True)
    with col2: st.bar_chart(df_result.set_index(df_result.columns[0]))

elif page == "🌍 Country Deep-Dive":
    st.title("Country Deep-Dive")
    ob = load_table("obesity")
    mn = load_table("malnutrition")
    countries = sorted(ob["Country"].dropna().unique())
    selected_country = st.selectbox("Choose a country", countries, index=countries.index("India") if "India" in countries else 0)
    col1, col2 = st.columns(2)
    with col1:
        ob_c = ob[(ob.Country==selected_country)&(ob.Gender=="Both")].groupby("Year")["Mean_Estimate"].mean().reset_index()
        fig = px.line(ob_c, x="Year", y="Mean_Estimate", title=f"Obesity trend — {selected_country}",
                      color_discrete_sequence=["#E24B4A"], markers=True)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        mn_c = mn[(mn.Country==selected_country)&(mn.Gender=="Both")].groupby("Year")["Mean_Estimate"].mean().reset_index()
        fig2 = px.line(mn_c, x="Year", y="Mean_Estimate", title=f"Malnutrition trend — {selected_country}",
                       color_discrete_sequence=["#378ADD"], markers=True)
        st.plotly_chart(fig2, use_container_width=True)