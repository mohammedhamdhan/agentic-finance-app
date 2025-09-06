import streamlit as st
from app.ui import inject_css, header, card, kpi, skeleton
from app.tools.backtest import run_backtest

inject_css()
header("📈 Simple Backtest", "Clean metrics and a smooth chart.")

c1, c2, c3 = st.columns((1,1,1))
with c1: asset = st.text_input("Asset", value="SPY")
with c2: strategy = st.selectbox("Strategy", ["SMA_50_200", "RSI_14"])
with c3: years = st.slider("Years", 1, 10, 5)
go = st.button("Run", type="primary", use_container_width=True)

if not go:
    with card(): skeleton(3)

if go:
    with st.spinner("Fetching & computing…"):
        res = run_backtest(asset, strategy, years)
    with card():
        if res.get("error"):
            st.error(res["error"])
        else:
            m = res["metrics"]
            cA, cB, cC = st.columns((1,1,1))
            with cA: kpi("CAGR", str(m.get("CAGR","–")))
            with cB: kpi("Sharpe", str(m.get("Sharpe","–")))
            with cC: kpi("Max DD", str(m.get("MaxDD","–")))
            st.line_chart(res["equity_curve"], use_container_width=True)
            st.caption("Assumptions: daily data; no look-ahead; fees/slippage not modeled.")
