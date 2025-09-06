from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from typing import List, Dict, Any
import re

from .state import AgentState
from .compliance import compliance_check
from .router_llm import classify_route_llm  # new LLM-based
from .tools import screen_spx_tool, summarize_fund_tool, run_backtest_tool, explain_risk_tool

# --- Nodes ---
def node_compliance(state: AgentState) -> AgentState:
    blocked, msg = compliance_check(state["input"])
    state["blocked"] = blocked
    if blocked:
        state["message"] = msg
    return state

def node_plan(state: AgentState) -> AgentState:
    """Very light planner: split by 'then' / commas; detect tool keywords."""
    if state.get("blocked"):
        return state
    text = (state["input"] or "").lower()
    # crude step split
    parts = re.split(r"\bthen\b|,| and then ", text)
    plan: List[str] = [p.strip() for p in parts if p.strip()]
    state["history"] = state.get("history", [])
    state["history"].append({"plan": plan})
    state["artifacts"] = {}
    return state

def node_route(state: AgentState) -> AgentState:
    if state.get("blocked"):
        return state
    route, debug = classify_route_llm(state["input"])
    state["intent"] = route
    state.setdefault("artifacts", {})["router_debug"] = debug
    return state

def node_screen(state: AgentState) -> AgentState:
    res = screen_spx_tool.invoke({})  # Person A’s tool will accept params later
    state.setdefault("artifacts", {})["screen"] = res
    state["message"] = f"Screened S&P500 (defaults). {len(res['rows'])} matches."
    return state

def node_fund(state: AgentState) -> AgentState:
    m = re.search(r"\b[A-Z]{2,5}\b", state["input"])
    ticker = (m.group(0) if m else "VOO")
    res = summarize_fund_tool.invoke({"ticker": ticker})
    state.setdefault("artifacts", {})["fund"] = res
    state["message"] = f"ETF summary for {ticker}."
    return state

def node_backtest(state: AgentState) -> AgentState:
    res = run_backtest_tool.invoke({})
    state.setdefault("artifacts", {})["backtest"] = res
    state["message"] = "Backtest complete."
    return state

def node_risk(state: AgentState) -> AgentState:
    res = explain_risk_tool.invoke({})
    state.setdefault("artifacts", {})["risk"] = res
    state["message"] = "Risk explainer."
    return state

def node_other(state: AgentState) -> AgentState:
    """Fallback when we can't classify the user's intent."""
    txt = state.get("input", "")
    # Optional: try a brief Ollama answer, but stay educational & non-advisory
    try:
        import subprocess, shlex
        prompt = (
            "You are an educational finance assistant. "
            "Answer concisely (2–3 sentences), no personal advice. "
            f"Question: {txt!r}"
        )
        out = subprocess.check_output(
            shlex.split(f"ollama run llama3.1 '{prompt}'"),
            timeout=8
        ).decode().strip()
        state["message"] = out
    except Exception:
        state["message"] = (
            "I can screen S&P 500 by PE/ROE, summarize ETF fact sheets, run simple backtests, "
            "and explain risks. Try: 'screen spx pe<18 roe>12' or 'summarize ETF VOO'."
        )
    return state


# --- Graph build ---
builder = StateGraph(AgentState)
builder.add_node("compliance", node_compliance)
builder.add_node("plan", node_plan)
builder.add_node("route", node_route)
builder.add_node("screen", node_screen)
builder.add_node("fund", node_fund)
builder.add_node("backtest", node_backtest)
builder.add_node("risk", node_risk)
builder.add_node("other", node_other)

builder.set_entry_point("compliance")
builder.add_edge("compliance", "plan")
builder.add_edge("plan", "route")

def branch(state: AgentState):
    if state.get("blocked"): return END
    return state.get("intent", "other")

builder.add_conditional_edges(
    "route",
    branch,
    {
        "screen": "screen",
        "fund": "fund",
        "backtest": "backtest",
        "risk": "risk",
        "other": "other",
    },
)

for n in ("screen","fund","backtest","risk","other"):
    builder.add_edge(n, END)

# Memory per session
memory = MemorySaver()
graph = builder.compile(checkpointer=memory)
