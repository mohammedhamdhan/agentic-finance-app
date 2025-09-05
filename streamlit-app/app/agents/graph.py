from langgraph.graph import StateGraph, END
from .state import AgentState
from .compliance import compliance_check
from .router_llm import classify_route
from .tools import screen_spx_tool, summarize_fund_tool, run_backtest_tool, explain_risk_tool

def node_compliance(state: AgentState) -> AgentState:
    blocked, msg = compliance_check(state["input"])
    state["blocked"] = blocked
    if blocked:
        state["message"] = msg
    return state

def node_route(state: AgentState) -> AgentState:
    if state.get("blocked"):
        return state
    route = classify_route(state["input"])
    state["intent"] = route  # "screen" | "fund" | "backtest" | "risk" | "other"
    return state

def node_screen(state: AgentState) -> AgentState:
    res = screen_spx_tool.invoke({})
    state["artifacts"] = {"screen": res}
    state["message"] = f"Found {len(res['rows'])} matches. See table below."
    return state

def node_fund(state: AgentState) -> AgentState:
    # default to VOO if none provided
    import re
    m = re.search(r"\b[A-Z]{2,5}\b", state["input"])
    ticker = (m.group(0) if m else "VOO")
    res = summarize_fund_tool.invoke({"ticker": ticker})
    state["artifacts"] = {"fund": res}
    state["message"] = f"ETF summary for {ticker}."
    return state

def node_backtest(state: AgentState) -> AgentState:
    res = run_backtest_tool.invoke({})
    state["artifacts"] = {"backtest": res}
    state["message"] = "Backtest complete."
    return state

def node_risk(state: AgentState) -> AgentState:
    res = explain_risk_tool.invoke({})
    state["artifacts"] = {"risk": res}
    state["message"] = "Risk explainer."
    return state

# Build graph
_builder = StateGraph(AgentState)
_builder.add_node("compliance", node_compliance)
_builder.add_node("route", node_route)
_builder.add_node("screen", node_screen)
_builder.add_node("fund", node_fund)
_builder.add_node("backtest", node_backtest)
_builder.add_node("risk", node_risk)

_builder.set_entry_point("compliance")
_builder.add_edge("compliance", "route")

def _branch(state: AgentState):
    if state.get("blocked"): return END
    return state.get("intent", "other")

_builder.add_conditional_edges(
    "route",
    _branch,
    {
        "screen": "screen",
        "fund": "fund",
        "backtest": "backtest",
        "risk": "risk",
        "other": END,
    },
)

_builder.add_edge("screen", END)
_builder.add_edge("fund", END)
_builder.add_edge("backtest", END)
_builder.add_edge("risk", END)

graph = _builder.compile()
