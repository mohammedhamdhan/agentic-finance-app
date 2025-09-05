import pandas as pd
from datetime import datetime

def screen_spx(pe_max: float = 20.0, roe_min: float = 0.15):
    # Day 1: return demo rows; A will replace with SQLite query
    rows = pd.DataFrame([
        {"ticker":"JPM","pe_ttm":12.1,"roe_ttm":0.17},
        {"ticker":"XOM","pe_ttm":13.4,"roe_ttm":0.19},
    ])
    meta = {
        "as_of": datetime.utcnow().date().isoformat(),
        "source": "demo (to be replaced by SQLite)",
        "csv": rows.to_csv(index=False)
    }
    return rows, meta
