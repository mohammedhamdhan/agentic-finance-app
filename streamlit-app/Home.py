import streamlit as st
from app.ui import inject_css, header, card, two_cols, chips

st.set_page_config(page_title="Agentic Finance (Edu)", page_icon="✨", layout="wide")
inject_css()

header("Agentic Finance — Educational Only",
       "Colorful, glassy, and fast. Screeners, ETF summaries, simple backtests.")

c1, c2, c3 = two_cols((1,1,1))
with c1:
    with card():
        st.markdown("### 🧠 Chat")
        st.caption("Ask in natural language — *“screen spx pe<18 roe>12”*, *“summarize VOO”*, *“backtest SPY 50/200”*.")
        chips([("No advice", "warn"), ("Agentic", "info"), ("Local LLM", "ok")])
with c2:
    with card():
        st.markdown("### 🔎 Screener")
        st.caption("Filter S&P 500 by **PE/ROE** with CSV export and timestamps.")
        chips([("Free APIs", "ok"), ("CSV Export", "info")])
with c3:
    with card():
        st.markdown("### 📄 ETF Summary")
        st.caption("Summarize fund fact sheets with **citations** (when available).")
        chips([("RAG-ready", "info"), ("PDF", "ok")])

st.divider()
with card():
    st.info("**Disclaimer**: For **educational purposes only** — not financial advice.")
