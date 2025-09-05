from langchain.tools import tool
from app.tools.screener import screen_spx
from app.tools.fund_summary import summarize_fund
from app.tools.backtest import run_backtest
from app.tools.risk_explain import explain_risk

@tool("screen_spx")
def screen_spx_tool(pe_max: float = 20.0, roe_min: float = 0.15):
    "Screen S&P 500 by PE and ROE using our DB (educational; delayed)."
    rows, meta = screen_spx(pe_max=pe_max, roe_min=roe_min)
    return {"rows": rows.to_dict(orient="records"), "meta": meta}

@tool("summarize_fund")
def summarize_fund_tool(ticker: str):
    "Summarize an ETF/fund from our local doc store (RAG)."
    return summarize_fund(ticker)

@tool("run_backtest")
def run_backtest_tool(asset: str = "SPY", strategy: str = "SMA_50_200", span_years: int = 5):
    "Run a simple educational backtest."
    return run_backtest(asset, strategy, span_years)

@tool("explain_risk")
def explain_risk_tool(topic: str = "diversification"):
    "Explain a risk concept from curated notes."
    return {"text": explain_risk(topic)}
