import subprocess, shlex, re

CLASS_LABELS = {"screen","fund","backtest","risk","other"}

FEW_SHOT = """You classify a user request for an educational finance tool.
Valid classes: screen, fund, backtest, risk, other.

Classify as:
- screen  → only if user asks to screen/filter a UNIVERSE with metrics (keywords: screen, filter, pe, p/e, roe, <, >).
- fund    → ETF/fund summary (e.g., 'summarize ETF VOO', 'fund factsheet').
- backtest→ performance test (e.g., 'backtest SPY 50/200 SMA', 'RSI backtest').
- risk    → finance risk concept explanations.
- other   → single company/ticker questions (e.g., 'NVIDIA', 'NVDA', 'about Apple'), definitions ('What is SPX?'), chit-chat.

Examples:
Q: NVIDIA → other
Q: NVDA → other
Q: Tell me about Apple → other
Q: What is SPX? → other
Q: screen spx pe<20 roe>15 → screen
Q: summarize ETF VOO → fund
Q: backtest SPY with 50/200 SMA → backtest
Q: explain diversification risk → risk

Return only one token from {screen,fund,backtest,risk,other}.
"""

def classify_route_llm(text: str) -> tuple[str, dict]:
    """Return (route, debug)."""
    debug = {"used":"heuristic","raw":""}

    # --- Try LLM
    try:
        prompt = FEW_SHOT + f"\nQ: {text}\nA:"
        out = subprocess.check_output(
            shlex.split(f"ollama run llama3.1 '{prompt}'"), timeout=8
        ).decode().strip().lower()
        if out not in CLASS_LABELS:
            raise ValueError(f"bad class {out}")
        debug = {"used":"ollama","raw":out}
        route = out
    except Exception as e:
        debug = {"used":"heuristic_fallback","error":str(e),"raw":""}
        route = _heuristic(text)

    # --- Last-mile sanity: only allow `screen` if user truly asked to screen
    route = _sanity(route, text)
    return route, debug

def _heuristic(text: str) -> str:
    t = (text or "").lower().strip()

    # screen only if explicit screening/filtering or metric comparisons
    screen_kw = any(k in t for k in ("screen","filter","screener"))
    has_metrics = bool(re.search(r"\b(pe|p/e|roe)\b", t)) or bool(re.search(r"[<>]=?\s*\d", t))
    if screen_kw or has_metrics:
        return "screen"

    if any(k in t for k in ("etf","fund","factsheet","fact sheet","prospectus","summary")):
        return "fund"
    if any(k in t for k in ("backtest","sma","rsi","cagr","sharpe")):
        return "backtest"
    if any(k in t for k in ("risk","volatility","drawdown","diversification","beta","var")):
        return "risk"

    # company/ticker names default to other
    return "other"

def _sanity(route: str, text: str) -> str:
    if route != "screen":
        return route
    t = (text or "").lower()
    # must contain REAL screening intent; otherwise demote to other
    if any(k in t for k in ("screen","filter")):
        return "screen"
    if re.search(r"\b(pe|p/e|roe)\b", t) or re.search(r"[<>]=?\s*\d", t):
        return "screen"
    return "other"
