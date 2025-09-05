from app.agents import compliance
from app.tools.screener import screen_spx
from app.tools.fund_summary import summarize_fund
from app.tools.backtest import run_backtest
from app.tools.risk_explain import explain_risk

from .graph import graph
from .state import AgentState

def route_query(user_msg: str) -> dict:
    state: AgentState = {"input": user_msg, "artifacts": {}}
    out: AgentState = graph.invoke(state)
    # normalize for Streamlit
    return {"message": out.get("message",""), "artifacts": out.get("artifacts", {})}


