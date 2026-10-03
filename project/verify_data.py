import pandas as pd

df = pd.read_csv("employee_data.csv")

print("=== FILE VERIFICATION ===")
print(f"Total rows     : {len(df)}")
print(f"Total columns  : {len(df.columns)}")
print(f"Columns        : {list(df.columns)}")

print("\n=== NULL CHECK ===")
print(df.isnull().sum())

print("\n=== DATA TYPES ===")
print(df.dtypes)

print("\n=== SAMPLE (first 3 rows) ===")
print(df.head(3).T.to_string())

print("\n=== VALUE RANGES ===")
print(f"Employee_ID range : {df['Employee_ID'].iloc[0]} → {df['Employee_ID'].iloc[-1]}")
print(f"Age               : {df['Age'].min()} – {df['Age'].max()}")
print(f"Salary_INR        : Rs.{df['Salary_INR'].min():,} – Rs.{df['Salary_INR'].max():,}")
print(f"Performance_Score : {df['Performance_Score'].min()} – {df['Performance_Score'].max()}")
print(f"Attendance_Pct    : {df['Attendance_Pct'].min()} – {df['Attendance_Pct'].max()}")

print("\n=== DEPT DISTRIBUTION ===")
print(df["Department"].value_counts().to_string())

print("\n=== STATUS DISTRIBUTION ===")
print(df["Status"].value_counts().to_string())

print("\n=== GENDER DISTRIBUTION ===")
print(df["Gender"].value_counts().to_string())

print("\n=== NUMERIC SUMMARY ===")
print(df[["Age", "Experience_Years", "Salary_INR", "Performance_Score", "Attendance_Pct"]].describe().round(1).to_string())
