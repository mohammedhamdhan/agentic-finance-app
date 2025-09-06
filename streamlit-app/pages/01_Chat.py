import streamlit as st, uuid
from app.ui import inject_css, header, card, chips
from app.agents.router import route_query

inject_css()
header("🧠 Agentic Chat", "Colorful bubbles, router badges, and tidy artifacts.")

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = str(uuid.uuid4())

q = st.text_area("Message", placeholder="e.g., screen spx pe<18 roe>12, then backtest SPY 50/200", height=110)
go = st.button("Run", type="primary", use_container_width=True)

if go and q.strip():
    with st.spinner("Thinking…"):
        res = route_query(q, thread_id=st.session_state["thread_id"])

    dbg = (res.get("artifacts") or {}).get("router_debug")
    if dbg:
        chips([(f"Router: {dbg.get('used','?')}", "ok")])

    with card():
        st.markdown(f"<div class='bubble ai'>{res.get('message','')}</div>", unsafe_allow_html=True)

    art = res.get("artifacts", {})
    keys = [k for k in ("screen","fund","backtest","risk") if k in art]
    if keys:
        tabs = st.tabs([k.capitalize() for k in keys])
        for key, tab in zip(keys, tabs):
            with tab:
                if key == "screen":
                    import pandas as pd
                    df = pd.DataFrame(art["screen"].get("rows", []))
                    meta = art["screen"].get("meta", {})
                    chips([(f"As-of {meta.get('as_of','?')}", "info"), (f"Source: {meta.get('source','?')}", "info")])
                    st.dataframe(df, use_container_width=True, height=380)
                    if meta.get("csv"):
                        st.download_button("Download CSV", meta["csv"].encode("utf-8"), "screen.csv")
                elif key == "fund":
                    f = art["fund"]
                    c1, c2 = st.columns((1,1))
                    with c1:
                        st.subheader(f.get("ticker","ETF"))
                        st.markdown(f"**Objective**: {f.get('objective','–')}")
                        st.markdown(f"**Benchmark**: {f.get('benchmark','–')}")
                        st.markdown(f"**Expense Ratio**: {f.get('fees','–')}")
                    with c2:
                        top = ", ".join(f.get("top_holdings", []) or [])
                        st.markdown(f"**Top Holdings**: {top or '–'}")
                        st.markdown(f"**Key Risks**: {f.get('risks','–')}")
                        st.caption(f"Doc date: {f.get('doc_date','?')} • Source: {f.get('source_url','?')}")
                elif key == "backtest":
                    from app.ui import kpi
                    b = art["backtest"]
                    if b.get("error"):
                        st.error(b["error"])
                    else:
                        m = b.get("metrics", {})
                        cA, cB, cC = st.columns((1,1,1))
                        with cA: kpi("CAGR", str(m.get("CAGR","–")))
                        with cB: kpi("Sharpe", str(m.get("Sharpe","–")))
                        with cC: kpi("Max DD", str(m.get("MaxDD","–")))
                        eq = b.get("equity_curve")
                        try:
                            import pandas as pd
                            if eq is not None and not isinstance(eq, pd.Series):
                                eq = pd.Series(eq)
                            if eq is not None:
                                st.line_chart(eq, use_container_width=True)
                        except Exception:
                            pass
                elif key == "risk":
                    st.write(art["risk"].get("text",""))
