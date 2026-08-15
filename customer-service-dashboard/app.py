# app.py
from pathlib import Path

import streamlit as st


st.set_page_config(
    page_title="Northstar Customer Support",
    page_icon=":material/support_agent:",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# --- Load Global Styles ---
try:
    css_path = Path(__file__).with_name("styles.css")
    if css_path.exists():
        st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)
except Exception as e:
    st.warning(f"Could not load stylesheet: {str(e)}", icon=":material/warning:")

st.markdown(
    """
    <div class="main-header">
        <div class="header-icon" aria-hidden="true">
            <span class="material-symbols-rounded">support_agent</span>
        </div>
        <h1>Northstar Customer Support</h1>
    </div>
    <p class="subtitle">
        Welcome to Northstar Retail Co. Self-Service Support.<br>
        We're here to help you find answers, fast.
    </p>
    <div class="section-heading">
        <h2>What can we help with?</h2>
        <p>Choose a service to get started. Most requests take less than two minutes.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ==================== COLUMN 1: Order Status ====================
col1, col2 = st.columns(2, gap="medium")

with col1:
    # Card content (HTML for styling only)
    st.markdown(
        """
        <div class="support-card">
            <span class="card-icon material-symbols-rounded" aria-hidden="true">local_shipping</span>
            <div class="card-title">Check order status</div>
            <div class="card-desc">Track your package and see the latest delivery updates.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    if st.button(
        "Track my order",
        key="track_order",
        icon=":material/local_shipping:",
        use_container_width=True,
    ):
        st.switch_page("pages/order_status.py")

# ==================== COLUMN 2: Returns & Refunds ====================
with col2:
    st.markdown(
        """
        <div class="support-card">
            <span class="card-icon material-symbols-rounded" aria-hidden="true">assignment_return</span>
            <div class="card-title">Returns & refunds</div>
            <div class="card-desc">Start a return or check the progress of your refund.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button(
        "Manage a return",
        key="manage_return",
        icon=":material/assignment_return:",
        use_container_width=True,
    ):
        st.switch_page("pages/returns_refunds.py")

# ==================== Footer ====================
st.markdown(
    """
    <div class="footer-divider"></div>
    <div class="footer-text">
        <p>Can't find what you need? We're here to help.</p>
        <p>
            <span class="material-symbols-rounded inline-icon" aria-hidden="true">mail</span>
            <a href="mailto:support@northstar.com">support@northstar.com</a> &nbsp;|&nbsp;
            <span class="material-symbols-rounded inline-icon" aria-hidden="true">call</span>
            <a href="tel:+254-735-0199">+254-735-0199</a>
        </p>
        <div class="quick-links">
            <span class="quick-link">Privacy Policy</span>
            <span class="quick-link">Terms of Service</span>
            <span class="quick-link">Accessibility</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
