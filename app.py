import streamlit as st
import pandas as pd
from src.data import load_csv
from src.filters import apply_filters
from src.metrics import kpi_summary
from src.charts import skills_bar, salary_hist, trend_line, salary_by_location

st.set_page_config(page_title="Job Market & Employment Analysis", layout="wide")  # [web:43]
st.markdown("""
<style>
.kpi-card {background: #ffffff; border: 1px solid #ffe3cc; border-radius: 14px; padding: 14px 16px; box-shadow: 0 4px 18px rgba(255,107,0,0.08);}
.kpi-title {color:#6b7280; font-size:0.85rem; margin-bottom:6px;}
.kpi-value {color:#111827; font-size:1.6rem; font-weight:700;}
</style>
""", unsafe_allow_html=True)

st.title("Job Market & Employment Analysis")  # [web:43]

# Load
df = load_csv("data/processed/jobs_clean.csv")  # [web:43]

# Sidebar filters
with st.sidebar:
    st.header("Filters")  # [web:45]
    roles = ["All"] + sorted(df["role"].dropna().unique().tolist()) if "role" in df.columns else ["All"]
    role = st.selectbox("Role", roles)  # [web:45]

    locs = ["All"] + sorted(df["location"].dropna().unique().tolist()) if "location" in df.columns else ["All"]
    loc = st.selectbox("Location", locs)  # [web:45]

    exps = ["All"] + sorted(df["experience_level"].dropna().unique().tolist()) if "experience_level" in df.columns else ["All"]
    exp = st.selectbox("Experience", exps)  # [web:45]

# app.py (inside sidebar)
skills_vocab = []
if "skills_vocab" in df.columns:
    exploded = df.explode("skills_vocab")
    if "skills_vocab" in exploded.columns:
        freq = (exploded["skills_vocab"]
                .dropna()
                .astype(str)
                .str.strip()
                .replace("", pd.NA)
                .dropna()
                .value_counts()
                .head(30)
                .index
                .tolist())
        skills_vocab = sorted(freq)
skills_any = st.multiselect("Skills (any)", skills_vocab)


# Apply filters
fdf = apply_filters(df, role, loc, exp, skills_any)  # [web:45]

# KPIs
total_jobs, uniq_comp, median_salary, top_loc = kpi_summary(fdf)  # [web:45]
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"<div class='kpi-card'><div class='kpi-title'>Total jobs</div><div class='kpi-value'>{total_jobs:,}</div></div>", unsafe_allow_html=True)
with c2:
    st.markdown(f"<div class='kpi-card'><div class='kpi-title'>Companies</div><div class='kpi-value'>{uniq_comp:,}</div></div>", unsafe_allow_html=True)
with c3:
    val = f"{int(median_salary):,}" if median_salary else "—"
    st.markdown(f"<div class='kpi-card'><div class='kpi-title'>Median salary</div><div class='kpi-value'>{val}</div></div>", unsafe_allow_html=True)
with c4:
    st.markdown(f"<div class='kpi-card'><div class='kpi-title'>Top location</div><div class='kpi-value'>{top_loc or '—'}</div></div>", unsafe_allow_html=True)

st.divider()  # [web:43]

# Charts
ch1 = skills_bar(fdf)  # [web:43]
if ch1 is not None:
    st.subheader("Top Skills")  # [web:43]
    st.altair_chart(ch1, use_container_width=True)  # [web:64]

c1, c2 = st.columns(2)  # [web:45]
with c1:
    st.subheader("Salary Distribution")  # [web:43]
    ch2 = salary_hist(fdf)  # [web:43]
    if ch2 is not None:
        st.altair_chart(ch2, use_container_width=True)  # [web:64]
with c2:
    st.subheader("Jobs Over Time")  # [web:43]
    ch3 = trend_line(fdf)  # [web:43]
    if ch3 is not None:
        st.altair_chart(ch3, use_container_width=True)  # [web:64]

st.subheader("Median Salary by Location")  # [web:43]
ch4 = salary_by_location(fdf)  # [web:43]
if ch4 is not None:
    st.altair_chart(ch4, use_container_width=True)  # [web:64]

st.divider()  # [web:43]
st.subheader("Filtered rows")  # [web:45]
st.dataframe(fdf, use_container_width=True)  # [web:45]
st.download_button("Download filtered CSV", fdf.to_csv(index=False), "jobs_filtered.csv", "text/csv")  # [web:48]
