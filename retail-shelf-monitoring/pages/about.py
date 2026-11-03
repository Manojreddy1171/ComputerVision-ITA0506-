# ============================================================
#  About Page — Academic Capstone Architecture & Specifications
# ============================================================

import streamlit as st


def show_about():
    st.markdown(
        """
        <div>
            <h1 style='font-size:1.85rem; margin-bottom:4px;'>About the Project</h1>
            <p style='color:#6B7280; font-size:0.95rem; margin-top:0; margin-bottom:20px;'>
                Intelligent Retail Shelf Monitoring and Product Availability Detection System · ITA 0506
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── 1. Project Overview & Problem Statement ──────────────
    c1, c2 = st.columns(2, gap="medium")

    with c1:
        st.markdown(
            """
            <div class="clean-card" style='height:100%;'>
                <h3 style='font-size:1.1rem; color:#4F46E5; margin-top:0;'>📌 Problem Statement</h3>
                <p style='font-size:0.88rem; color:#374151; line-height:1.6;'>
                    Retail stores suffer significant revenue losses when shelves go out of stock undetected. Manual stock auditing is slow, labor-intensive, and prone to human counting errors.
                </p>
                <p style='font-size:0.88rem; color:#374151; line-height:1.6; margin-bottom:0;'>
                    Store managers need an automated, image-based solution that instantly flags low-stock conditions and identifies depleted items before customer churn occurs.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            """
            <div class="clean-card" style='height:100%;'>
                <h3 style='font-size:1.1rem; color:#4F46E5; margin-top:0;'>🎯 Objective</h3>
                <p style='font-size:0.88rem; color:#374151; line-height:1.6;'>
                    Design and implement an end-to-end Computer Vision web application that accepts retail shelf photos, detects and recognizes target beverage items using YOLO, and computes stock availability levels.
                </p>
                <p style='font-size:0.88rem; color:#374151; line-height:1.6; margin-bottom:0;'>
                    The system delivers actionable intelligence via executive KPI dashboards and restocking alerts, requiring no manual barcode scanning or counting.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

    # ── 2. Five Mandatory Modules ─────────────────────────────
    st.markdown("<div class='section-title'>📦 Five Mandatory Modules</div>", unsafe_allow_html=True)

    modules_data = [
        ("Module 1 — Shelf Image Acquisition", "📷", "Accepts JPG/PNG shelf photos. Validates image integrity, resizes oversized files, and applies OpenCV preprocessing (Gaussian noise filtering + CLAHE contrast enhancement)."),
        ("Module 2 — Product Segmentation / Detection", "🔲", "Runs Ultralytics YOLO to localize individual products with normalized bounding box coordinates and confidence scores."),
        ("Module 3 — Product Recognition", "🏷️", "Classifies each detected bounding box into target classes (Coke, Pepsi, Sprite). Aggregates per-product counts and computes mean class confidence."),
        ("Module 4 — Shelf Condition Analysis", "📊", "Evaluates detected counts against retail business thresholds: Available (≥5), Low Stock (1–4), and Out of Stock (0). Flags missing expected catalogue products."),
        ("Module 5 — Retail Monitoring Dashboard", "🖥️", "Renders real-time executive KPIs, color-coded product distribution bar charts, stock target progress bars, and restock alerts."),
    ]

    for title, icon, desc in modules_data:
        st.markdown(
            f"""
            <div class="clean-card" style='padding:14px 18px; margin-bottom:10px;'>
                <div style='display:flex; align-items:center; gap:8px;'>
                    <span style='font-size:1.2rem;'>{icon}</span>
                    <span style='font-size:0.95rem; font-weight:700; color:#111827;'>{title}</span>
                </div>
                <p style='font-size:0.85rem; color:#4B5563; margin:6px 0 0; line-height:1.5;'>{desc}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

    # ── 3. Tech Stack & Stock Rules ───────────────────────────
    ts_col1, ts_col2 = st.columns(2, gap="medium")

    with ts_col1:
        st.markdown(
            """
            <div class="clean-card" style='height:100%;'>
                <h3 style='font-size:1.1rem; color:#4F46E5; margin-top:0;'>🛠️ Technology Stack</h3>
                <table style='width:100%; font-size:0.85rem; line-height:2;'>
                    <tr><td style='color:#6B7280;'>Language</td><td style='font-weight:600;'>Python 3.10+</td></tr>
                    <tr><td style='color:#6B7280;'>Web Framework</td><td style='font-weight:600;'>Streamlit 1.32+</td></tr>
                    <tr><td style='color:#6B7280;'>Deep Learning</td><td style='font-weight:600;'>Ultralytics YOLOv8 / YOLO11</td></tr>
                    <tr><td style='color:#6B7280;'>Computer Vision</td><td style='font-weight:600;'>OpenCV (cv2)</td></tr>
                    <tr><td style='color:#6B7280;'>Visualizations</td><td style='font-weight:600;'>Plotly Express & Graph Objects</td></tr>
                    <tr><td style='color:#6B7280;'>Data Handling</td><td style='font-weight:600;'>Pandas & NumPy</td></tr>
                </table>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with ts_col2:
        st.markdown(
            """
            <div class="clean-card" style='height:100%;'>
                <h3 style='font-size:1.1rem; color:#4F46E5; margin-top:0;'>📏 Stock Classification Rules</h3>
                <div style='display:flex; flex-direction:column; gap:8px; margin-top:10px;'>
                    <div style='background:#ECFDF5; border:1px solid #A7F3D0; padding:10px 14px; border-radius:8px;'>
                        <b style='color:#065F46;'>Available (Count ≥ 5)</b><br/>
                        <span style='font-size:0.8rem; color:#047857;'>Shelf is sufficiently stocked. No replenishment needed.</span>
                    </div>
                    <div style='background:#FFFBEB; border:1px solid #FDE68A; padding:10px 14px; border-radius:8px;'>
                        <b style='color:#92400E;'>Low Stock (1 ≤ Count ≤ 4)</b><br/>
                        <span style='font-size:0.8rem; color:#B45309;'>Inventory is depleting. Restocking task scheduled.</span>
                    </div>
                    <div style='background:#FEF2F2; border:1px solid #FECACA; padding:10px 14px; border-radius:8px;'>
                        <b style='color:#991B1B;'>Out of Stock (Count = 0)</b><br/>
                        <span style='font-size:0.8rem; color:#B91C1C;'>Critical depletion. Urgent restocking alert dispatched.</span>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

    # ── 4. Limitations & Future Work ──────────────────────────
    st.markdown("<div class='section-title'>🚀 Limitations & Future Work</div>", unsafe_allow_html=True)

    lim_col1, lim_col2 = st.columns(2, gap="medium")

    with lim_col1:
        st.markdown(
            """
            <div class="clean-card" style='height:100%;'>
                <h4 style='font-size:0.95rem; color:#111827; margin-top:0;'>Current Limitations</h4>
                <ul style='font-size:0.84rem; color:#4B5563; line-height:1.7; padding-left:18px;'>
                    <li>Operates on still photographs rather than continuous RTSP CCTV stream.</li>
                    <li>Detection accuracy is bound to product brands in the training set (Coke, Pepsi, Sprite).</li>
                    <li>Heavily occluded items behind front-facing rows are partially hidden from 2D camera view.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with lim_col2:
        st.markdown(
            """
            <div class="clean-card" style='height:100%;'>
                <h4 style='font-size:0.95rem; color:#111827; margin-top:0;'>Future Enhancements</h4>
                <ul style='font-size:0.84rem; color:#4B5563; line-height:1.7; padding-left:18px;'>
                    <li>Live RTSP supermarket IP camera video stream ingestion.</li>
                    <li>Planogram compliance verification (spatial x,y slot alignment).</li>
                    <li>Automated ERP purchase order generation on stock-out events.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
