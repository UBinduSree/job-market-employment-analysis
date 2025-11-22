# Job Market & Employment Analysis (Streamlit)

A simple Streamlit dashboard that analyzes a small job market CSV with filters, KPIs, and charts. [web:43]

## Quick start
1) Python 3.9+ and virtualenv recommended. [web:53]
2) pip install -r requirements.txt. [web:53]
3) Put your CSV at data/processed/jobs_clean.csv. Use scripts/clean_csv.py if needed. [web:43]
4) Run: streamlit run app.py. [web:53]

## Dataset columns
Expected columns (case-insensitive):
- job_title, company, location, industry, experience_level, employment_type, salary_min, salary_max, posted_date, skills (comma-separated) [web:43]

## Features
- Filters: role, location, experience, skills-any. [web:45]
- KPIs: total jobs, companies, median salary, top location. [web:45]
- Charts: top skills, salary distribution, jobs trend, salary by location. [web:43]
- Download filtered CSV. [web:48]
