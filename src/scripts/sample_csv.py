"""
Generate a small sample CSV for UI testing. [web:43]
"""
import pandas as pd
from datetime import date, timedelta
import random

roles = ["Data Analyst","Web Developer","Backend Engineer","ML Engineer","Data Scientist"]
locs = ["Bangalore","Hyderabad","Pune","Remote","Chennai","Mumbai"]
exps = ["Entry","Mid","Senior"]
skills_pool = ["python","sql","excel","tableau","power bi","javascript","react","node","pandas","numpy"]

def sample(n=100):
    today = date.today()
    rows = []
    for i in range(n):
        role = random.choice(roles)
        company = f"Company_{random.randint(1,20)}"
        loc = random.choice(locs)
        exp = random.choice(exps)
        sal_min = random.randint(4, 20) * 100000
        sal_max = sal_min + random.randint(1, 10) * 100000
        posted = today - timedelta(days=random.randint(0, 120))
        skills = ", ".join(random.sample(skills_pool, k=random.randint(2,4)))
        rows.append({
            "job_title": role,
            "company": company,
            "location": loc,
            "industry": "Technology",
            "experience_level": exp,
            "employment_type": "Full-time",
            "salary_min": sal_min,
            "salary_max": sal_max,
            "posted_date": posted.isoformat(),
            "skills": skills
        })
    return pd.DataFrame(rows)  # [web:43]

if __name__ == "__main__":
    df = sample(200)
    out = "data/processed/jobs_clean.csv"
    df.to_csv(out, index=False)
    print(f"Wrote {out} with {len(df)} rows")
