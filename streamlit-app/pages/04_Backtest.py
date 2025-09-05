import streamlit as st
from app.tools.backtest import run_backtest

st.title("📈 Simple Backtest (Educational)")
asset = st.text_input("Asset (e.g., SPY)", value="SPY")
strategy = st.selectbox("Strategy", ["SMA_50_200", "RSI_14"])
span_years = st.slider("Years of history", 1, 10, 5)

if st.button("Run"):
    with st.spinner("Fetching prices (delayed)…"):
        res = run_backtest(asset, strategy, span_years)
    if res.get("error"):
        st.error(res["error"])
    else:
        st.write(res["metrics"])
        st.line_chart(res["equity_curve"])
        st.caption("Assumptions: daily data, no look-ahead; fees/slippage not modeled unless specified.")
