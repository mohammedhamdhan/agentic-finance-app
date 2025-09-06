import streamlit as st
from app.ui import inject_css, header, card, chips, skeleton
from app.tools.screener import screen_spx

inject_css()
header("🔎 Screener", "Glassy table with colorful badges.")

with card():
    with st.form("screen_form"):
        c1, c2, c3 = st.columns((1,1,1))
        with c1: pe_max = st.number_input("PE <", value=20.0, step=0.5)
        with c2: roe_min = st.number_input("ROE >", value=0.15, step=0.01, format="%.2f")
        with c3: go = st.form_submit_button("Run Screen", type="primary", use_container_width=True)

if 'screen_last' not in st.session_state: st.session_state['screen_last'] = None

if go:
    with st.spinner("Fetching fundamentals…"):
        rows, meta = screen_spx(pe_max=pe_max, roe_min=roe_min)
    st.session_state['screen_last'] = (rows, meta)

if st.session_state['screen_last']:
    rows, meta = st.session_state['screen_last']
    with card():
        chips([(f"As-of {meta.get('as_of','?')}", "info"), (f"Source: {meta.get('source','?')}", "info")])
        st.dataframe(rows, use_container_width=True, height=420)
        if meta.get("csv"):
            st.download_button("Download CSV", meta["csv"].encode("utf-8"), "screen.csv", use_container_width=True)
else:
    with card():
        skeleton(4)
