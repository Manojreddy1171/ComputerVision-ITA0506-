# ============================================================
#  Shelf Analysis Page — Complete Computer Vision Pipeline
# ============================================================

import streamlit as st
import pandas as pd
import time
from pathlib import Path
from PIL import Image

# ─── Local Utilities ──────────────────────────────────────────
from utils.image_processing import (
    validate_image_format,
    full_pipeline,
    bgr_to_rgb_pil,
)
from utils.detection import (
    load_model,
    run_detection,
    draw_detections,
    aggregate_detections,
    get_expected_classes,
)
from utils.shelf_analysis import (
    analyse_shelf,
    generate_alerts,
    compute_kpis,
    StockStatus,
)

DEFAULT_CONF = 0.25


# ─── Model Caching (Zero arguments = cached once in memory) ──
@st.cache_resource(show_spinner="Loading YOLO detection model…")
def get_cached_model():
    return load_model()


def _request_dashboard():
    """Safe navigation callback to Dashboard."""
    st.session_state["nav_request"] = "📊 Dashboard"


def _reset_shelf_state():
    """Reset all current shelf analysis keys."""
    for key in [
        "detections", "aggregated", "analyses", "alerts", "kpis",
        "annotated_pil", "orig_pil", "image_info", "active_file_sig"
    ]:
        st.session_state.pop(key, None)


def show_shelf_analysis():
    st.markdown(
        """
        <div>
            <h1 style='font-size:1.85rem; margin-bottom:4px;'>Analyze Retail Shelf</h1>
            <p style='color:#6B7280; font-size:0.95rem; margin-top:0; margin-bottom:20px;'>
                Upload a shelf photograph and run the complete AI analysis pipeline.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Model Status Notification Banner ──────────────────────
    try:
        model = get_cached_model()
    except Exception as exc:
        st.error(f"Unable to load YOLO model: {exc}")
        return

    source = getattr(model, "_source", "demo")
    expected_classes = get_expected_classes(model)

    if source == "custom":
        st.markdown(
            f"""
            <div style='background:#ECFDF5; border:1px solid #A7F3D0; border-radius:10px; padding:10px 16px; margin-bottom:18px; display:flex; justify-content:space-between; align-items:center;'>
                <span style='color:#065F46; font-size:0.86rem; font-weight:600;'>
                    🎯 <b>Custom Retail Model Active</b> (models/best.pt) — Tracking: <b>{', '.join(expected_classes)}</b>
                </span>
                <span class='status-badge-saas status-available'>Custom Weights</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div style='background:#FFFBEB; border:1px solid #FDE68A; border-radius:10px; padding:10px 16px; margin-bottom:18px; display:flex; justify-content:space-between; align-items:center;'>
                <span style='color:#92400E; font-size:0.86rem; font-weight:600;'>
                    💡 <b>Demo Mode Active</b> (Pretrained YOLOv8n COCO weights) — Tracking: <b>{', '.join(expected_classes)}</b>
                </span>
                <span class='status-badge-saas status-low'>Pretrained</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ════════════════════════════════════════════════════════
    #  STEP 1 — Image Acquisition & Upload Card
    # ════════════════════════════════════════════════════════
    st.markdown("<div class='section-title'>📷 Step 1: Upload Shelf Photograph</div>", unsafe_allow_html=True)

    project_root = Path(__file__).resolve().parent.parent
    sample_dir = project_root / "samples"
    if not sample_dir.exists() or not any(sample_dir.glob("*.jp*g")):
        sample_dir = project_root / "data" / "sample_images"
    sample_files = sorted(list(sample_dir.glob("*.jpg")) + list(sample_dir.glob("*.png")) + list(sample_dir.glob("*.jpeg")), key=lambda p: p.name)
    sample_options = ["-- Upload Custom Image --"] + [f.name for f in sample_files]

    upload_col1, upload_col2 = st.columns([1.5, 1], gap="medium")

    with upload_col1:
        selected_sample = None
        if len(sample_files) > 0:
            selected_sample = st.selectbox(
                "Choose from pre-loaded sample shelf tests:",
                options=sample_options,
                index=0,
                key="sample_shelf_selector"
            )

        uploaded_file = st.file_uploader(
            "Or upload local shelf photo (JPG / JPEG / PNG):",
            type=["jpg", "jpeg", "png"],
            key="shelf_file_uploader",
        )

    # Resolve file bytes & filename safely
    file_bytes = None
    filename = None

    if uploaded_file is not None:
        filename = uploaded_file.name
        file_bytes = uploaded_file.getvalue()
    elif selected_sample and selected_sample != "-- Upload Custom Image --":
        sample_path = sample_dir / selected_sample
        if sample_path.exists():
            filename = selected_sample
            with open(sample_path, "rb") as f:
                file_bytes = f.read()

    img_bgr = None
    image_info = None

    if file_bytes is not None and filename is not None:
        # Check if new file was uploaded to invalidate stale analysis
        file_sig = f"{filename}_{len(file_bytes)}"
        if st.session_state.get("active_file_sig") != file_sig:
            for k in ["detections", "aggregated", "analyses", "alerts", "kpis", "annotated_pil"]:
                st.session_state.pop(k, None)
            st.session_state["active_file_sig"] = file_sig

        if not validate_image_format(filename):
            st.error("Invalid image format. Please upload a JPG, JPEG, or PNG file.")
        else:
            try:
                img_bgr, image_info = full_pipeline(file_bytes, filename)
            except Exception as exc:
                st.error(f"Error reading image: {exc}")
                img_bgr = None

    with upload_col2:
        if image_info:
            st.markdown(
                f"""
                <div class="clean-card" style='padding:16px 18px;'>
                    <div style='font-size:0.75rem; font-weight:700; color:#4F46E5; text-transform:uppercase; margin-bottom:8px;'>
                        IMAGE METADATA
                    </div>
                    <table style='width:100%; font-size:0.83rem; line-height:1.9;'>
                        <tr>
                            <td style='color:#6B7280;'>File</td>
                            <td style='font-weight:600; text-align:right;'>{image_info['filename']}</td>
                        </tr>
                        <tr>
                            <td style='color:#6B7280;'>Resolution</td>
                            <td style='font-weight:600; text-align:right;'>{image_info['width']} × {image_info['height']} px</td>
                        </tr>
                        <tr>
                            <td style='color:#6B7280;'>File Size</td>
                            <td style='font-weight:600; text-align:right;'>{image_info['size_kb']} KB</td>
                        </tr>
                        <tr>
                            <td style='color:#6B7280;'>Preprocessing</td>
                            <td style='color:#10B981; font-weight:600; text-align:right;'>Gaussian Blur + CLAHE</td>
                        </tr>
                    </table>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                """
                <div class="clean-card" style='padding:24px; text-align:center; color:#6B7280; font-size:0.85rem;'>
                    Upload an image or pick a sample from the list to preview metadata.
                </div>
                """,
                unsafe_allow_html=True,
            )

    if img_bgr is None:
        st.info("Upload a retail shelf photograph above to begin analysis.")
        return

    # ════════════════════════════════════════════════════════
    #  STEP 2 — Constrained Original Image Display
    # ════════════════════════════════════════════════════════
    st.markdown("<div class='section-title'>🖼️ Step 2: Uploaded Shelf Image</div>", unsafe_allow_html=True)
    orig_pil = bgr_to_rgb_pil(img_bgr)

    # Use constrained column to avoid extreme width stretching
    img_preview_col, _ = st.columns([2, 1])
    with img_preview_col:
        st.image(orig_pil, use_container_width=True, caption="Source shelf photograph (OpenCV preprocessed)")

    # ════════════════════════════════════════════════════════
    #  STEP 3 — Analysis Controls
    # ════════════════════════════════════════════════════════
    st.markdown("<div class='section-title'>⚙️ Step 3: Analysis Controls</div>", unsafe_allow_html=True)

    ctrl_col1, ctrl_col2, ctrl_col3 = st.columns([1.2, 1, 2], gap="medium")

    with ctrl_col1:
        conf_slider = st.slider(
            "Confidence Threshold",
            min_value=0.10,
            max_value=0.90,
            value=DEFAULT_CONF,
            step=0.05,
            help="Minimum confidence required for a detection box."
        )

    with ctrl_col2:
        st.write("")  # vertical spacing
        analyse_clicked = st.button(
            "⚡ Run Shelf Analysis",
            type="primary",
            use_container_width=True,
            key="run_analysis_primary_btn",
        )

    with ctrl_col3:
        st.write("")
        st.button(
            "🗑️ Reset All",
            type="secondary",
            on_click=_reset_shelf_state,
            key="reset_shelf_btn",
        )

    # ════════════════════════════════════════════════════════
    #  PIPELINE EXECUTION
    # ════════════════════════════════════════════════════════
    if analyse_clicked:
        with st.spinner("Running YOLO Product Detection and Condition Analysis…"):
            time.sleep(0.15)
            try:
                # 1. Product Detection (Module 2)
                detections = run_detection(model, img_bgr, conf_threshold=conf_slider)
                annotated_bgr = draw_detections(img_bgr, detections)
                annotated_pil = bgr_to_rgb_pil(annotated_bgr)

                # 2. Product Aggregation (Module 3)
                aggregated = aggregate_detections(detections)

                # 3. Condition Analysis (Module 4)
                analyses = analyse_shelf(aggregated, all_tracked_classes=expected_classes)
                alerts = generate_alerts(analyses)
                kpis = compute_kpis(analyses, total_detected=len(detections))

                # Persist state for Dashboard
                st.session_state["detections"] = detections
                st.session_state["aggregated"] = aggregated
                st.session_state["analyses"] = analyses
                st.session_state["alerts"] = alerts
                st.session_state["kpis"] = kpis
                st.session_state["annotated_pil"] = annotated_pil
                st.session_state["orig_pil"] = orig_pil
                st.session_state["image_info"] = image_info
                st.session_state["last_conf_used"] = conf_slider

                st.success("Shelf analysis completed successfully. Results updated below.")
            except Exception as exc:
                st.error(f"Error during inference: {exc}")

    # Render results if available for current image
    if "analyses" in st.session_state:
        _render_shelf_results()


def _render_shelf_results():
    detections = st.session_state["detections"]
    analyses = st.session_state["analyses"]
    alerts = st.session_state["alerts"]
    kpis = st.session_state["kpis"]
    annotated_pil = st.session_state["annotated_pil"]

    st.markdown("<hr style='border-color:#E2E8F0; margin:28px 0;'/>", unsafe_allow_html=True)

    # ════════════════════════════════════════════════════════
    #  STEP 4 — Product Detection (Module 2)
    # ════════════════════════════════════════════════════════
    st.markdown("<div class='section-title'>🔲 Step 4: Product Detection (YOLO Bounding Boxes)</div>", unsafe_allow_html=True)

    # Clean KPI summary row
    kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
    with kpi_col1:
        st.markdown(
            f"""
            <div class="kpi-card-saas">
                <div class="kpi-label-saas">Detected Items</div>
                <div class="kpi-val-saas" style="color:#4F46E5;">{len(detections)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with kpi_col2:
        avg_conf = (
            sum(d["confidence"] for d in detections) / len(detections) * 100
            if len(detections) > 0 else 0
        )
        st.markdown(
            f"""
            <div class="kpi-card-saas">
                <div class="kpi-label-saas">Average Confidence</div>
                <div class="kpi-val-saas" style="color:#10B981;">{avg_conf:.1f}%</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with kpi_col3:
        unique_classes = len(set(d["class_name"] for d in detections))
        st.markdown(
            f"""
            <div class="kpi-card-saas">
                <div class="kpi-label-saas">Detected Classes</div>
                <div class="kpi-val-saas" style="color:#6366F1;">{unique_classes}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

    det_col_left, det_col_right = st.columns([1.4, 1], gap="medium")
    with det_col_left:
        st.image(annotated_pil, use_container_width=True, caption="YOLO bounding boxes and recognized labels")

    with det_col_right:
        if detections:
            st.markdown("<div style='font-size:0.85rem; font-weight:700; margin-bottom:6px;'>Detection Bbox Log</div>", unsafe_allow_html=True)
            det_rows = [
                {
                    "Product": d["class_name"],
                    "Confidence": f"{d['confidence']*100:.1f}%",
                    "Bounding Box (x1,y1,x2,y2)": str(d["bbox"]),
                }
                for d in detections
            ]
            st.dataframe(pd.DataFrame(det_rows), use_container_width=True, hide_index=True)
        else:
            st.warning("No supported products were detected at this confidence threshold.")

    # ════════════════════════════════════════════════════════
    #  STEP 5 — Product Recognition (Module 3)
    # ════════════════════════════════════════════════════════
    st.markdown("<div class='section-title'>🏷️ Step 5: Product Recognition & Quantities</div>", unsafe_allow_html=True)

    recog_rows = []
    for pa in analyses:
        recog_rows.append({
            "Product": pa.product_name,
            "Count": pa.count,
            "Confidence": (
                f"{pa.avg_confidence*100:.1f}%"
                if pa.avg_confidence is not None else "—"
            ),
            "Stock Condition": pa.status,
        })
    st.dataframe(pd.DataFrame(recog_rows), use_container_width=True, hide_index=True)

    # ════════════════════════════════════════════════════════
    #  STEP 6 — Shelf Condition Analysis (Module 4)
    # ════════════════════════════════════════════════════════
    st.markdown("<div class='section-title'>📊 Step 6: Shelf Condition Analysis</div>", unsafe_allow_html=True)

    card_cols = st.columns(len(analyses)) if analyses else []
    for col, pa in zip(card_cols, analyses):
        if pa.status == StockStatus.AVAILABLE:
            badge_class = "status-available"
            border_class = "pcard-avail"
            badge_text = "Available"
        elif pa.status == StockStatus.LOW_STOCK:
            badge_class = "status-low"
            border_class = "pcard-low"
            badge_text = "Low Stock"
        else:
            badge_class = "status-out"
            border_class = "pcard-out"
            badge_text = "Out of Stock"

        with col:
            st.markdown(
                f"""
                <div class="product-condition-card {border_class}">
                    <div style="font-size:0.8rem; font-weight:700; color:#6B7280; text-transform:uppercase;">
                        {pa.product_name}
                    </div>
                    <div style="font-size:2.2rem; font-weight:800; font-family:Poppins,sans-serif; color:#111827; margin:4px 0;">
                        {pa.count}
                    </div>
                    <div style="font-size:0.75rem; color:#6B7280; margin-bottom:8px;">
                        items on shelf
                    </div>
                    <span class="status-badge-saas {badge_class}">
                        {badge_text}
                    </span>
                    <div style="margin-top:10px; font-size:0.72rem; color:#94A3B8;">
                        Target: 5 units ({pa.availability_pct:.0f}%)
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # Restock Alerts
    if alerts:
        st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)
        for alert in alerts:
            if "out of stock" in alert.lower():
                st.error(alert)
            else:
                st.warning(alert)

    # Navigation CTA to Dashboard using safe on_click pattern
    st.markdown("<br/>", unsafe_allow_html=True)
    c_btn, _ = st.columns([1.5, 3])
    with c_btn:
        st.button(
            "📊 Open Monitoring Dashboard",
            type="primary",
            use_container_width=True,
            on_click=_request_dashboard,
            key="analysis_to_dashboard_btn",
        )
