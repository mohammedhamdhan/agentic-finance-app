import streamlit as st
from app.agents.router import route_query

st.title("🧠 Agentic Chat (Educational)")
user_msg = st.text_area("Ask a task (e.g., 'screen SPX pe<18 roe>12, compare to VOO, run SMA 50/200 on SPY')", height=120)

if st.button("Run"):
    with st.spinner("Thinking..."):
        result = route_query(user_msg)
    st.write(result["message"])
    if "artifacts" in result:
        with st.expander("Artifacts / Data"):
            st.json(result["artifacts"])
st.caption("No personal financial advice. Outputs include timestamps, sources, and limitations when available.")
