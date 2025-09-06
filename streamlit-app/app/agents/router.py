from app.agents import compliance
from app.tools.screener import screen_spx
from app.tools.fund_summary import summarize_fund
from app.tools.backtest import run_backtest
from app.tools.risk_explain import explain_risk
import subprocess, shlex

from .graph import graph
from .state import AgentState

def route_query(user_msg: str, thread_id: str | None = None) -> dict:
    state: AgentState = {"input": user_msg, "artifacts": {}}
    config = None
    if thread_id:
        config = {"configurable": {"thread_id": thread_id}}
    out: AgentState = graph.invoke(state, config=config)  # <-- pass config
    if user_msg.strip().lower().startswith("ollama:"):
        cmd = f"ollama run llama3.1 '{user_msg[7:].strip()}'"
        out = subprocess.check_output(shlex.split(cmd)).decode().strip()
        return {"message": f"Ollama says: {out}", "artifacts": {}}
    return {"message": out.get("message",""), "artifacts": out.get("artifacts", {})}
