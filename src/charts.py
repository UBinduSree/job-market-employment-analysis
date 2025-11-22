import altair as alt
import pandas as pd

def skills_bar(df: pd.DataFrame):
    if "skills_vocab" not in df.columns or df.empty:
        return None
    exploded = df.explode("skills_vocab")
    if "skills_vocab" not in exploded.columns or exploded.empty:
        return None
    s = (exploded["skills_vocab"]
         .dropna()
         .astype(str)
         .str.strip()
         .replace("", pd.NA)
         .dropna()
         .value_counts()
         .reset_index())
    if s.empty:
        return None
    s.columns = ["skill", "postings"]  # ensure unique names
    s = s.head(10)
    return alt.Chart(s).mark_bar().encode(
        x=alt.X("postings:Q", title="Postings"),
        y=alt.Y("skill:N", sort="-x", title="Skill"),
        tooltip=["skill:N", "postings:Q"],
        color=alt.Color("skill:N", legend=None)
    )


    return chart  # [web:131]


def salary_hist(df: pd.DataFrame):
    if "salary_mid" not in df.columns or df["salary_mid"].dropna().empty:
        return None
    base = df[["salary_mid"]].dropna()
    chart = alt.Chart(base).mark_bar().encode(
        x=alt.X("salary_mid:Q", bin=alt.Bin(maxbins=30), title="Salary (mid)"),
        y=alt.Y("count():Q", title="Count"),
        tooltip=[alt.Tooltip("count():Q", title="Count")]
    )  # [web:66]
    return chart  # [web:43]

def trend_line(df: pd.DataFrame):
    if "posted_month" not in df.columns or df["posted_month"].dropna().empty:
        return None
    t = df.groupby("posted_month").size().reset_index(name="jobs")
    chart = alt.Chart(t).mark_line(point=True).encode(
        x=alt.X("posted_month:T", title="Month"),
        y=alt.Y("jobs:Q", title="Postings"),
        tooltip=["posted_month:T", "jobs:Q"]
    )  # [web:66]
    return chart  # [web:43]

def salary_by_location(df: pd.DataFrame):
    if "salary_mid" not in df.columns or "location" not in df.columns:
        return None
    g = (
        df.dropna(subset=["location"])
          .groupby("location", as_index=False)["salary_mid"]
          .median()
          .sort_values("salary_mid", ascending=False)
          .head(8)
    )
    if g.empty:
        return None
    chart = alt.Chart(g).mark_bar().encode(
        x=alt.X("salary_mid:Q", title="Median Salary"),
        y=alt.Y("location:N", sort="-x", title="Location"),
        tooltip=["location:N", alt.Tooltip("salary_mid:Q", title="Median Salary")]
    )  # [web:69]
    return chart  # [web:43]
alt.themes.register('warm', lambda: {'config': {'range': {'category': {'scheme':'set2'}}}})
alt.themes.enable('warm')
