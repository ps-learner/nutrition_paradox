import sqlite3, pandas as pd
from pathlib import Path

DB_PATH = "nutrition.db"

def get_conn():
    return sqlite3.connect(DB_PATH)

def create_tables():
    conn = get_conn()
    cur = conn.cursor()
    cur.executescript("""
    CREATE TABLE IF NOT EXISTS obesity (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        Year            INTEGER,
        Gender          TEXT,
        Mean_Estimate   REAL,
        LowerBound      REAL,
        UpperBound      REAL,
        Age_Group       TEXT,
        Country         TEXT,
        Region          TEXT,
        CI_Width        REAL,
        Obesity_Level   TEXT
    );
    CREATE TABLE IF NOT EXISTS malnutrition (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        Year            INTEGER,
        Gender          TEXT,
        Mean_Estimate   REAL,
        LowerBound      REAL,
        UpperBound      REAL,
        Age_Group       TEXT,
        Country         TEXT,
        Region          TEXT,
        CI_Width        REAL,
        Malnutrition_Level TEXT
    );
    CREATE INDEX IF NOT EXISTS idx_ob_country ON obesity(Country);
    CREATE INDEX IF NOT EXISTS idx_ob_year    ON obesity(Year);
    CREATE INDEX IF NOT EXISTS idx_mn_country ON malnutrition(Country);
    CREATE INDEX IF NOT EXISTS idx_mn_year    ON malnutrition(Year);
    """)
    conn.commit(); conn.close()
    print("Tables created.")

def insert_data(df_obesity, df_malnutrition):
    conn = get_conn()
    # Use pandas to_sql for speed (replace if re-running)
    ob_cols  = ["Year","Gender","Mean_Estimate","LowerBound","UpperBound",
                "Age_Group","Country","Region","CI_Width","Obesity_Level"]
    mn_cols  = ["Year","Gender","Mean_Estimate","LowerBound","UpperBound",
                "Age_Group","Country","Region","CI_Width","Malnutrition_Level"]
    df_obesity[ob_cols].to_sql("obesity",      conn, if_exists="replace", index=False)
    df_malnutrition[mn_cols].to_sql("malnutrition", conn, if_exists="replace", index=False)
    conn.close()
    print(f"Inserted: obesity={len(df_obesity):,}, malnutrition={len(df_malnutrition):,}")

# Run once
if __name__ == "__main__":
    import pandas as pd

    BASE_DIR = Path(__file__).resolve().parent.parent
    df_obesity = pd.read_csv (BASE_DIR / "data" / "processed" / "obesity_clean.csv")
    df_malnutrition = pd.read_csv (BASE_DIR / "data" / "processed" / "malnutrition_clean.csv")
    create_tables()
    insert_data(df_obesity, df_malnutrition)