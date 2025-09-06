# streamlit_app/app/utils/ui.py
from datetime import datetime, timedelta
import streamlit as st

def stale_badge(as_of_iso: str, days: int = 14):
    try:
        as_of = datetime.fromisoformat(as_of_iso).date()
        if (datetime.utcnow().date() - as_of) > timedelta(days=days):
            st.warning(f"Data may be stale (as of {as_of_iso}).")
    except Exception:
        pass
