# -*- coding: utf-8 -*-
"""
Employee Data -> MySQL Loader
============================
Flow:  CSV  →  Clean  →  MySQL

Steps performed:
  1. Read employee_data.csv
  2. Clean & validate the data
  3. Connect to MySQL
  4. Create database + table (if not exists)
  5. Insert all records
  6. Verify row count

SETUP — edit the CONFIG block below before running:
  HOST     : MySQL server address  (usually localhost)
  PORT     : MySQL port            (usually 3306)
  USER     : your MySQL username   (usually root)
  PASSWORD : your MySQL password
  DATABASE : name of the DB to create / use
"""

import pandas as pd
import mysql.connector
from mysql.connector import Error
import sys

# ── CONFIG — edit these values ────────────────────────────────────────────────
HOST     = "localhost"
PORT     = 3306
USER     = "root"
PASSWORD = "Admin@123"
DATABASE = "employee_db"
TABLE    = "employees"
CSV_FILE = "employee_data.csv"
# ─────────────────────────────────────────────────────────────────────────────


# ── STEP 1: Read CSV ──────────────────────────────────────────────────────────
def load_csv(path: str) -> pd.DataFrame:
    print(f"[1/5] Reading '{path}' …")
    df = pd.read_csv(path)
    print(f"      Loaded {len(df):,} rows × {len(df.columns)} columns")
    return df


# ── STEP 2: Clean Data ────────────────────────────────────────────────────────
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    print("[2/5] Cleaning data …")

    # Drop full duplicates
    before = len(df)
    df = df.drop_duplicates()
    print(f"      Removed {before - len(df)} duplicate rows")

    # Drop rows where critical fields are null
    df = df.dropna(subset=["Employee_ID", "Name", "Department"])

    # Normalise text columns
    str_cols = ["Name", "Gender", "Department", "Role",
                "Education", "City", "Status"]
    for col in str_cols:
        df[col] = df[col].str.strip().str.title()

    # Clamp numeric ranges
    df["Performance_Score"] = df["Performance_Score"].clip(0, 100)
    df["Attendance_Pct"]    = df["Attendance_Pct"].clip(0, 100)
    df["Age"]               = df["Age"].clip(18, 65)
    df["Experience_Years"]  = df["Experience_Years"].clip(0, 45)
    df["Salary_INR"]        = df["Salary_INR"].clip(0)

    # Fix types
    df["Salary_INR"]       = df["Salary_INR"].astype(int)
    df["Age"]              = df["Age"].astype(int)
    df["Experience_Years"] = df["Experience_Years"].astype(int)
    df["Joining_Year"]     = df["Joining_Year"].astype(int)

    print(f"      Clean rows ready: {len(df):,}")
    return df


# ── STEP 3: Connect to MySQL ──────────────────────────────────────────────────
def get_connection(database: str = None):
    """Return a MySQL connection. Pass database=None to connect without DB."""
    print(f"[3/5] Connecting to MySQL at {HOST}:{PORT} as '{USER}' …")
    try:
        conn = mysql.connector.connect(
            host=HOST,
            port=PORT,
            user=USER,
            password=PASSWORD,
            database=database,
            autocommit=False,
        )
        print("      Connected ✓")
        return conn
    except Error as e:
        print(f"\n❌  Connection failed: {e}")
        print("\nTroubleshooting tips:")
        print("  • Make sure MySQL server is running")
        print("  • Check HOST, PORT, USER, PASSWORD in the CONFIG block")
        print("  • Grant privileges: GRANT ALL ON employee_db.* TO 'root'@'localhost';")
        sys.exit(1)


# ── STEP 4: Create Database & Table ──────────────────────────────────────────
CREATE_TABLE_SQL = f"""
CREATE TABLE IF NOT EXISTS {TABLE} (
    id               INT AUTO_INCREMENT PRIMARY KEY,
    employee_id      VARCHAR(10)    NOT NULL UNIQUE,
    name             VARCHAR(100)   NOT NULL,
    gender           VARCHAR(10),
    age              TINYINT UNSIGNED,
    department       VARCHAR(50),
    role             VARCHAR(100),
    experience_years TINYINT UNSIGNED,
    education        VARCHAR(50),
    city             VARCHAR(50),
    salary_inr       INT UNSIGNED,
    performance_score DECIMAL(5,1),
    attendance_pct   DECIMAL(5,1),
    status           VARCHAR(20),
    joining_year     SMALLINT UNSIGNED,
    email            VARCHAR(150),
    phone            VARCHAR(20),
    created_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""

def setup_database(conn):
    print(f"[4/5] Setting up database '{DATABASE}' and table '{TABLE}' …")
    cursor = conn.cursor()

    # Create DB if it doesn't exist
    cursor.execute(
        f"CREATE DATABASE IF NOT EXISTS {DATABASE} "
        f"CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
    )
    cursor.execute(f"USE {DATABASE};")

    # Create table
    cursor.execute(CREATE_TABLE_SQL)
    conn.commit()
    cursor.close()
    print(f"      Database & table ready ✓")


# ── STEP 5: Insert Data ───────────────────────────────────────────────────────
INSERT_SQL = f"""
    INSERT IGNORE INTO {TABLE}
        (employee_id, name, gender, age, department, role,
         experience_years, education, city, salary_inr,
         performance_score, attendance_pct, status,
         joining_year, email, phone)
    VALUES
        (%s, %s, %s, %s, %s, %s,
         %s, %s, %s, %s,
         %s, %s, %s,
         %s, %s, %s)
"""

def insert_data(conn, df: pd.DataFrame):
    print(f"[5/5] Inserting {len(df):,} records into '{TABLE}' …")
    cursor = conn.cursor()

    # Convert DataFrame to list of tuples
    records = [
        (
            row["Employee_ID"],
            row["Name"],
            row["Gender"],
            int(row["Age"]),
            row["Department"],
            row["Role"],
            int(row["Experience_Years"]),
            row["Education"],
            row["City"],
            int(row["Salary_INR"]),
            float(row["Performance_Score"]),
            float(row["Attendance_Pct"]),
            row["Status"],
            int(row["Joining_Year"]),
            row["Email"],
            str(row["Phone"]),
        )
        for _, row in df.iterrows()
    ]

    # Batch insert in chunks of 500 for efficiency
    BATCH = 500
    inserted = 0
    for i in range(0, len(records), BATCH):
        chunk = records[i : i + BATCH]
        cursor.executemany(INSERT_SQL, chunk)
        conn.commit()
        inserted += len(chunk)
        print(f"      Inserted {inserted:,} / {len(records):,} rows …", end="\r")

    cursor.close()
    print(f"\n      Done — {inserted:,} rows inserted ✓")


# ── STEP 6: Verify ────────────────────────────────────────────────────────────
def verify(conn):
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {TABLE};")
    count = cursor.fetchone()[0]

    cursor.execute(
        f"SELECT department, COUNT(*) AS cnt "
        f"FROM {TABLE} GROUP BY department ORDER BY cnt DESC;"
    )
    dept_rows = cursor.fetchall()

    cursor.execute(
        f"SELECT AVG(salary_inr), AVG(performance_score), AVG(attendance_pct) "
        f"FROM {TABLE};"
    )
    avg_sal, avg_perf, avg_att = cursor.fetchone()

    cursor.close()

    print("\n── Verification ────────────────────────────────────────────")
    print(f"  Total rows in MySQL : {count:,}")
    print(f"  Avg Salary          : Rs.{avg_sal:,.0f}")
    print(f"  Avg Performance     : {avg_perf:.1f}")
    print(f"  Avg Attendance      : {avg_att:.1f}%")
    print("\n  Department counts:")
    for dept, cnt in dept_rows:
        print(f"    {dept:<20} {cnt}")


# ── MAIN ──────────────────────────────────────────────────────────────────────
def main():
    print("=" * 55)
    print("  Employee Data → MySQL Pipeline")
    print("=" * 55)

    # 1. Load
    df = load_csv(CSV_FILE)

    # 2. Clean
    df = clean_data(df)

    # 3. Connect (without DB first, so we can create it)
    conn = get_connection(database=None)

    # 4. Setup DB & table
    setup_database(conn)

    # Reconnect to the specific database
    conn.close()
    conn = get_connection(database=DATABASE)

    # 5. Insert
    insert_data(conn, df)

    # 6. Verify
    verify(conn)

    conn.close()
    print("\n✅  Pipeline complete! Data is now in MySQL.")
    print(f"    Connect with: USE {DATABASE}; SELECT * FROM {TABLE} LIMIT 10;")



if __name__ == "__main__":
    main()
