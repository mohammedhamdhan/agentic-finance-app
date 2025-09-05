import streamlit as st
from app.tools.fund_summary import summarize_fund

st.title("📄 ETF / Fund Summary")
ticker = st.text_input("Fund ticker (e.g., VOO, SPY, IVV)", value="VOO")

if st.button("Summarize"):
    with st.spinner("Retrieving local docs..."):
        summary = summarize_fund(ticker.strip().upper())
    if summary.get("error"):
        st.error(summary["error"])
    else:
        st.markdown(f"**Objective:** {summary.get('objective','N/A')}")
        st.markdown(f"**Benchmark:** {summary.get('benchmark','N/A')}")
        st.markdown(f"**Expense Ratio:** {summary.get('fees','N/A')}")
        st.markdown(f"**Top Holdings:** {', '.join(summary.get('top_holdings', [])) or 'N/A'}")
        st.markdown(f"**Key Risks:** {summary.get('risks','N/A')}")
        st.caption(f"Doc date: {summary.get('doc_date','?')} • Source: {summary.get('source_url','?')}")
        if summary.get("citations"):
            with st.expander("Citations"):
                for c in summary["citations"]:
                    st.write(f"Page {c.get('page')} • {c.get('snippet','')}")
