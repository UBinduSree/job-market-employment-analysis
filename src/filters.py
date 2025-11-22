import pandas as pd

def apply_filters(df: pd.DataFrame, role: str, loc: str, exp: str, skills_any: list) -> pd.DataFrame:
    f = df.copy()
    if role != "All" and "role" in f.columns:
        f = f[f["role"] == role]
    if loc != "All" and "location" in f.columns:
        f = f[f["location"] == loc]
    if exp != "All" and "experience_level" in f.columns:
        f = f[f["experience_level"] == exp]
    if skills_any:
        f = f[f["skills_vocab"].apply(lambda lst: any(s in lst for s in skills_any))]
    return f  # [web:45]
