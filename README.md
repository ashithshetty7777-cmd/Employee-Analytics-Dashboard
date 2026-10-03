# Employee Data Analytics Project

An end-to-end HR analytics pipeline that generates synthetic employee data, loads it into MySQL, runs SQL-based analysis, and produces Python/Matplotlib visualizations — plus a Tableau dashboard.

---

## Project Structure

```
project/
├── generate_employees.py   # Generate 5,000 synthetic employee records → CSV
├── employee_data.csv       # Generated dataset (output of above)
├── load_to_mysql.py        # Clean & load CSV into MySQL
├── verify_data.py          # Quick sanity-check on the CSV
├── analysis.sql            # 30+ SQL queries across 8 analysis sections
├── eda_analysis.py         # EDA + 9 Matplotlib/Seaborn charts
└── charts/
    ├── 01_dept_headcount.png
    ├── 02_avg_salary_dept.png
    ├── 03_performance_distribution.png
    ├── 04_salary_boxplot.png
    ├── 05_experience_vs_salary.png
    ├── 06_status_pie.png
    ├── 07_attendance_vs_performance.png
    ├── 08_correlation_heatmap.png
    ├── 09_dashboard.png
    └── Employee Analytics Dashboard.twb   # Tableau workbook
```

---

## Dataset

5,000 synthetic employee records generated with [Faker](https://faker.readthedocs.io/) (Indian locale) and seeded for reproducibility.

| Column | Description |
|---|---|
| `Employee_ID` | Unique ID (E1001 – E6000) |
| `Name` | Full name |
| `Gender` | Male / Female |
| `Age` | 22 – 58 |
| `Department` | 10 departments (IT, HR, Finance, …) |
| `Role` | Role within department |
| `Experience_Years` | 0 – 35 years |
| `Education` | Highest qualification |
| `City` | One of 10 major Indian cities |
| `Salary_INR` | Department-based range (₹18K – ₹2L) |
| `Performance_Score` | Normal distribution ~75, clamped 40–100 |
| `Attendance_Pct` | Normal distribution ~90%, clamped 55–100 |
| `Status` | Active (85%) / On Leave (8%) / Resigned (5%) / Terminated (2%) |
| `Joining_Year` | Derived from experience |
| `Email` / `Phone` | Faker-generated contact info |

---

## Prerequisites

- Python 3.8+
- MySQL 8.0+

Install Python dependencies:

```bash
pip install pandas faker mysql-connector-python matplotlib seaborn
```

---

## Usage

### Step 1 — Generate the dataset

```bash
python generate_employees.py
```

Outputs `employee_data.csv` with 5,000 rows.

### Step 2 — (Optional) Verify the CSV

```bash
python verify_data.py
```

Prints row counts, null checks, data types, and value ranges.

### Step 3 — Load into MySQL

Edit the `CONFIG` block at the top of `load_to_mysql.py` with your credentials:

```python
HOST     = "localhost"
PORT     = 3306
USER     = "root"
PASSWORD = "your_password"
DATABASE = "employee_db"
```

Then run:

```bash
python load_to_mysql.py
```

This creates the `employee_db` database and `employees` table, cleans the data, and inserts all records in batches of 500.

### Step 4 — Run SQL analysis

Open `analysis.sql` in MySQL Workbench (or any MySQL client) and run queries from any of the 8 sections:

| Section | Topics |
|---|---|
| 1 — Overview | Total count, gender split, status breakdown, city headcount |
| 2 — Department | Headcount, avg salary, avg performance, full summary |
| 3 — Salary | Top/bottom earners, salary brackets, salary vs experience |
| 4 — Performance | Categories, top/bottom performers, underpaid high performers |
| 5 — Attendance | Categories, at-risk employees, departments with issues |
| 6 — Attrition | Overall rate, by department, by experience, left vs stayed |
| 7 — Role & Experience | Common roles, avg experience, promotion eligibility |
| 8 — Advanced | Window functions: salary rank, vs dept avg, cumulative hires |

### Step 5 — Generate charts

Update the DB credentials in `eda_analysis.py` (same `CONFIG` block pattern), then:

```bash
python eda_analysis.py
```

Saves 9 PNG charts to the `charts/` directory.

---

## Charts

| # | Chart | What it shows |
|---|---|---|
| 1 | Department Headcount | Horizontal bar — employee count per dept |
| 2 | Avg Salary by Dept | Bar chart with value labels |
| 3 | Performance Distribution | Histogram with mean line |
| 4 | Salary Box Plot | Distribution spread per department |
| 5 | Experience vs Salary | Scatter coloured by performance score |
| 6 | Status Pie | Active / On Leave / Resigned / Terminated share |
| 7 | Attendance vs Performance | Scatter by employment status |
| 8 | Correlation Heatmap | Age, experience, salary, performance, attendance |
| 9 | Dashboard | All 8 panels combined in a single 3×3 grid |

---

## Tableau

`charts/Employee Analytics Dashboard.twb` is a Tableau workbook built on top of the same dataset. Open it in Tableau Desktop (2021.1+) and point the data source to your `employee_data.csv` or the MySQL connection.

---

## Notes

- All scripts use `random.seed(42)` and `Faker.seed(42)` so the generated data is fully reproducible.
- `load_to_mysql.py` uses `INSERT IGNORE` — safe to re-run without creating duplicate rows.
- Salary is rounded to the nearest ₹1,000 and senior employees trend toward the top of their department's range.
