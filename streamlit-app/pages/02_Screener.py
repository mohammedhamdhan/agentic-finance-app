import streamlit as st
from app.tools.screener import screen_spx

st.title("🔎 Screener (S&P 500)")
pe_max = st.number_input("PE < ", value=20.0, step=0.5)
roe_min = st.number_input("ROE > ", value=0.15, step=0.01, format="%.2f")

if st.button("Run screen"):
    with st.spinner("Querying local DB..."):
        rows, meta = screen_spx(pe_max=pe_max, roe_min=roe_min)
    st.success(f"{len(rows)} results • as-of: {meta.get('as_of')} • source: {meta.get('source')}")
    st.dataframe(rows, use_container_width=True)
    st.download_button("Download CSV", meta.get("csv", "").encode("utf-8"), file_name="screen.csv")

st.caption("Educational only. Metrics are TTM and may be delayed; see as-of timestamp and source.")
