import pandas as pd

def kpi_summary(df: pd.DataFrame):
    total = len(df)
    uniq = df["company"].nunique() if "company" in df.columns else 0
    median_salary = float(df["salary_mid"].median()) if "salary_mid" in df.columns and not df["salary_mid"].dropna().empty else 0.0
    top_loc = df["location"].mode().iat[0] if "location" in df.columns and not df["location"].dropna().empty else None
    return total, uniq, median_salary, top_loc  # [web:45]
