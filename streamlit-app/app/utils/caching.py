import streamlit as st

@st.cache_data(ttl=60*60*24)
def cached_csv(text: str):  # example pattern
    return text
