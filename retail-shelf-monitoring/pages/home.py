# ============================================================
#  Home Page — Modern AI SaaS Landing
# ============================================================

import streamlit as st


def _request_analysis():
    """Safe navigation callback to Shelf Analysis."""
    st.session_state["nav_request"] = "🔍 Shelf Analysis"


def show_home():
    # ── 1. Hero Section (Split Layout) ───────────────────────
    hero_col_left, hero_col_right = st.columns([1.5, 1], gap="large")

    with hero_col_left:
        st.markdown(
            """
            <div>
                <span class="hero-pill">⚡ COMPUTER VISION CAPSTONE</span>
                <h1 class="hero-title">
                    Intelligent Retail Shelf Monitoring
                </h1>
                <p class="hero-sub">
                    Detect products, measure shelf availability, and identify restocking needs using Computer Vision.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.button(
            "🚀 Analyze a Shelf",
            type="primary",
            on_click=_request_analysis,
            key="home_cta_analysis_btn",
        )

        st.markdown(
            """
            <p style='font-size:0.84rem; color:#6B7280; margin-top:14px;'>
                Upload a retail shelf image and get instant product counts and stock-status insights.
            </p>
            """,
            unsafe_allow_html=True,
        )

    with hero_col_right:
        st.markdown(
            """
            <div class="hero-side-card">
                <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:14px;'>
                    <span style='font-size:0.75rem; font-weight:700; color:#4F46E5; text-transform:uppercase; letter-spacing:0.06em;'>
                        LIVE SHELF SCANNER
                    </span>
                    <span class='status-badge-saas status-available'>● SYSTEM ONLINE</span>
                </div>
                <div style='display:flex; flex-direction:column; gap:10px;'>
                    <div style='background:#FFFFFF; border:1px solid #E5E7EB; border-radius:8px; padding:10px 14px; display:flex; justify-content:space-between; align-items:center;'>
                        <span style='font-weight:600; font-size:0.88rem;'>🥫 Coke</span>
                        <span class='status-badge-saas status-available'>6 Units · Available</span>
                    </div>
                    <div style='background:#FFFFFF; border:1px solid #E5E7EB; border-radius:8px; padding:10px 14px; display:flex; justify-content:space-between; align-items:center;'>
                        <span style='font-weight:600; font-size:0.88rem;'>🥫 Pepsi</span>
                        <span class='status-badge-saas status-low'>2 Units · Low Stock</span>
                    </div>
                    <div style='background:#FFFFFF; border:1px solid #E5E7EB; border-radius:8px; padding:10px 14px; display:flex; justify-content:space-between; align-items:center;'>
                        <span style='font-weight:600; font-size:0.88rem;'>🥫 Sprite</span>
                        <span class='status-badge-saas status-out'>0 Units · Out of Stock</span>
                    </div>
                </div>
                <div style='margin-top:16px; padding-top:12px; border-top:1px solid #E2E8F0; display:flex; justify-content:space-between; font-size:0.75rem; color:#64748B;'>
                    <span>Detection Model: <b>YOLOv8 Nano</b></span>
                    <span>Inference: <b>~85 ms</b></span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br/>", unsafe_allow_html=True)

    # ── 2. Visual Process Workflow (5 Steps with Arrows) ──────
    st.markdown(
        "<div class='section-title'>⚙️ System Workflow</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p class='section-sub'>End-to-end pipeline from shelf photograph acquisition to real-time inventory decisions.</p>",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="workflow-row">
            <div class="workflow-node">
                <div class="workflow-icon">📤</div>
                <div>
                    <div class="workflow-title">Upload</div>
                    <div style="font-size:0.72rem; color:#6B7280;">Shelf Photo</div>
                </div>
            </div>
            <div class="workflow-arrow">→</div>
            <div class="workflow-node">
                <div class="workflow-icon">🔍</div>
                <div>
                    <div class="workflow-title">Detect</div>
                    <div style="font-size:0.72rem; color:#6B7280;">YOLO Bboxes</div>
                </div>
            </div>
            <div class="workflow-arrow">→</div>
            <div class="workflow-node">
                <div class="workflow-icon">🏷️</div>
                <div>
                    <div class="workflow-title">Recognize</div>
                    <div style="font-size:0.72rem; color:#6B7280;">Product Class</div>
                </div>
            </div>
            <div class="workflow-arrow">→</div>
            <div class="workflow-node">
                <div class="workflow-icon">📊</div>
                <div>
                    <div class="workflow-title">Analyze</div>
                    <div style="font-size:0.72rem; color:#6B7280;">Stock Rules</div>
                </div>
            </div>
            <div class="workflow-arrow">→</div>
            <div class="workflow-node">
                <div class="workflow-icon">🖥️</div>
                <div>
                    <div class="workflow-title">Dashboard</div>
                    <div style="font-size:0.72rem; color:#6B7280;">KPIs & Alerts</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── 3. Five Mandatory Modules Section ─────────────────────
    st.markdown(
        "<div class='section-title'>📦 How the System Works</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p class='section-sub'>Five synchronized modules built for computer vision retail auditing.</p>",
        unsafe_allow_html=True,
    )

    modules_row1 = [
        {
            "num": "01",
            "icon": "📷",
            "title": "Shelf Image Acquisition",
            "desc": "Upload and prepare a shelf image using OpenCV preprocessing.",
        },
        {
            "num": "02",
            "icon": "🔲",
            "title": "Product Segmentation",
            "desc": "Locate products present on the shelf with YOLO bounding boxes.",
        },
        {
            "num": "03",
            "icon": "🏷️",
            "title": "Product Recognition",
            "desc": "Identify Coke, Pepsi, and Sprite with confidence scores.",
        },
    ]

    modules_row2 = [
        {
            "num": "04",
            "icon": "📊",
            "title": "Shelf Condition Analysis",
            "desc": "Classify stock as available (≥5), low (1-4), or out (0).",
        },
        {
            "num": "05",
            "icon": "🖥️",
            "title": "Monitoring Dashboard",
            "desc": "View counts, alerts, and executive stock summaries.",
        },
    ]

    # Row 1 (3 columns)
    r1_cols = st.columns(3)
    for col, m in zip(r1_cols, modules_row1):
        with col:
            st.markdown(
                f"""
                <div class="module-grid-card">
                    <div class="module-num-tag">{m['icon']} {m['num']}</div>
                    <div class="module-card-title">{m['title']}</div>
                    <p class="module-card-desc">{m['desc']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

    # Row 2 (2 columns)
    r2_cols = st.columns(2)
    for col, m in zip(r2_cols, modules_row2):
        with col:
            st.markdown(
                f"""
                <div class="module-grid-card">
                    <div class="module-num-tag">{m['icon']} {m['num']}</div>
                    <div class="module-card-title">{m['title']}</div>
                    <p class="module-card-desc">{m['desc']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<br/><br/>", unsafe_allow_html=True)
