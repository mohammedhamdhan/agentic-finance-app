import streamlit as st

def _heuristic(text: str) -> str:
    t = (text or "").lower()
    if "screen" in t or "pe" in t or "roe" in t: return "screen"
    if "etf" in t or "fund" in t or "summary" in t: return "fund"
    if "backtest" in t or "sma" in t or "rsi" in t: return "backtest"
    if "risk" in t or "volatility" in t or "drawdown" in t: return "risk"
    return "other"

def classify_route_llm(text: str) -> str:
    try:
        import subprocess, shlex
        prompt = (
            "Classify into: screen, fund, backtest, risk, other. "
            f"User: {text!r}\nReturn ONLY the class token."
        )
        cmd = f"ollama run llama3.1 '{prompt}'"
        out = subprocess.check_output(shlex.split(cmd), timeout=8).decode().strip().lower()
        # 👇 show raw response in Streamlit
        st.info(f"Ollama raw response: {out}")
        if out in {"screen","fund","backtest","risk"}:
            return out
        return _heuristic(text)
    except Exception as e:
        st.warning(f"Ollama fallback: {e}")
        return _heuristic(text)
