from app.agents import compliance
from app.tools.screener import screen_spx
from app.tools.fund_summary import summarize_fund
from app.tools.backtest import run_backtest
from app.tools.risk_explain import explain_risk

def route_query(user_msg: str) -> dict:
    guard = compliance.check(user_msg)
    if guard.get("blocked"):
        return {"message": guard["message"]}

    text = (user_msg or "").lower()
    # naive routing for Day 1; A/B will enhance later
    if "screen" in text or "pe" in text or "roe" in text:
        rows, meta = screen_spx()
        return {"message": f"Ran S&P500 screen (default pe<20, roe>0.15): {len(rows)} hits.", "artifacts": {"meta": meta, "rows": rows}}
    if "etf" in text or "fund" in text or "summary" in text:
        return {"message": "Summarized sample ETF (VOO).", "artifacts": summarize_fund("VOO")}
    if "backtest" in text or "sma" in text or "rsi" in text:
        return {"message": "Ran demo backtest on SPY (SMA_50_200).", "artifacts": run_backtest("SPY", "SMA_50_200", 5)}
    if "risk" in text:
        return {"message": "Risk explainer", "artifacts": {"text": explain_risk("diversification")}}
    return {"message": "I can screen (PE/ROE), summarize funds, run simple backtests, or explain risks. Try: 'screen spx pe<18 roe>12'."}
