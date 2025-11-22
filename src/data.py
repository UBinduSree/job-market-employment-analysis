# import pandas as pd
# from functools import lru_cache
# import csv

# @lru_cache(maxsize=1)
# def load_csv(path: str) -> pd.DataFrame:
#     # Be lenient with quotes to avoid EOF inside string errors
#     try:
#         df = pd.read_csv(path)
#     except pd.errors.ParserError:
#         # Ignore all quotes and fall back to Python engine
#         df = pd.read_csv(path, engine="python", quoting=csv.QUOTE_NONE, escapechar="\\")
#     df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

#     def _to_vocab(val):
#         if isinstance(val, list):
#             return [x.strip().lower() for x in val if isinstance(x, str) and x.strip()]
#         s = str(val) if val is not None else ""
#         s = s.strip().strip('"').strip("'")          # remove outer quotes
#         s = s.replace("[", "").replace("]", "")      # remove brackets if list-like string
#         parts = [p.strip().strip("'").strip('"').lower() for p in s.split(",")]
#         return [p for p in parts if p]

#     if "skills" not in df.columns:
#         df["skills"] = ""
#     df["skills_vocab"] = df["skills"].apply(_to_vocab)

#     # Derive role from job_title if not present
#     if "role" not in df.columns and "job_title" in df.columns:
#         df["role"] = df["job_title"].astype(str).str.title()

#     # Salary mid calculation
#     if {"salary_min", "salary_max"}.issubset(df.columns):
#         df["salary_mid"] = (df["salary_min"].astype(float).fillna(0) + df["salary_max"].astype(float).fillna(0)) / 2  # [web:43]

#     # Posted month for trend
#     if "posted_date" in df.columns:
#         dt = pd.to_datetime(df["posted_date"], errors="coerce")
#         df["posted_month"] = dt.dt.to_period("M").dt.to_timestamp()  # [web:43]

#     # Skills list normalization
#     if "skills" in df.columns:
#         df["skills_vocab"] = (
#             df["skills"].fillna("")
#               .astype(str)
#               .str.split(",")
#               .apply(lambda xs: [x.strip().lower() for x in xs if x and x.strip()])
#         )  # [web:45]
#     else:
#         df["skills_vocab"] = [[] for _ in range(len(df))]

#     # Ensure essential columns exist
#     for col in ["company", "location", "experience_level", "industry"]:
#         if col not in df.columns:
#             df[col] = None

#     return df  # [web:43]
import pandas as pd
from functools import lru_cache
import csv

@lru_cache(maxsize=1)
def load_csv(path: str) -> pd.DataFrame:
    # Be lenient with quotes to avoid EOF inside string errors
    try:
        df = pd.read_csv(path)
    except pd.errors.ParserError:
        df = pd.read_csv(path, engine="python", quoting=csv.QUOTE_NONE, escapechar="\\")
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    # Always (re)build skills_vocab from skills text
    def _to_vocab(val):
        if isinstance(val, list):
            return [x.strip().lower() for x in val if isinstance(x, str) and x.strip()]
        s = str(val) if val is not None else ""
        s = s.strip().strip('"').strip("'")          # remove outer quotes
        s = s.replace("[", "").replace("]", "")      # remove brackets if list-like string
        parts = [p.strip().strip("'").strip('"').lower() for p in s.split(",")]
        return [p for p in parts if p]

    if "skills" not in df.columns:
        df["skills"] = ""
    df["skills_vocab"] = df["skills"].apply(_to_vocab)

    # Derive role from job_title if not present
    if "role" not in df.columns and "job_title" in df.columns:
        df["role"] = df["job_title"].astype(str).str.title()

    # Salary mid calculation
    if {"salary_min", "salary_max"}.issubset(df.columns):
        df["salary_mid"] = (pd.to_numeric(df["salary_min"], errors="coerce").fillna(0)
                            + pd.to_numeric(df["salary_max"], errors="coerce").fillna(0)) / 2

    # Posted month for trend
    if "posted_date" in df.columns:
        dt = pd.to_datetime(df["posted_date"], errors="coerce")
        df["posted_month"] = dt.dt.to_period("M").dt.to_timestamp()

    # Ensure essential columns exist
    for col in ["company", "location", "experience_level", "industry"]:
        if col not in df.columns:
            df[col] = None

    return df
