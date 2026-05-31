# import sqlite3, pandas as pd
# from pathlib import Path

# DB_PATH = "nutrition.db"

# def get_conn():
#     return sqlite3.connect(DB_PATH)

# def create_tables():
#     conn = get_conn()
#     cur = conn.cursor()
#     cur.executescript("""
#     CREATE TABLE IF NOT EXISTS obesity (
#         id              INTEGER PRIMARY KEY AUTOINCREMENT,
#         Year            INTEGER,
#         Gender          TEXT,
#         Mean_Estimate   REAL,
#         LowerBound      REAL,
#         UpperBound      REAL,
#         Age_Group       TEXT,
#         Country         TEXT,
#         Region          TEXT,
#         CI_Width        REAL,
#         Obesity_Level   TEXT
#     );
#     CREATE TABLE IF NOT EXISTS malnutrition (
#         id              INTEGER PRIMARY KEY AUTOINCREMENT,
#         Year            INTEGER,
#         Gender          TEXT,
#         Mean_Estimate   REAL,
#         LowerBound      REAL,
#         UpperBound      REAL,
#         Age_Group       TEXT,
#         Country         TEXT,
#         Region          TEXT,
#         CI_Width        REAL,
#         Malnutrition_Level TEXT
#     );
#     CREATE INDEX IF NOT EXISTS idx_ob_country ON obesity(Country);
#     CREATE INDEX IF NOT EXISTS idx_ob_year    ON obesity(Year);
#     CREATE INDEX IF NOT EXISTS idx_mn_country ON malnutrition(Country);
#     CREATE INDEX IF NOT EXISTS idx_mn_year    ON malnutrition(Year);
#     """)
#     conn.commit(); conn.close()
#     print("Tables created.")

# def insert_data(df_obesity, df_malnutrition):
#     conn = get_conn()
#     # Use pandas to_sql for speed (replace if re-running)
#     ob_cols  = ["Year","Gender","Mean_Estimate","LowerBound","UpperBound",
#                 "Age_Group","Country","Region","CI_Width","Obesity_Level"]
#     mn_cols  = ["Year","Gender","Mean_Estimate","LowerBound","UpperBound",
#                 "Age_Group","Country","Region","CI_Width","Malnutrition_Level"]
#     df_obesity[ob_cols].to_sql("obesity",      conn, if_exists="replace", index=False)
#     df_malnutrition[mn_cols].to_sql("malnutrition", conn, if_exists="replace", index=False)
#     conn.close()
#     print(f"Inserted: obesity={len(df_obesity):,}, malnutrition={len(df_malnutrition):,}")

# # Run once
# if __name__ == "__main__":
#     import pandas as pd

#     BASE_DIR = Path(__file__).resolve().parent.parent
#     df_obesity = pd.read_csv (BASE_DIR / "data" / "processed" / "obesity_clean.csv")
#     df_malnutrition = pd.read_csv (BASE_DIR / "data" / "processed" / "malnutrition_clean.csv")
#     create_tables()
#     insert_data(df_obesity, df_malnutrition)









"""
db_utils.py  —  Database helpers for the Nutrition Paradox Streamlit app.
Handles SQLite connection, query execution, and summary stats.

nutrition.db lives one level above app/, so the path is ../nutrition.db
relative to this file's location.
"""

import os
import sqlite3
import pandas as pd
import streamlit as st

# ── Resolve DB path regardless of where streamlit is launched from ────────
_HERE   = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(_HERE, "..", "nutrition.db")


# ── Single cached connection ───────────────────────────────────────────────
@st.cache_resource
def get_connection():
    """Return a persistent SQLite connection (one per Streamlit session)."""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


# ── Generic query runner ───────────────────────────────────────────────────
def run_query(sql: str) -> tuple[pd.DataFrame | None, str | None]:
    """
    Execute any SQL string and return (DataFrame, None) on success
    or (None, error_message) on failure.
    """
    try:
        conn = get_connection()
        df   = pd.read_sql_query(sql, conn)
        return df, None
    except Exception as exc:
        return None, str(exc)


# ── Cached full-table loaders ─────────────────────────────────────────────
@st.cache_data(ttl=3600, show_spinner=False)
def load_obesity() -> pd.DataFrame:
    df, err = run_query("SELECT * FROM obesity")
    if err:
        st.error(f"Could not load obesity table: {err}")
        return pd.DataFrame()
    return df


@st.cache_data(ttl=3600, show_spinner=False)
def load_malnutrition() -> pd.DataFrame:
    df, err = run_query("SELECT * FROM malnutrition")
    if err:
        st.error(f"Could not load malnutrition table: {err}")
        return pd.DataFrame()
    return df


# ── Dashboard KPI stats ───────────────────────────────────────────────────
@st.cache_data(ttl=3600, show_spinner=False)
def get_dashboard_stats() -> dict:
    """
    Returns a dict of headline numbers for the Overview page metrics row.
    All values are safe to display even if a query fails.
    """
    stats = {
        "obesity_records":    0,
        "malnutrition_records": 0,
        "countries":          0,
        "years_covered":      "2012–2022",
        "highest_ob_country": "—",
        "highest_ob_pct":     0.0,
        "highest_mn_country": "—",
        "highest_mn_pct":     0.0,
        "dual_burden_count":  0,
    }

    # Obesity row count
    df, _ = run_query("SELECT COUNT(*) AS n FROM obesity")
    if df is not None:
        stats["obesity_records"] = int(df.iloc[0]["n"])

    # Malnutrition row count
    df, _ = run_query("SELECT COUNT(*) AS n FROM malnutrition")
    if df is not None:
        stats["malnutrition_records"] = int(df.iloc[0]["n"])

    # Unique countries (union of both tables)
    df, _ = run_query("""
        SELECT COUNT(DISTINCT Country) AS n FROM (
            SELECT Country FROM obesity
            UNION
            SELECT Country FROM malnutrition
        )
    """)
    if df is not None:
        stats["countries"] = int(df.iloc[0]["n"])

    # Highest obesity country (2022, Both, Adult)
    df, _ = run_query("""
        SELECT Country, ROUND(AVG(Mean_Estimate),1) AS pct
        FROM obesity
        WHERE Year=2022 AND Gender='Both' AND Age_Group='Adult'
        GROUP BY Country ORDER BY pct DESC LIMIT 1
    """)
    if df is not None and len(df):
        stats["highest_ob_country"] = df.iloc[0]["Country"]
        stats["highest_ob_pct"]     = float(df.iloc[0]["pct"])

    # Highest malnutrition country (2022, Both, Adult)
    df, _ = run_query("""
        SELECT Country, ROUND(AVG(Mean_Estimate),1) AS pct
        FROM malnutrition
        WHERE Year=2022 AND Gender='Both' AND Age_Group='Adult'
        GROUP BY Country ORDER BY pct DESC LIMIT 1
    """)
    if df is not None and len(df):
        stats["highest_mn_country"] = df.iloc[0]["Country"]
        stats["highest_mn_pct"]     = float(df.iloc[0]["pct"])

    # Dual-burden country count
    # (countries where both obesity avg > 10% AND malnutrition avg > 10%)
    df, _ = run_query("""
        SELECT COUNT(*) AS n FROM (
            SELECT o.Country
            FROM obesity o JOIN malnutrition m
              ON o.Country=m.Country AND o.Year=m.Year AND o.Gender=m.Gender
            WHERE o.Gender='Both'
            GROUP BY o.Country
            HAVING AVG(o.Mean_Estimate) > 10 AND AVG(m.Mean_Estimate) > 10
        )
    """)
    if df is not None:
        stats["dual_burden_count"] = int(df.iloc[0]["n"])

    return stats