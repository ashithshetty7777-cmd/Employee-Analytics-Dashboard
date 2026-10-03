-- ============================================================
--  EMPLOYEE DATA ANALYSIS
--  Database : employee_db
--  Table    : employees
--  Every query has USE employee_db so you can run any of
--  them independently in MySQL Workbench.
-- ============================================================

-- ============================================================
-- SECTION 1 : OVERVIEW
-- ============================================================

-- 1.1 Total employee count
USE employee_db;
SELECT COUNT(*) AS total_employees
FROM employees;

-- 1.2 Gender split
USE employee_db;
SELECT gender,
       COUNT(*) AS count,
       ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM employees), 1) AS percentage
FROM employees
GROUP BY gender;

-- 1.3 Status breakdown
USE employee_db;
SELECT status,
       COUNT(*) AS count,
       ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM employees), 1) AS percentage
FROM employees
GROUP BY status
ORDER BY count DESC;

-- 1.4 City-wise headcount
USE employee_db;
SELECT city,
       COUNT(*) AS total_employees
FROM employees
GROUP BY city
ORDER BY total_employees DESC;


-- ============================================================
-- SECTION 2 : DEPARTMENT ANALYSIS
-- ============================================================

-- 2.1 Headcount per department
USE employee_db;
SELECT department,
       COUNT(*) AS total_employees
FROM employees
GROUP BY department
ORDER BY total_employees DESC;

-- 2.2 Average salary per department
USE employee_db;
SELECT department,
       ROUND(AVG(salary_inr), 0) AS avg_salary,
       MIN(salary_inr)           AS min_salary,
       MAX(salary_inr)           AS max_salary
FROM employees
GROUP BY department
ORDER BY avg_salary DESC;

-- 2.3 Average performance score per department
USE employee_db;
SELECT department,
       ROUND(AVG(performance_score), 1) AS avg_performance,
       ROUND(MIN(performance_score), 1) AS min_performance,
       ROUND(MAX(performance_score), 1) AS max_performance
FROM employees
GROUP BY department
ORDER BY avg_performance DESC;

-- 2.4 Average attendance per department
USE employee_db;
SELECT department,
       ROUND(AVG(attendance_pct), 1) AS avg_attendance
FROM employees
GROUP BY department
ORDER BY avg_attendance DESC;

-- 2.5 Full department summary in one query
USE employee_db;
SELECT department,
       COUNT(*)                         AS headcount,
       ROUND(AVG(salary_inr), 0)        AS avg_salary,
       ROUND(AVG(performance_score), 1) AS avg_performance,
       ROUND(AVG(attendance_pct), 1)    AS avg_attendance,
       ROUND(AVG(experience_years), 1)  AS avg_experience
FROM employees
GROUP BY department
ORDER BY headcount DESC;


-- ============================================================
-- SECTION 3 : SALARY ANALYSIS
-- ============================================================

-- 3.1 Top 10 highest paid employees
USE employee_db;
SELECT name, department, role, experience_years, salary_inr
FROM employees
ORDER BY salary_inr DESC
LIMIT 10;

-- 3.2 Bottom 10 lowest paid employees
USE employee_db;
SELECT name, department, role, experience_years, salary_inr
FROM employees
ORDER BY salary_inr ASC
LIMIT 10;

-- 3.3 Salary brackets
USE employee_db;
SELECT
    CASE
        WHEN salary_inr < 30000  THEN 'Below 30K'
        WHEN salary_inr < 50000  THEN '30K - 50K'
        WHEN salary_inr < 75000  THEN '50K - 75K'
        WHEN salary_inr < 100000 THEN '75K - 1L'
        ELSE 'Above 1L'
    END AS salary_bracket,
    COUNT(*) AS employee_count
FROM employees
GROUP BY salary_bracket
ORDER BY MIN(salary_inr);

-- 3.4 Salary vs experience (avg salary per experience band)
USE employee_db;
SELECT
    CASE
        WHEN experience_years BETWEEN 0  AND 2  THEN '0-2 yrs'
        WHEN experience_years BETWEEN 3  AND 5  THEN '3-5 yrs'
        WHEN experience_years BETWEEN 6  AND 10 THEN '6-10 yrs'
        WHEN experience_years BETWEEN 11 AND 20 THEN '11-20 yrs'
        ELSE '20+ yrs'
    END AS experience_band,
    COUNT(*)                  AS employees,
    ROUND(AVG(salary_inr), 0) AS avg_salary
FROM employees
GROUP BY experience_band
ORDER BY MIN(experience_years);


-- ============================================================
-- SECTION 4 : PERFORMANCE ANALYSIS
-- ============================================================

-- 4.1 Performance categories
USE employee_db;
SELECT
    CASE
        WHEN performance_score >= 90 THEN 'Excellent (90-100)'
        WHEN performance_score >= 75 THEN 'Good (75-89)'
        WHEN performance_score >= 60 THEN 'Average (60-74)'
        ELSE 'Poor (Below 60)'
    END AS performance_category,
    COUNT(*) AS employee_count
FROM employees
GROUP BY performance_category
ORDER BY MIN(performance_score) DESC;

-- 4.2 Top 10 performers
USE employee_db;
SELECT name, department, role, performance_score, salary_inr
FROM employees
ORDER BY performance_score DESC
LIMIT 10;

-- 4.3 Bottom 10 performers
USE employee_db;
SELECT name, department, role, performance_score, attendance_pct
FROM employees
ORDER BY performance_score ASC
LIMIT 10;

-- 4.4 High performers who are underpaid
--     (performance > 85 but salary below department average)
USE employee_db;
SELECT e.name, e.department, e.role,
       e.performance_score,
       e.salary_inr,
       ROUND(dept_avg.avg_sal, 0) AS dept_avg_salary
FROM employees e
JOIN (
    SELECT department, AVG(salary_inr) AS avg_sal
    FROM employees
    GROUP BY department
) dept_avg ON e.department = dept_avg.department
WHERE e.performance_score > 85
  AND e.salary_inr < dept_avg.avg_sal
ORDER BY e.performance_score DESC;


-- ============================================================
-- SECTION 5 : ATTENDANCE ANALYSIS
-- ============================================================

-- 5.1 Attendance categories
USE employee_db;
SELECT
    CASE
        WHEN attendance_pct >= 95 THEN 'Excellent (95-100%)'
        WHEN attendance_pct >= 85 THEN 'Good (85-94%)'
        WHEN attendance_pct >= 75 THEN 'Average (75-84%)'
        ELSE 'At Risk (Below 75%)'
    END AS attendance_category,
    COUNT(*) AS employee_count
FROM employees
GROUP BY attendance_category
ORDER BY MIN(attendance_pct) DESC;

-- 5.2 Employees at attendance risk (below 75%)
USE employee_db;
SELECT name, department, role, attendance_pct, status
FROM employees
WHERE attendance_pct < 75
ORDER BY attendance_pct ASC;

-- 5.3 Departments with most attendance issues
USE employee_db;
SELECT department,
       COUNT(*) AS at_risk_employees
FROM employees
WHERE attendance_pct < 75
GROUP BY department
ORDER BY at_risk_employees DESC;


-- ============================================================
-- SECTION 6 : ATTRITION ANALYSIS
-- ============================================================

-- 6.1 Overall attrition rate
USE employee_db;
SELECT
    SUM(CASE WHEN status IN ('Resigned', 'Terminated') THEN 1 ELSE 0 END) AS attrition_count,
    COUNT(*) AS total,
    ROUND(SUM(CASE WHEN status IN ('Resigned', 'Terminated') THEN 1 ELSE 0 END)
          * 100.0 / COUNT(*), 1) AS attrition_rate_pct
FROM employees;

-- 6.2 Attrition by department
USE employee_db;
SELECT department,
       COUNT(*) AS total,
       SUM(CASE WHEN status IN ('Resigned', 'Terminated') THEN 1 ELSE 0 END) AS attrition,
       ROUND(SUM(CASE WHEN status IN ('Resigned', 'Terminated') THEN 1 ELSE 0 END)
             * 100.0 / COUNT(*), 1) AS attrition_rate_pct
FROM employees
GROUP BY department
ORDER BY attrition_rate_pct DESC;

-- 6.3 Attrition by experience band
USE employee_db;
SELECT
    CASE
        WHEN experience_years BETWEEN 0 AND 2  THEN '0-2 yrs'
        WHEN experience_years BETWEEN 3 AND 5  THEN '3-5 yrs'
        WHEN experience_years BETWEEN 6 AND 10 THEN '6-10 yrs'
        ELSE '10+ yrs'
    END AS experience_band,
    COUNT(*) AS total,
    SUM(CASE WHEN status IN ('Resigned', 'Terminated') THEN 1 ELSE 0 END) AS attrition,
    ROUND(SUM(CASE WHEN status IN ('Resigned', 'Terminated') THEN 1 ELSE 0 END)
          * 100.0 / COUNT(*), 1) AS attrition_rate_pct
FROM employees
GROUP BY experience_band
ORDER BY MIN(experience_years);

-- 6.4 Left vs stayed — performance, salary, attendance comparison
USE employee_db;
SELECT
    CASE WHEN status IN ('Resigned', 'Terminated') THEN 'Left' ELSE 'Stayed' END AS employee_group,
    COUNT(*)                         AS count,
    ROUND(AVG(performance_score), 1) AS avg_performance,
    ROUND(AVG(salary_inr), 0)        AS avg_salary,
    ROUND(AVG(attendance_pct), 1)    AS avg_attendance
FROM employees
GROUP BY employee_group;


-- ============================================================
-- SECTION 7 : ROLE & EXPERIENCE ANALYSIS
-- ============================================================

-- 7.1 Most common roles
USE employee_db;
SELECT role, COUNT(*) AS count
FROM employees
GROUP BY role
ORDER BY count DESC
LIMIT 10;

-- 7.2 Average experience per department
USE employee_db;
SELECT department,
       ROUND(AVG(experience_years), 1) AS avg_experience,
       MIN(experience_years)           AS min_experience,
       MAX(experience_years)           AS max_experience
FROM employees
GROUP BY department
ORDER BY avg_experience DESC;

-- 7.3 Employees eligible for promotion
--     (Active, experience >= 5 yrs, performance >= 80)
USE employee_db;
SELECT name, department, role,
       experience_years, performance_score, salary_inr
FROM employees
WHERE status = 'Active'
  AND experience_years >= 5
  AND performance_score >= 80
ORDER BY performance_score DESC, experience_years DESC;


-- ============================================================
-- SECTION 8 : ADVANCED (Window Functions)
-- ============================================================

-- 8.1 Rank employees by salary within each department
USE employee_db;
SELECT name, department, salary_inr,
       RANK() OVER (PARTITION BY department ORDER BY salary_inr DESC) AS salary_rank
FROM employees
ORDER BY department, salary_rank;

-- 8.2 Each employee salary vs their department average
USE employee_db;
SELECT name, department, salary_inr,
       ROUND(AVG(salary_inr) OVER (PARTITION BY department), 0) AS dept_avg_salary,
       salary_inr - ROUND(AVG(salary_inr) OVER (PARTITION BY department), 0) AS diff_from_avg
FROM employees
ORDER BY department, diff_from_avg DESC;

-- 8.3 Running total of hires by joining year
USE employee_db;
SELECT joining_year,
       COUNT(*) AS hired,
       SUM(COUNT(*)) OVER (ORDER BY joining_year) AS cumulative_total
FROM employees
GROUP BY joining_year
ORDER BY joining_year;
