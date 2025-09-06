import uuid, streamlit as st
from app.agents.router import route_query

st.title("🧠 Agentic Chat (Educational)")
if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = str(uuid.uuid4())
user_msg = st.text_area("Describe your task (e.g., 'screen SPX pe<18 roe>12, then backtest SPY SMA 50/200, and summarize VOO')", height=120)

if st.button("Run"):
    with st.spinner("Running agent..."):
        result = route_query(user_msg, thread_id=st.session_state["thread_id"])
    st.success(result.get("message",""))
    artifacts = result.get("artifacts", {})

    if "screen" in artifacts:
        st.subheader("Screener Results")
        meta = artifacts["screen"].get("meta", {})
        st.caption(f"As-of: {meta.get('as_of','?')} • Source: {meta.get('source','?')}")
        import pandas as pd
        st.dataframe(pd.DataFrame(artifacts["screen"].get("rows", [])), use_container_width=True)
        if meta.get("csv"):
            st.download_button("Download CSV", meta["csv"].encode("utf-8"), file_name="screen.csv")

    if "fund" in artifacts:
        st.subheader("ETF Summary")
        f = artifacts["fund"]
        st.markdown(f"**Objective:** {f.get('objective','N/A')}")
        st.markdown(f"**Benchmark:** {f.get('benchmark','N/A')}")
        st.markdown(f"**Expense Ratio:** {f.get('fees','N/A')}")
        st.markdown(f"**Top Holdings:** {', '.join(f.get('top_holdings', [])) or 'N/A'}")
        st.markdown(f"**Key Risks:** {f.get('risks','N/A')}")
        st.caption(f"Doc date: {f.get('doc_date','?')} • Source: {f.get('source_url','?')}")
        if f.get("citations"):
            with st.expander("Citations"):
                for c in f["citations"]:
                    st.write(f"Page {c.get('page')}: {c.get('snippet','')[:240]}…")

    if "backtest" in artifacts:
        st.subheader("Backtest")
        b = artifacts["backtest"]
        if b.get("error"):
            st.error(b["error"])
        else:
            st.json(b.get("metrics", {}))
            # equity_curve may be a pandas Series; handle both dict and series
            eq = b.get("equity_curve")
            try:
                import pandas as pd
                if not isinstance(eq, pd.Series):
                    eq = pd.Series(eq)
                st.line_chart(eq)
            except Exception:
                st.write("Equity curve not available.")
            st.caption("Assumptions: daily data, no look-ahead; fees/slippage not modeled unless specified.")

    if "risk" in artifacts:
        st.subheader("Risk Explainer")
        st.write(artifacts["risk"].get("text",""))
