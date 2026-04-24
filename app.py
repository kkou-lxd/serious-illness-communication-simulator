"""Main entry point for the Serious Illness Communication Simulator."""

from __future__ import annotations

from pathlib import Path

import streamlit as st

st.set_page_config(
    page_title="Serious Illness Communication Simulator",
    page_icon="💬",
    layout="wide",
)

# ── Inject all custom styles ────────────────────────────────────────────────
def _inject_styles() -> None:
    """Load external CSS and inject global styles + Google Fonts."""

    # Google Fonts: DM Serif Display (title) + Lato (body) — warm, editorial pair
    st.markdown(
        """
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Lato:wght@300;400;700&display=swap" rel="stylesheet">
        """,
        unsafe_allow_html=True,
    )

    css = """
    /* ── Reset & Root ─────────────────────────────────────────── */
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

    /* ── Global overrides ─────────────────────────────────────── */
    html, body,
    [data-testid="stAppViewContainer"],
    [data-testid="stAppViewBlockContainer"],
    [data-testid="stMain"],
    .main, .stApp {
        background-color: var(--bg) !important;
        font-family: var(--font-body) !important;
        color: var(--text-primary) !important;
    }

    /* Kill sidebar + its toggle completely */
    [data-testid="stSidebar"],
    [data-testid="collapsedControl"],
    section[data-testid="stSidebarNav"] {
        display: none !important;
    }

    /* Nuke the purple toolbar — every known selector across Streamlit versions */
    header[data-testid="stHeader"],
    [data-testid="stHeader"],
    [data-testid="stToolbar"],
    [data-testid="stDecoration"],
    #stDecoration,
    .stDeployButton,
    .viewerBadge_container__1QSob,
    [data-testid="manage-app-button"] {
        display: none !important;
        height: 0 !important;
        visibility: hidden !important;
    }

    /* Remove default top padding from main block */
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }

    /* ── Hero wrapper ─────────────────────────────────────────── */
    .hero-wrapper {
        min-height: 100vh;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 60px 24px;
        background-color: var(--bg);
    }

    /* ── Decorative top rule ──────────────────────────────────── */
    .hero-ornament {
        width: 48px;
        height: 3px;
        background: var(--accent);
        border-radius: 2px;
        margin: 0 auto 40px auto;
        opacity: 0.75;
    }

    /* ── Eyebrow label above title ────────────────────────────── */
    .hero-eyebrow {
        font-family: var(--font-body);
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.22em;
        text-transform: uppercase;
        color: var(--accent);
        margin-bottom: 20px;
        text-align: center;
    }

    /* ── Main title ───────────────────────────────────────────── */
     .hero-title {
        font-family: var(--font-title);
        font-size: clamp(39px, 4vw, 58px) !important; 
        font-weight: 400;
        color: var(--text-primary);
        text-align: center;
        line-height: 1.15 !important;
        letter-spacing: -0.01em;
        max-width: 900px !important; 
        margin: 0 auto 36px auto;
    }

    .hero-title em {
        font-style: italic;
        color: var(--accent);
    }

    /* ── Divider between title and body ──────────────────────── */
    .hero-divider {
        width: 1px;
        height: 44px;
        background: linear-gradient(to bottom, var(--border), transparent);
        margin: 0 auto 36px auto;
    }

    /* ── Body / welcome text ──────────────────────────────────── */
    .hero-body {
        font-family: var(--font-body);
        font-size: clamp(15px, 1.8vw, 17px);
        font-weight: 300;
        line-height: 1.80;
        color: var(--text-muted);
        text-align: center;
        max-width: 520px;
        margin: 0 auto 56px auto;
    }

    /* ── CTA button ───────────────────────────────────────────── */
    .cta-link {
        display: inline-block;
        background-color: var(--accent);
        color: #FFFFFF !important;
        text-decoration: none !important;
        font-family: var(--font-body);
        font-size: 14px;
        font-weight: 700;
        letter-spacing: 0.08em;
        padding: 16px 52px;
        border-radius: var(--radius-pill);
        border: 2px solid transparent;
        cursor: pointer;
        transition:
            background-color 0.22s ease,
            box-shadow       0.22s ease,
            transform        0.18s ease;
        box-shadow: 0 4px 18px rgba(193, 127, 90, 0.22);
    }

    .cta-link:hover {
        background-color: var(--accent-hover);
        box-shadow: 0 8px 28px rgba(168, 104, 69, 0.32);
        transform: translateY(-2px);
    }

    .cta-link:active {
        transform: translateY(0px);
        box-shadow: 0 2px 10px rgba(168, 104, 69, 0.20);
    }

    /* ── Footer note ──────────────────────────────────────────── */
    .hero-footer {
        margin-top: 72px;
        font-family: var(--font-body);
        font-size: 11px;
        letter-spacing: 0.06em;
        color: var(--border);
        text-align: center;
        text-transform: uppercase;
    }

    /* ── Fade-in animation on load ────────────────────────────── */
    @keyframes fadeUp {
        from { opacity: 0; transform: translateY(18px); }
        to   { opacity: 1; transform: translateY(0);    }
    }

    .hero-ornament  { animation: fadeUp 0.6s ease both; animation-delay: 0.05s; }
    .hero-eyebrow   { animation: fadeUp 0.6s ease both; animation-delay: 0.12s; }
    .hero-title     { animation: fadeUp 0.7s ease both; animation-delay: 0.22s; }
    .hero-divider   { animation: fadeUp 0.6s ease both; animation-delay: 0.32s; }
    .hero-body      { animation: fadeUp 0.7s ease both; animation-delay: 0.40s; }
    .cta-link       { animation: fadeUp 0.7s ease both; animation-delay: 0.52s; }
    .hero-footer    { animation: fadeUp 0.6s ease both; animation-delay: 0.64s; }
    """

    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

    # Also load external CSS if it exists (keeps your original asset pipeline intact)
    css_path = Path(__file__).resolve().parent / "assets" / "styles.css"
    if css_path.exists():
        external_css = css_path.read_text(encoding="utf-8")
        st.markdown(f"<style>{external_css}</style>", unsafe_allow_html=True)


_inject_styles()

# ── Hero section ─────────────────────────────────────────────────────────────
# NOTE: HTML passed to st.markdown() must NOT have lines indented by 4+ spaces,
# or Markdown will interpret them as a fenced code block. We build the string
# explicitly with no leading whitespace per line to avoid that pitfall.
_HERO_HTML = (
"<div class='hero-wrapper'>"
"<div class='hero-ornament'></div>"
"<p class='hero-eyebrow'>A Training Experience</p>"
"<h1 class='hero-title'>Serious Illness<br><em>Communication</em> Simulator</h1>"
"<div class='hero-divider'></div>"
"<p class='hero-body'>"
"Every difficult conversation deserves to be approached with kindness. "
"In this safe, simulated space, we will explore how to "
"convey both the weight and the strength of our experiences."
"</p>"
"<a href='/Home' class='cta-link' target='_self'>Go to Home &nbsp;\U0001f3e0</a>"
"<p class='hero-footer'>Pediatric Palliative Care</p>"
"</div>"
)

# st.html() (Streamlit ≥ 1.31) is the cleanest path; fall back to st.markdown.
try:
    st.html(_HERO_HTML)
except AttributeError:
    st.markdown(_HERO_HTML, unsafe_allow_html=True)
