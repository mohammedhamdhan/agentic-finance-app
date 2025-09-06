import streamlit as st
from contextlib import contextmanager
from typing import List, Tuple

def inject_css():
    if st.session_state.get("_css_injected"):
        return
    st.session_state["_css_injected"] = True

    st.markdown("""
    <style>
      /* ---------- Fonts ---------- */
      @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
      html, body, [class^="css"] {
        font-family: 'Inter', system-ui, -apple-system, Segoe UI, Roboto, sans-serif;
      }

      /* ---------- Page Layout ---------- */
      .block-container { max-width: 1280px; padding-top: 2rem; padding-bottom: 4rem; }
      header[data-testid="stHeader"] { background: transparent; }
      #MainMenu, footer { display: none; }

      /* ---------- Animated Background ---------- */
      body:before {
        content: "";
        position: fixed; inset: -20% -20% auto -20%;
        height: 140vh;
        background: radial-gradient(60% 60% at 10% 10%, rgba(124,58,237,0.18) 0%, rgba(124,58,237,0) 60%),
                    radial-gradient(50% 50% at 90% 20%, rgba(59,130,246,0.18) 0%, rgba(59,130,246,0) 60%),
                    radial-gradient(45% 45% at 40% 80%, rgba(236,72,153,0.14) 0%, rgba(236,72,153,0) 60%);
        filter: blur(60px);
        z-index: -2;
        animation: floaty 22s ease-in-out infinite alternate;
      }
      @keyframes floaty { 
        0% { transform: translateY(-2%) translateX(-2%) scale(1.0); }
        100% { transform: translateY(2%) translateX(1%) scale(1.06); }
      }

      /* ---------- Glass Cards ---------- */
      .glass {
        background: linear-gradient(180deg, rgba(255,255,255,0.06), rgba(255,255,255,0.03));
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 16px;
        padding: 18px 18px;
        box-shadow: 0 8px 40px rgba(0,0,0,0.35);
        backdrop-filter: blur(8px);
        transition: transform .18s ease, border-color .18s ease, box-shadow .18s ease;
      }
      .glass:hover {
        transform: translateY(-2px);
        border-color: rgba(255,255,255,0.18);
        box-shadow: 0 12px 50px rgba(0,0,0,0.45);
      }

      /* ---------- Hero ---------- */
      .hero-title {
        font-weight: 800;
        letter-spacing: -0.02em;
        font-size: clamp(28px, 3.4vw, 48px);
        background: linear-gradient(90deg,#FDE68A 0%,#A78BFA 40%,#60A5FA 80%);
        -webkit-background-clip: text; background-clip: text; color: transparent;
        margin-bottom: 6px;
      }
      .hero-sub { color: #B9C2DF; margin-bottom: 14px; }

      /* ---------- Chips / Badges ---------- */
      .chip {
        display: inline-flex; align-items: center; gap: 8px;
        border-radius: 999px; padding: 6px 12px; font-size: 12px; font-weight: 600;
        border: 1px solid rgba(255,255,255,0.16);
        background: rgba(255,255,255,0.06);
      }
      .chip.ok   { color:#B4F0D0; border-color:rgba(34,197,94,0.35); background:linear-gradient(180deg,rgba(34,197,94,0.18),rgba(34,197,94,0.08)); }
      .chip.warn { color:#FFD8AE; border-color:rgba(245,158,11,0.35); background:linear-gradient(180deg,rgba(245,158,11,0.18),rgba(245,158,11,0.08)); }
      .chip.info { color:#C8D6FF; border-color:rgba(99,102,241,0.35); background:linear-gradient(180deg,rgba(99,102,241,0.18),rgba(99,102,241,0.08)); }

      /* ---------- Fancy Buttons ---------- */
      .btn {
        display:inline-block; padding:10px 14px; border-radius:12px; font-weight:700;
        color:#0B0D13; background:linear-gradient(180deg,#FDE68A 0%, #FCA5A5 50%, #A78BFA 100%);
        box-shadow: 0 6px 22px rgba(124,58,237,0.35);
        border: none; cursor:pointer; user-select:none;
      }
      .btn:hover { filter: brightness(1.05); transform: translateY(-1px); transition: 150ms ease; }

      /* ---------- Chat Bubbles ---------- */
      .bubble { padding:14px 16px; border-radius:14px; margin:8px 0; max-width: 95%; }
      .bubble.user { background: #131a2e; border: 1px solid rgba(255,255,255,0.10); margin-left:auto; }
      .bubble.ai   { background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.10); }

      /* ---------- DataFrames ---------- */
      .stDataFrame { border-radius: 12px; overflow: hidden; }

      /* ---------- Skeleton ---------- */
      .skeleton {
        height: 16px; border-radius: 8px; width: 100%;
        background: linear-gradient(90deg, rgba(255,255,255,0.06) 25%, rgba(255,255,255,0.12) 37%, rgba(255,255,255,0.06) 63%);
        background-size: 400% 100%;
        animation: shimmer 1.3s ease infinite;
      }
      @keyframes shimmer { 0%{background-position: 100% 0;} 100%{background-position: 0 0;} }

      /* ---------- Metrics ---------- */
      .kpi {
        display:flex; flex-direction:column; gap:6px; padding:14px;
        border-radius:14px; background:rgba(255,255,255,0.05);
        border:1px solid rgba(255,255,255,0.10);
      }
      .kpi .label { color:#B7C3E0; font-size:12px; font-weight:600; text-transform:uppercase; letter-spacing: .06em; }
      .kpi .value { font-size:22px; font-weight:800; }
    </style>
    """, unsafe_allow_html=True)

def header(title: str, subtitle: str = ""):
    st.markdown(f"<div class='hero-title'>{title}</div>", unsafe_allow_html=True)
    if subtitle:
        st.markdown(f"<div class='hero-sub'>{subtitle}</div>", unsafe_allow_html=True)

@contextmanager
def card(hover=True):
    st.markdown(f"<div class='glass'>", unsafe_allow_html=True)
    try:
        yield
    finally:
        st.markdown("</div>", unsafe_allow_html=True)

def chips(items: List[Tuple[str, str]]):
    # list of (text, kind)
    html = "".join([f"<span class='chip {k}'>{t}</span>&nbsp;" for t,k in items])
    st.markdown(html, unsafe_allow_html=True)

def kpi(label: str, value: str):
    st.markdown(f"<div class='kpi'><div class='label'>{label}</div><div class='value'>{value}</div></div>", unsafe_allow_html=True)

def two_cols(ratios=(1,1)):
    return st.columns(ratios, gap="large")

def button(label: str, key: str):
    st.markdown(f"<button class='btn' id='{key}'>{label}</button>", unsafe_allow_html=True)
    return st.button(label, key=f"st_{key}", type="primary", use_container_width=True)

def skeleton(lines=3):
    for _ in range(lines):
        st.markdown("<div class='skeleton'></div>", unsafe_allow_html=True)
