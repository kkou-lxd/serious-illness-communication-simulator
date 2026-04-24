from __future__ import annotations

import streamlit as st

st.set_page_config(
    page_title="Home — Simulator",
    initial_sidebar_state="collapsed"
)
st.markdown("""
    <style>
        [data-testid="stSidebar"] {display: none;}
        [data-testid="collapsedControl"] {display: none;}
    </style>
""", unsafe_allow_html=True)


# ── Inject design system CSS ──────────────────────────────────
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Lato:wght@300;400;700&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

st.markdown("""
<style>
:root {
    --bg:           #FBF7F0;
    --surface:      #F2EEE8;
    --text-primary: #3A3530;
    --text-muted:   #7A746D;
    --accent:       #C17F5A;
    --accent-hover: #A86845;
    --accent-light: #F0E0D2;
    --border:       #E2DAD1;
    --radius-pill:  50px;
    --font-title:   'DM Serif Display', Georgia, serif;
    --font-body:    'Lato', system-ui, sans-serif;
}

/* ── Global ── */
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"],
[data-testid="stMain"],
.main, .stApp {
    background-color: var(--bg) !important;
    font-family: var(--font-body) !important;
    color: var(--text-primary) !important;
}

/* ── Hide chrome ── */
[data-testid="stSidebar"],
[data-testid="collapsedControl"],
header[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
.stDeployButton {
    display: none !important;
    height: 0 !important;
    visibility: hidden !important;
}

.block-container {
    padding: 60px 40px !important;
    max-width: 860px !important;
    margin: 0 auto !important;
}

/* ── Page header ── */
.cc-page-header {
    text-align: center;
    margin-bottom: 56px;
}

.cc-page-title {
    font-family: var(--font-title) !important;
    font-size: 36px !important;    
    font-weight: 400 !important;
    color: var(--text-primary) !important;
    line-height: 1.2 !important;   
    margin: 0 0 14px 0 !important;
}

.cc-page-sub {
    font-family: var(--font-body);
    font-size: 16px;
    font-weight: 300;
    color: var(--text-muted);
    line-height: 1.7;
    margin: 0;
}

/* ── Role cards grid ── */
.cc-role-cards {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px;
    margin-bottom: 40px;
}

@media (max-width: 600px) {
    .cc-role-cards { grid-template-columns: 1fr; }
}

.cc-role-card {
    display: block;                          
    text-decoration: none !important;
    background: var(--surface);
    border: 1.5px solid var(--border);
    border-radius: 16px;
    padding: 36px 28px;
    text-align: center;
    cursor: pointer;
    transition: box-shadow 0.22s ease, transform 0.18s ease, border-color 0.22s ease;
}

.cc-role-card:hover {
    border-color: var(--accent);
    box-shadow: 0 8px 28px rgba(193, 127, 90, 0.14);
    transform: translateY(-3px);
}

.cc-role-icon {
    font-size: 36px;
    margin-bottom: 16px;
    display: block;
}

.cc-role-title {
    font-family: var(--font-title);
    font-size: 22px;
    font-weight: 400;
    color: var(--text-primary);
    margin: 0 0 10px 0;
}

.cc-role-desc {
    font-family: var(--font-body);
    font-size: 14px;
    font-weight: 300;
    color: var(--text-muted);
    line-height: 1.65;
    margin: 0 0 20px 0;
}

.cc-role-cta {
    font-family: var(--font-body);
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.06em;
    color: var(--accent);
    margin: 0;
    text-transform: uppercase;
}

/* ── Streamlit buttons ── */
.stButton > button {
    font-family: var(--font-body) !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    letter-spacing: 0.06em !important;
    color: var(--text-muted) !important;
    background-color: transparent !important;
    border: 1.5px solid var(--border) !important;
    border-radius: var(--radius-pill) !important;
    padding: 10px 28px !important;
    transition: all 0.22s ease !important;
    box-shadow: none !important;
}

.stButton > button:hover {
    border-color: #2D2660 !important;
    color: #2D2660 !important;
    background-color: #F2F0FB !important;
    box-shadow: none !important;
    transform: none !important;
}

/* ── Fade-in ── */
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
}

.cc-page-header { animation: fadeUp 0.6s ease both 0.1s; }
.cc-role-cards  { animation: fadeUp 0.7s ease both 0.25s; }
</style>
""", unsafe_allow_html=True)
# ──────────────────────────────────────────────────────────────

st.markdown("""
<div class="cc-page-header">
  <p class="cc-page-title">Serious Illness Communication Simulator</p>
  <p class="cc-page-sub">An AI-powered role-play environment for medical trainees.</p>
</div>
<div class="cc-role-cards">
  <a href="/Teacher" class="cc-role-card" target="_self">
    <span class="cc-role-icon">🎓</span>
    <p class="cc-role-title">I am a teacher</p>
    <p class="cc-role-desc">Set up courses, configure cases, and review student session records.</p>
    <p class="cc-role-cta">Go to teacher panel →</p>
  </a>
  <a href="/Student" class="cc-role-card" target="_self">
    <span class="cc-role-icon">💬</span>
    <p class="cc-role-title">I am a student</p>
    <p class="cc-role-desc">Enter your course, select a case, and start a live simulation.</p>
    <p class="cc-role-cta">Start a simulation →</p>
  </a>
</div>
""", unsafe_allow_html=True)

if st.button("Back"):
    try:
        st.switch_page("app.py")
    except Exception:
        pass


def _go_to(page_path: str) -> None:
    try:
        st.switch_page(page_path)
    except Exception:
        pass



