"""
Usage:
  python scripts/clean_csv.py data/raw/jobs_raw.csv data/processed/jobs_clean.csv
Cleans and normalizes a raw jobs CSV into expected schema. [web:43]
"""
import sys
import pandas as pd

def clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    # Standard columns
    for col in ["job_title","company","location","industry","experience_level","employment_type","posted_date","skills"]:
        if col not in df.columns:
            df[col] = None
    # Salary normalization
    if "salary" in df.columns and "salary_min" not in df.columns and "salary_max" not in df.columns:
        # If a single salary column exists, copy to mid and set min/max same
        df["salary_min"] = pd.to_numeric(df["salary"], errors="coerce")
        df["salary_max"] = pd.to_numeric(df["salary"], errors="coerce")
    else:
        for c in ["salary_min","salary_max"]:
            if c in df.columns:
                df[c] = pd.to_numeric(df[c], errors="coerce")
            else:
                df[c] = None
    # Role
    if "role" not in df.columns:
        df["role"] = df["job_title"].astype(str).str.title()
    # Dates
    if "posted_date" in df.columns:
        df["posted_date"] = pd.to_datetime(df["posted_date"], errors="coerce").dt.date.astype(str)
    # Skills as comma string if a list-like given
    if "skills" in df.columns:
        df["skills"] = df["skills"].apply(lambda v: ", ".join(v) if isinstance(v, (list, tuple)) else v)
    # Deduplicate rows heuristically
    subset_cols = [c for c in ["job_title","company","location","posted_date"] if c in df.columns]
    if subset_cols:
        df = df.drop_duplicates(subset=subset_cols)
    return df  # [web:43]

def main():
    if len(sys.argv) != 3:
        print("Usage: python scripts/clean_csv.py <input_raw.csv> <output_clean.csv>")
        sys.exit(1)
    inp, out = sys.argv[1], sys.argv[2]
    df = pd.read_csv(inp)
    df = clean(df)
    df.to_csv(out, index=False)
    print(f"Wrote {out} with {len(df)} rows")

if __name__ == "__main__":
    main()
