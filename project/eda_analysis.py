# -*- coding: utf-8 -*-
"""
Employee Data - Python / Pandas EDA & Visualization
====================================================
Reads data from MySQL and generates 8 charts + 1 combined dashboard.

Output files saved in: charts/
"""

import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")   # non-interactive backend (no popup windows)
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import mysql.connector

# ── CONFIG ────────────────────────────────────────────────────────────────────
HOST     = "localhost"
PORT     = 3306
USER     = "root"
PASSWORD = "Admin@123"
DATABASE = "employee_db"
TABLE    = "employees"
OUT_DIR  = "charts"
# ─────────────────────────────────────────────────────────────────────────────

# Chart style
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({"figure.dpi": 130, "font.size": 10})

os.makedirs(OUT_DIR, exist_ok=True)


# ── Load data from MySQL ──────────────────────────────────────────────────────
def load_data() -> pd.DataFrame:
    print("Connecting to MySQL and loading data ...")
    conn = mysql.connector.connect(
        host=HOST, port=PORT, user=USER,
        password=PASSWORD, database=DATABASE
    )
    df = pd.read_sql(f"SELECT * FROM {TABLE}", conn)
    conn.close()
    print(f"Loaded {len(df):,} rows from MySQL\n")
    return df


def save(fig, name: str):
    path = os.path.join(OUT_DIR, name)
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {path}")


# ── Chart 1 : Department Headcount ───────────────────────────────────────────
def chart_dept_headcount(df):
    print("Chart 1 : Department headcount ...")
    counts = df["department"].value_counts().sort_values(ascending=True)
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.barh(counts.index, counts.values, color=sns.color_palette("muted", len(counts)))
    ax.bar_label(bars, padding=3)
    ax.set_title("Employee Count by Department", fontsize=13, fontweight="bold")
    ax.set_xlabel("Number of Employees")
    fig.tight_layout()
    save(fig, "01_dept_headcount.png")


# ── Chart 2 : Average Salary by Department ───────────────────────────────────
def chart_avg_salary(df):
    print("Chart 2 : Average salary by department ...")
    avg_sal = df.groupby("department")["salary_inr"].mean().sort_values(ascending=False).reset_index()
    fig, ax = plt.subplots(figsize=(9, 5))
    sns.barplot(data=avg_sal, x="department", y="salary_inr", palette="Blues_d", ax=ax)
    ax.set_title("Average Salary by Department", fontsize=13, fontweight="bold")
    ax.set_xlabel("Department")
    ax.set_ylabel("Avg Salary (INR)")
    ax.tick_params(axis="x", rotation=30)
    for bar in ax.patches:
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 500,
                f"{int(bar.get_height()):,}",
                ha="center", va="bottom", fontsize=8)
    fig.tight_layout()
    save(fig, "02_avg_salary_dept.png")


# ── Chart 3 : Performance Score Distribution ─────────────────────────────────
def chart_performance_dist(df):
    print("Chart 3 : Performance score distribution ...")
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(df["performance_score"], bins=20, color="#4C72B0", edgecolor="white", alpha=0.85)
    ax.axvline(df["performance_score"].mean(), color="red", linestyle="--",
               linewidth=1.5, label=f"Mean: {df['performance_score'].mean():.1f}")
    ax.set_title("Performance Score Distribution", fontsize=13, fontweight="bold")
    ax.set_xlabel("Performance Score")
    ax.set_ylabel("Number of Employees")
    ax.legend()
    fig.tight_layout()
    save(fig, "03_performance_distribution.png")


# ── Chart 4 : Salary Box Plot by Department ──────────────────────────────────
def chart_salary_boxplot(df):
    print("Chart 4 : Salary box plot by department ...")
    fig, ax = plt.subplots(figsize=(11, 5))
    order = df.groupby("department")["salary_inr"].median().sort_values(ascending=False).index
    sns.boxplot(data=df, x="department", y="salary_inr", order=order,
                palette="Set2", ax=ax)
    ax.set_title("Salary Distribution by Department", fontsize=13, fontweight="bold")
    ax.set_xlabel("Department")
    ax.set_ylabel("Salary (INR)")
    ax.tick_params(axis="x", rotation=30)
    fig.tight_layout()
    save(fig, "04_salary_boxplot.png")


# ── Chart 5 : Experience vs Salary Scatter ───────────────────────────────────
def chart_exp_vs_salary(df):
    print("Chart 5 : Experience vs salary scatter ...")
    fig, ax = plt.subplots(figsize=(9, 5))
    scatter = ax.scatter(
        df["experience_years"], df["salary_inr"],
        c=df["performance_score"], cmap="RdYlGn",
        alpha=0.5, s=20, edgecolors="none"
    )
    cbar = fig.colorbar(scatter, ax=ax)
    cbar.set_label("Performance Score")
    ax.set_title("Experience vs Salary\n(colour = performance score)",
                 fontsize=13, fontweight="bold")
    ax.set_xlabel("Experience (Years)")
    ax.set_ylabel("Salary (INR)")
    fig.tight_layout()
    save(fig, "05_experience_vs_salary.png")


# ── Chart 6 : Employee Status Pie Chart ──────────────────────────────────────
def chart_status_pie(df):
    print("Chart 6 : Employee status pie chart ...")
    status_counts = df["status"].value_counts()
    colors = ["#2ecc71", "#f39c12", "#e74c3c", "#3498db"]
    fig, ax = plt.subplots(figsize=(7, 5))
    wedges, texts, autotexts = ax.pie(
        status_counts.values,
        labels=status_counts.index,
        autopct="%1.1f%%",
        colors=colors[:len(status_counts)],
        startangle=140,
        wedgeprops=dict(edgecolor="white", linewidth=1.5)
    )
    for t in autotexts:
        t.set_fontsize(10)
    ax.set_title("Employee Status Breakdown", fontsize=13, fontweight="bold")
    fig.tight_layout()
    save(fig, "06_status_pie.png")


# ── Chart 7 : Attendance vs Performance ──────────────────────────────────────
def chart_attendance_vs_performance(df):
    print("Chart 7 : Attendance vs performance ...")
    fig, ax = plt.subplots(figsize=(9, 5))
    colors = {"Active": "#2ecc71", "On Leave": "#f39c12",
              "Resigned": "#e74c3c", "Terminated": "#8e44ad"}
    for status, grp in df.groupby("status"):
        ax.scatter(grp["attendance_pct"], grp["performance_score"],
                   label=status, alpha=0.4, s=15,
                   color=colors.get(status, "grey"))
    ax.set_title("Attendance vs Performance by Status",
                 fontsize=13, fontweight="bold")
    ax.set_xlabel("Attendance (%)")
    ax.set_ylabel("Performance Score")
    ax.legend(title="Status", markerscale=2)
    fig.tight_layout()
    save(fig, "07_attendance_vs_performance.png")


# ── Chart 8 : Correlation Heatmap ────────────────────────────────────────────
def chart_correlation_heatmap(df):
    print("Chart 8 : Correlation heatmap ...")
    cols = ["age", "experience_years", "salary_inr",
            "performance_score", "attendance_pct"]
    corr = df[cols].corr()
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm",
                linewidths=0.5, ax=ax, vmin=-1, vmax=1)
    ax.set_title("Correlation Heatmap", fontsize=13, fontweight="bold")
    fig.tight_layout()
    save(fig, "08_correlation_heatmap.png")


# ── Chart 9 : Combined Dashboard ─────────────────────────────────────────────
def chart_dashboard(df):
    print("Chart 9 : Combined dashboard ...")
    fig = plt.figure(figsize=(18, 14))
    fig.suptitle("Employee Data Analysis Dashboard",
                 fontsize=16, fontweight="bold", y=0.98)

    # 1 — Dept headcount
    ax1 = fig.add_subplot(3, 3, 1)
    counts = df["department"].value_counts().sort_values()
    ax1.barh(counts.index, counts.values, color=sns.color_palette("muted", len(counts)))
    ax1.set_title("Dept Headcount")
    ax1.set_xlabel("Employees")

    # 2 — Avg salary
    ax2 = fig.add_subplot(3, 3, 2)
    avg_sal = df.groupby("department")["salary_inr"].mean().sort_values(ascending=False)
    ax2.bar(avg_sal.index, avg_sal.values, color=sns.color_palette("Blues_d", len(avg_sal)))
    ax2.set_title("Avg Salary by Dept")
    ax2.set_ylabel("INR")
    ax2.tick_params(axis="x", rotation=45)

    # 3 — Performance hist
    ax3 = fig.add_subplot(3, 3, 3)
    ax3.hist(df["performance_score"], bins=18, color="#4C72B0", edgecolor="white", alpha=0.85)
    ax3.axvline(df["performance_score"].mean(), color="red", linestyle="--", linewidth=1.2)
    ax3.set_title("Performance Distribution")
    ax3.set_xlabel("Score")

    # 4 — Status pie
    ax4 = fig.add_subplot(3, 3, 4)
    sc = df["status"].value_counts()
    ax4.pie(sc.values, labels=sc.index, autopct="%1.0f%%",
            colors=["#2ecc71", "#f39c12", "#e74c3c", "#3498db"],
            startangle=140,
            wedgeprops=dict(edgecolor="white"))
    ax4.set_title("Status Breakdown")

    # 5 — Exp vs salary
    ax5 = fig.add_subplot(3, 3, 5)
    ax5.scatter(df["experience_years"], df["salary_inr"],
                c=df["performance_score"], cmap="RdYlGn",
                alpha=0.4, s=10, edgecolors="none")
    ax5.set_title("Experience vs Salary")
    ax5.set_xlabel("Years")
    ax5.set_ylabel("INR")

    # 6 — Attendance vs performance
    ax6 = fig.add_subplot(3, 3, 6)
    colors_map = {"Active": "#2ecc71", "On Leave": "#f39c12",
                  "Resigned": "#e74c3c", "Terminated": "#8e44ad"}
    for status, grp in df.groupby("status"):
        ax6.scatter(grp["attendance_pct"], grp["performance_score"],
                    label=status, alpha=0.35, s=8,
                    color=colors_map.get(status, "grey"))
    ax6.set_title("Attendance vs Performance")
    ax6.set_xlabel("Attendance %")
    ax6.legend(fontsize=7, markerscale=2)

    # 7 — Correlation heatmap
    ax7 = fig.add_subplot(3, 3, 7)
    cols = ["age", "experience_years", "salary_inr", "performance_score", "attendance_pct"]
    corr = df[cols].corr()
    sns.heatmap(corr, annot=True, fmt=".1f", cmap="coolwarm",
                linewidths=0.5, ax=ax7, vmin=-1, vmax=1,
                annot_kws={"size": 7}, cbar=False)
    ax7.set_title("Correlation Heatmap")

    # 8 — Avg performance by dept
    ax8 = fig.add_subplot(3, 3, 8)
    avg_perf = df.groupby("department")["performance_score"].mean().sort_values(ascending=False)
    ax8.bar(avg_perf.index, avg_perf.values,
            color=sns.color_palette("Greens_d", len(avg_perf)))
    ax8.set_title("Avg Performance by Dept")
    ax8.tick_params(axis="x", rotation=45)
    ax8.set_ylabel("Score")

    # 9 — Salary bracket bar
    ax9 = fig.add_subplot(3, 3, 9)
    brackets = pd.cut(
        df["salary_inr"],
        bins=[0, 30000, 50000, 75000, 100000, 999999],
        labels=["<30K", "30-50K", "50-75K", "75K-1L", ">1L"]
    ).value_counts().sort_index()
    ax9.bar(brackets.index.astype(str), brackets.values,
            color=sns.color_palette("Oranges_d", len(brackets)))
    ax9.set_title("Salary Brackets")
    ax9.set_xlabel("Range (INR)")
    ax9.set_ylabel("Employees")

    fig.tight_layout(rect=[0, 0, 1, 0.97])
    save(fig, "09_dashboard.png")


# ── MAIN ──────────────────────────────────────────────────────────────────────
def main():
    print("=" * 50)
    print("  Employee EDA & Visualization")
    print("=" * 50)

    df = load_data()

    # Normalise column names to lowercase
    df.columns = [c.lower() for c in df.columns]

    chart_dept_headcount(df)
    chart_avg_salary(df)
    chart_performance_dist(df)
    chart_salary_boxplot(df)
    chart_exp_vs_salary(df)
    chart_status_pie(df)
    chart_attendance_vs_performance(df)
    chart_correlation_heatmap(df)
    chart_dashboard(df)

    print(f"\nAll charts saved in: {os.path.abspath(OUT_DIR)}/")
    print("Done!")


if __name__ == "__main__":
    main()
