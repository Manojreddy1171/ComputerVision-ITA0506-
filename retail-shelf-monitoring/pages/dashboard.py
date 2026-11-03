# ============================================================
#  Module 5 — Retail Monitoring Dashboard (Modern SaaS Style)
# ============================================================

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.shelf_analysis import StockStatus


def _request_analysis():
    """Safe navigation callback to Shelf Analysis."""
    st.session_state["nav_request"] = "🔍 Shelf Analysis"


def show_dashboard():
    st.markdown(
        """
        <div>
            <h1 style='font-size:1.85rem; margin-bottom:4px;'>Retail Monitoring Dashboard</h1>
            <p style='color:#6B7280; font-size:0.95rem; margin-top:0; margin-bottom:20px;'>
                Real-time inventory overview, stock status breakdown, and automated replenishment alerts.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Guard: Empty State Check ──────────────────────────────
    if "analyses" not in st.session_state or not st.session_state.get("analyses"):
        st.markdown(
            """
            <div class="clean-card" style='text-align:center; padding:48px 24px; margin-top:10px;'>
                <div style='font-size:3rem; margin-bottom:12px;'>📊</div>
                <h3 style='font-family:Poppins,sans-serif; margin:0 0 8px;'>No Active Shelf Data</h3>
                <p style='color:#6B7280; font-size:0.92rem; max-width:480px; margin:0 auto 20px;'>
                    Upload and analyze a retail shelf photograph to populate the executive dashboard with real-time product counts and condition metrics.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        c1, c2, c3 = st.columns([1.5, 1, 1.5])
        with c2:
            st.button(
                "🚀 Analyze a Shelf",
                type="primary",
                on_click=_request_analysis,
                key="empty_dash_to_analysis_btn",
                use_container_width=True,
            )
        return

    analyses = st.session_state["analyses"]
    kpis     = st.session_state["kpis"]
    alerts   = st.session_state["alerts"]

    # ── 1. Top Row: 5 Clean SaaS KPI Cards ────────────────────
    st.markdown("<div class='section-title'>📌 Key Performance Indicators</div>", unsafe_allow_html=True)

    k1, k2, k3, k4, k5 = st.columns(5)

    with k1:
        st.markdown(
            f"""
            <div class="kpi-card-saas">
                <div class="kpi-label-saas">Total Items</div>
                <div class="kpi-val-saas" style="color:#4F46E5;">{kpis['total_items']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with k2:
        st.markdown(
            f"""
            <div class="kpi-card-saas">
                <div class="kpi-label-saas">Product Categories</div>
                <div class="kpi-val-saas" style="color:#6366F1;">{kpis['total_categories']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with k3:
        st.markdown(
            f"""
            <div class="kpi-card-saas">
                <div class="kpi-label-saas">Available (≥5)</div>
                <div class="kpi-val-saas" style="color:#10B981;">{kpis['available_count']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with k4:
        st.markdown(
            f"""
            <div class="kpi-card-saas">
                <div class="kpi-label-saas">Low Stock (1–4)</div>
                <div class="kpi-val-saas" style="color:#F59E0B;">{kpis['low_stock_count']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with k5:
        st.markdown(
            f"""
            <div class="kpi-card-saas">
                <div class="kpi-label-saas">Out of Stock (0)</div>
                <div class="kpi-val-saas" style="color:#EF4444;">{kpis['out_of_stock_count']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ── 2. Urgent Restock Alerts ──────────────────────────────
    if alerts:
        st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)
        for alert in alerts:
            if "out of stock" in alert.lower():
                st.error(alert)
            else:
                st.warning(alert)

    st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)

    # ── 3. Main Analytics Area (Two Columns) ──────────────────
    chart_col, summary_col = st.columns([1.4, 1], gap="medium")

    with chart_col:
        st.markdown("<div class='section-title'>📊 Product Quantities</div>", unsafe_allow_html=True)

        products = [pa.product_name for pa in analyses]
        counts   = [pa.count for pa in analyses]
        statuses = [pa.status for pa in analyses]

        color_map = {
            StockStatus.AVAILABLE   : "#10B981",  # Emerald
            StockStatus.LOW_STOCK   : "#F59E0B",  # Amber
            StockStatus.OUT_OF_STOCK: "#EF4444",  # Red
        }
        bar_colors = [color_map.get(s, "#4F46E5") for s in statuses]

        fig = go.Figure(
            go.Bar(
                x=products,
                y=counts,
                marker_color=bar_colors,
                text=counts,
                textposition="outside",
                textfont=dict(family="Inter", size=13, color="#111827"),
                hoverinfo="x+y",
            )
        )
        max_y = max(counts) if counts and max(counts) > 5 else 6
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=25, b=20, l=10, r=10),
            xaxis=dict(
                tickfont=dict(family="Inter", size=13, color="#111827"),
                showgrid=False,
                zeroline=False,
            ),
            yaxis=dict(
                tickfont=dict(family="Inter", size=12, color="#64748B"),
                gridcolor="#F1F5F9",
                zeroline=False,
                title="Units Detected",
                range=[0, max_y + 1],
            ),
            showlegend=False,
            height=300,
        )
        st.plotly_chart(fig, use_container_width=True)

    with summary_col:
        st.markdown("<div class='section-title'>📈 Stock Target Progress</div>", unsafe_allow_html=True)
        st.markdown(
            "<div style='font-size:0.8rem; color:#6B7280; margin-top:-6px; margin-bottom:12px;'>Target: 5 units per product</div>",
            unsafe_allow_html=True,
        )

        for pa in analyses:
            pct = pa.availability_pct / 100.0
            if pa.status == StockStatus.AVAILABLE:
                badge_html = "<span class='status-badge-saas status-available'>Available</span>"
            elif pa.status == StockStatus.LOW_STOCK:
                badge_html = "<span class='status-badge-saas status-low'>Low Stock</span>"
            else:
                badge_html = "<span class='status-badge-saas status-out'>Out of Stock</span>"

            st.markdown(
                f"""
                <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;'>
                    <span style='font-size:0.86rem; font-weight:600;'>{pa.product_name}</span>
                    {badge_html}
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.progress(pct)
            st.markdown(
                f"<div style='font-size:0.75rem; color:#64748B; margin-bottom:12px;'>{pa.count} of 5 units on shelf ({pa.availability_pct:.0f}%)</div>",
                unsafe_allow_html=True,
            )

    st.markdown("<hr style='border-color:#E2E8F0; margin:24px 0;'/>", unsafe_allow_html=True)

    # ── 4. Detailed Product Availability Table ────────────────
    st.markdown("<div class='section-title'>📋 Product Availability Breakdown</div>", unsafe_allow_html=True)

    rows = []
    for pa in analyses:
        rows.append({
            "Product": pa.product_name,
            "Count": pa.count,
            "Confidence": (
                f"{pa.avg_confidence*100:.1f}%"
                if pa.avg_confidence is not None else "—"
            ),
            "Target Stock %": f"{pa.availability_pct:.0f}%",
            "Condition": pa.status,
        })
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    # ── 5. Visual Verification ────────────────────────────────
    if "annotated_pil" in st.session_state:
        st.markdown("<div class='section-title'>🖼️ Visual Shelf Verification</div>", unsafe_allow_html=True)
        img_col, _ = st.columns([1.8, 1])
        with img_col:
            st.image(
                st.session_state["annotated_pil"],
                use_container_width=True,
                caption="Current shelf photo analyzed with YOLO localized bounding boxes",
            )
