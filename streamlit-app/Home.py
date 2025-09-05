import streamlit as st
from app.config import settings

st.set_page_config(page_title="Agentic Finance (Edu)", page_icon="📊", layout="wide")

st.title("Agentic Finance — Educational Only")
st.info("This tool is for **educational purposes only** and **not financial advice**.")

st.markdown("""
Use the sidebar pages:
- **Chat**: natural language tasks (screen, summarize funds, run simple backtests, explain risks)
- **Screener**: filter S&P 500 by PE/ROE
- **ETF Summary**: summarize fund fact sheets with citations
- **Backtest**: simple SMA/RSI demos (assumptions shown)
""")

st.caption(f"Data dir: `{settings.DATA_DIR}` • FAISS dir: `{settings.FAISS_DIR}`")
