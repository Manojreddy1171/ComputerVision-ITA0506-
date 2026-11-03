# ============================================================
#  Intelligent Retail Shelf Monitoring System
#  Main Entry Point – app.py
# ============================================================

import sys
import os
from pathlib import Path

# Ensure root directory and modules can be found regardless of CWD
APP_DIR = Path(__file__).resolve().parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

import streamlit as st

# ─── Page Configuration ───────────────────────────────────────
st.set_page_config(
    page_title = "RetailVision AI — Shelf Monitoring",
    page_icon  = "🛒",
    layout     = "wide",
    initial_sidebar_state = "expanded",
)

# ─── Inject Custom SaaS CSS ───────────────────────────────────
css_path = APP_DIR / "assets" / "styles.css"
if css_path.exists():
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ─── Safe Navigation Request Pattern ─────────────────────────
# Prevents StreamlitWidgetAlreadyInstantiatedError:
# Any navigation button writes to st.session_state["nav_request"] via an on_click callback.
# Before creating the st.radio widget, nav_request is popped into nav_selection.
if "nav_selection" not in st.session_state:
    st.session_state["nav_selection"] = "🏠 Home"

if "nav_request" in st.session_state:
    st.session_state["nav_selection"] = st.session_state.pop("nav_request")

NAV_OPTIONS = ["🏠 Home", "🔍 Shelf Analysis", "📊 Dashboard", "ℹ️ About"]

# ─── Sidebar Redesign (Clean, Compact, Minimal) ───────────────
with st.sidebar:
    st.markdown(
        """
        <div style='padding: 10px 4px 6px;'>
            <div style='display:flex; align-items:center; gap:10px;'>
                <span style='font-size:1.8rem;'>🛒</span>
                <div>
                    <h2 style='font-family:Poppins,sans-serif; font-weight:800;
                               font-size:1.15rem; margin:0; color:#FFFFFF; line-height:1.2;'>
                        RetailVision AI
                    </h2>
                    <p style='font-size:0.75rem; color:#94A3B8; margin:2px 0 0;'>
                        Intelligent Shelf Monitoring
                    </p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<hr/>", unsafe_allow_html=True)

    page = st.radio(
        label            = "Navigation",
        options          = NAV_OPTIONS,
        key              = "nav_selection",
        label_visibility = "collapsed",
    )

    st.markdown("<hr/>", unsafe_allow_html=True)

    # Clean model status badge at the bottom of the sidebar
    model_custom_path = APP_DIR / "models" / "best.pt"
    if model_custom_path.exists():
        badge_html = """
        <div style='padding: 4px 6px;'>
            <span class='sidebar-badge sidebar-badge-custom'>● Custom Model Active</span>
            <p style='font-size:0.72rem; color:#94A3B8; margin:6px 0 0;'>
                Tracking: Coke, Pepsi, Sprite
            </p>
        </div>
        """
    else:
        badge_html = """
        <div style='padding: 4px 6px;'>
            <span class='sidebar-badge sidebar-badge-demo'>● Demo Mode (COCO)</span>
            <p style='font-size:0.72rem; color:#94A3B8; margin:6px 0 0;'>
                Pretrained nano weights
            </p>
        </div>
        """
    st.markdown(badge_html, unsafe_allow_html=True)

# ─── Route to Pages ──────────────────────────────────────────
if "🏠 Home" in page:
    from pages.home import show_home
    show_home()

elif "🔍 Shelf Analysis" in page:
    from pages.shelf_analysis import show_shelf_analysis
    show_shelf_analysis()

elif "📊 Dashboard" in page:
    from pages.dashboard import show_dashboard
    show_dashboard()

elif "ℹ️ About" in page:
    from pages.about import show_about
    show_about()
