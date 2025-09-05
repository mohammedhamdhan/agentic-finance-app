def classify_route(text: str) -> str:
    t = (text or "").lower()
    if "screen" in t or "pe" in t or "roe" in t: return "screen"
    if "etf" in t or "fund" in t or "summary" in t: return "fund"
    if "backtest" in t or "sma" in t or "rsi" in t: return "backtest"
    if "risk" in t: return "risk"
    return "other"
