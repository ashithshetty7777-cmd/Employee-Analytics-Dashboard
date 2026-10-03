"""
Employee Dummy Data Generator
Generates 5000 realistic employee records using Faker, Pandas, and Random.
Output: employee_data.csv
"""

import pandas as pd
from faker import Faker
import random

fake = Faker("en_IN")  # Indian locale for realistic Indian names

# ── Configuration ──────────────────────────────────────────────────────────────
NUM_RECORDS = 5000

DEPARTMENTS = [
    "IT", "HR", "Finance", "Marketing", "Sales",
    "Operations", "Legal", "R&D", "Customer Support", "Admin"
]

ROLES = {
    "IT":               ["Software Engineer", "DevOps Engineer", "QA Engineer", "Data Analyst", "Tech Lead"],
    "HR":               ["HR Executive", "Recruiter", "HR Manager", "Payroll Specialist"],
    "Finance":          ["Accountant", "Finance Analyst", "Auditor", "CFO Assistant"],
    "Marketing":        ["Marketing Executive", "SEO Analyst", "Content Writer", "Brand Manager"],
    "Sales":            ["Sales Executive", "Account Manager", "Business Development Manager"],
    "Operations":       ["Operations Executive", "Logistics Manager", "Supply Chain Analyst"],
    "Legal":            ["Legal Advisor", "Compliance Officer", "Contract Manager"],
    "R&D":              ["Research Scientist", "Product Developer", "Innovation Lead"],
    "Customer Support": ["Support Executive", "Customer Success Manager", "Help Desk Analyst"],
    "Admin":            ["Admin Executive", "Office Manager", "Receptionist"],
}

SALARY_RANGE = {
    "IT":               (40000, 180000),
    "HR":               (30000, 90000),
    "Finance":          (35000, 120000),
    "Marketing":        (30000, 100000),
    "Sales":            (25000, 110000),
    "Operations":       (28000, 95000),
    "Legal":            (45000, 150000),
    "R&D":              (50000, 200000),
    "Customer Support": (20000, 60000),
    "Admin":            (18000, 55000),
}

CITIES = [
    "Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai",
    "Pune", "Kolkata", "Ahmedabad", "Jaipur", "Noida"
]

EDUCATION = ["B.Tech", "B.Sc", "BBA", "B.Com", "MBA", "M.Tech", "MCA", "B.E", "M.Sc"]

STATUS_WEIGHTS = ["Active"] * 85 + ["On Leave"] * 8 + ["Resigned"] * 5 + ["Terminated"] * 2

# ── Generator ──────────────────────────────────────────────────────────────────
def generate_employee(emp_num: int) -> dict:
    dept        = random.choice(DEPARTMENTS)
    role        = random.choice(ROLES[dept])
    age         = random.randint(22, 58)
    experience  = min(random.randint(0, age - 21), 35)          # can't exceed working age
    sal_min, sal_max = SALARY_RANGE[dept]
    # Senior employees trend higher
    salary_base = sal_min + (sal_max - sal_min) * (experience / 35)
    salary      = int(salary_base * random.uniform(0.85, 1.15) / 1000) * 1000  # round to 1k
    salary      = max(sal_min, min(sal_max, salary))

    performance = round(random.gauss(75, 12), 1)    # normal distribution ~75
    performance = max(40.0, min(100.0, performance))

    attendance  = round(random.gauss(90, 7), 1)
    attendance  = max(55.0, min(100.0, attendance))

    gender      = random.choice(["Male", "Female", "Male"])     # slight male skew
    name        = fake.name_male() if gender == "Male" else fake.name_female()

    return {
        "Employee_ID":      f"E{1000 + emp_num}",
        "Name":             name,
        "Gender":           gender,
        "Age":              age,
        "Department":       dept,
        "Role":             role,
        "Experience_Years": experience,
        "Education":        random.choice(EDUCATION),
        "City":             random.choice(CITIES),
        "Salary_INR":       salary,
        "Performance_Score":performance,
        "Attendance_Pct":   attendance,
        "Status":           random.choice(STATUS_WEIGHTS),
        "Joining_Year":     2024 - experience - random.randint(0, 2),
        "Email":            fake.email(),
        "Phone":            fake.phone_number(),
    }


def main():
    random.seed(42)
    Faker.seed(42)

    print(f"Generating {NUM_RECORDS} employee records …")
    records = [generate_employee(i) for i in range(1, NUM_RECORDS + 1)]

    df = pd.DataFrame(records)

    # Tidy up types
    df["Salary_INR"]        = df["Salary_INR"].astype(int)
    df["Performance_Score"] = df["Performance_Score"].round(1)
    df["Attendance_Pct"]    = df["Attendance_Pct"].round(1)

    output_file = "employee_data.csv"
    df.to_csv(output_file, index=False)

    print(f"\n✅  Saved {len(df)} records to '{output_file}'")
    print("\n── Sample Records ──────────────────────────────────────────")
    print(df.head(5).to_string(index=False))
    print("\n── Dataset Summary ─────────────────────────────────────────")
    print(f"  Total records   : {len(df)}")
    print(f"  Departments     : {df['Department'].nunique()}")
    print(f"  Unique roles    : {df['Role'].nunique()}")
    print(f"  Avg Salary      : ₹{df['Salary_INR'].mean():,.0f}")
    print(f"  Avg Performance : {df['Performance_Score'].mean():.1f}")
    print(f"  Avg Attendance  : {df['Attendance_Pct'].mean():.1f}%")
    print(f"  Status split    :\n{df['Status'].value_counts().to_string()}")


if __name__ == "__main__":
    main()
