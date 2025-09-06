import streamlit as st
from app.ui import inject_css, header, card, chips, skeleton
from app.tools.fund_summary import summarize_fund

inject_css()
header("📄 ETF / Fund Summary", "Glassy card with structured info and citations.")

c1, c2 = st.columns((1,3))
with c1:
    ticker = st.text_input("Ticker", value="VOO").upper()
    go = st.button("Summarize", type="primary", use_container_width=True)

placeholder = st.empty()
with card():
    if not go:
        skeleton(3)

if go:
    with st.spinner("Reading document…"):
        s = summarize_fund(ticker)

    placeholder.empty()
    with card():
        if s.get("error"):
            st.error(s["error"])
        else:
            chips([(f"Doc date: {s.get('doc_date','?')}", "info"), (f"Source", "ok")])
            cA, cB = st.columns((1,1))
            with cA:
                st.subheader(ticker)
                st.markdown(f"**Objective**: {s.get('objective','–')}")
                st.markdown(f"**Benchmark**: {s.get('benchmark','–')}")
                st.markdown(f"**Expense Ratio**: {s.get('fees','–')}")
            with cB:
                top = ", ".join(s.get("top_holdings", []) or [])
                st.markdown(f"**Top Holdings**: {top or '–'}")
                st.markdown(f"**Key Risks**: {s.get('risks','–')}")
                st.caption(f"Source URL: {s.get('source_url','?')}")
            if s.get("citations"):
                with st.expander("Citations"):
                    for c in s["citations"]:
                        st.write(f"Page {c.get('page')}: {c.get('snippet','')[:240]}…")
