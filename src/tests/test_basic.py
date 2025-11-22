import pandas as pd
from src.metrics import kpi_summary

def test_kpis_smoke():
    df = pd.DataFrame({
        "company": ["A","B","A"],
        "location": ["X","X","Y"],
        "salary_mid": [100, 200, 300]
    })
    t, u, m, top = kpi_summary(df)
    assert t == 3 and u == 2
    assert m == 200
    assert top in {"X","Y"}
