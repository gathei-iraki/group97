# pages/order_status.py
import streamlit as st
import random
from datetime import datetime, timedelta
from pathlib import Path

# --- Page Configuration ---
st.set_page_config(
    page_title="Order Status - Northstar Support",
    page_icon=":material/local_shipping:",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# --- Load Global Styles ---
try:
    css_path = Path(__file__).parent.parent / "styles.css"
    if css_path.exists():
        st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)
except Exception as e:
    st.warning(f"⚠️ Could not load stylesheet: {str(e)}")

# --- Back Navigation ---
st.markdown(
    """
    <div class="back-link">
        <a href="/">
            <span class="material-symbols-rounded">arrow_back</span>
            Back to Home
        </a>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- Page Header ---
st.markdown(
    """
    <div class="main-header order-header">
        <div class="header-icon">
            <span class="material-symbols-rounded">local_shipping</span>
            <h1>Check Order Status</h1>
        </div>
    </div>
    <p class="subtitle order-subtitle">
        Enter your order number to track your package and see the latest delivery updates.
    </p>
    """,
    unsafe_allow_html=True,
)

# --- Helper Functions ---
def generate_mock_order_status(order_id):
    """
    Simulates fetching order status from a database or API.
    Each call generates a RANDOM status independently.
    """
    # IMPORTANT: Random choice is called HERE for EACH order
    # This ensures different orders get different statuses
    statuses = ["Processing", "Shipped", "Out for Delivery", "Delivered"]
    status = random.choice(statuses)  # <-- THIS MUST BE INSIDE THE FUNCTION
    
    today = datetime.now()
    
    if status == "Processing":
        order_date = today - timedelta(days=random.randint(1, 3))
        est_delivery = today + timedelta(days=random.randint(3, 7))
        tracking = None
    elif status == "Shipped":
        order_date = today - timedelta(days=random.randint(3, 6))
        est_delivery = today + timedelta(days=random.randint(1, 4))
        tracking = f"1Z{random.randint(100, 999)}AA{random.randint(10000000, 99999999)}"
    elif status == "Out for Delivery":
        order_date = today - timedelta(days=random.randint(5, 9))
        est_delivery = today
        tracking = f"1Z{random.randint(100, 999)}AA{random.randint(10000000, 99999999)}"
    else:  # Delivered
        order_date = today - timedelta(days=random.randint(8, 15))
        est_delivery = today - timedelta(days=random.randint(1, 5))
        tracking = f"1Z{random.randint(100, 999)}AA{random.randint(10000000, 99999999)}"
    
    # Generate order history
    history = [
        {"status": "Order Placed", "date": order_date.strftime("%Y-%m-%d")},
        {"status": "Processing Started", "date": (order_date + timedelta(days=1)).strftime("%Y-%m-%d")},
    ]
    
    if status in ["Shipped", "Out for Delivery", "Delivered"]:
        history.append({"status": "Shipped", "date": (order_date + timedelta(days=random.randint(2, 4))).strftime("%Y-%m-%d")})
    
    if status in ["Out for Delivery", "Delivered"]:
        history.append({"status": "Out for Delivery", "date": (order_date + timedelta(days=random.randint(5, 7))).strftime("%Y-%m-%d")})
    
    if status == "Delivered":
        history.append({"status": "Delivered", "date": (order_date + timedelta(days=random.randint(8, 10))).strftime("%Y-%m-%d")})
    
    # Ensure consistent return type: estimated_delivery is always a string date or "Delivered"
    if status == "Delivered":
        estimated_delivery_str = "Delivered"
    else:
        estimated_delivery_str = est_delivery.strftime("%Y-%m-%d") if isinstance(est_delivery, datetime) else "Delivered"
    
    return {
        "order_id": order_id,
        "status": status,
        "order_date": order_date.strftime("%Y-%m-%d"),
        "estimated_delivery": estimated_delivery_str,
        "tracking_number": tracking,
        "history": history,
    }

# --- Input Form ---
with st.container():
    st.markdown('<div class="support-card form-container">', unsafe_allow_html=True)
    
    submitted = False
    clear_clicked = False
    
    with st.form(key="order_status_form", clear_on_submit=False):
        order_id = st.text_input(
            "Order Number",
            placeholder="e.g., ORD-12345 or #12345",
            help="Enter the order number from your confirmation email.",
            label_visibility="collapsed",
            max_chars=12,
        )
        
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            submitted = st.form_submit_button(
                "🔍 Check Status",
                type="primary",
                use_container_width=True,
            )
        with col2:
            clear_clicked = st.form_submit_button("Clear", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- Clear Form Handler ---
if clear_clicked:
    st.rerun()

# --- Main Logic ---
if submitted:
    if not order_id or not order_id.strip():
        st.error("⚠️ Please enter an order number.")
    elif len(order_id.strip()) < 3:
        st.warning("⚠️ Please enter a valid order number (at least 3 characters).")
    elif len(order_id.strip()) > 12:
        st.warning("⚠️ Please enter a valid order number (maximum 12 characters).")
    else:
        try:
            with st.spinner("Looking up your order..."):
                order_data = generate_mock_order_status(order_id.strip())
            
            # --- Success: Display Results ---
            st.success(f"✅ Order found for {order_data['order_id']}!")
            
            # Status with appropriate styling
            status = order_data["status"]
            status_colors = {
                "Processing": ("🔄", "#d69e2e", "Your order is being prepared for shipment."),
                "Shipped": ("🚚", "#2b6cb0", f"Tracking Number: `{order_data['tracking_number']}`"),
                "Out for Delivery": ("🚀", "#38a169", "📬 Your order is out for delivery today!"),
                "Delivered": ("✅", "#38a169", "🎉 Your order has been delivered."),
            }
            icon, color, message = status_colors.get(status, ("📦", "#667085", ""))
            
            st.markdown(
                f"""
                <div class="status-badge" style="--status-color: {color}; background: {color}10; border-color: {color};">
                    <span class="status-icon">{icon}</span>
                    <div class="status-content">
                        <div class="status-title" style="color: {color};">
                            Current Status: {status}
                        </div>
                        <div class="status-message">{message}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            
            # --- Order Details Grid ---
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📋 Order Number", order_data["order_id"])
            with col2:
                st.metric("📅 Order Date", order_data["order_date"])
            with col3:
                delivery_display = order_data["estimated_delivery"]
                if delivery_display == "Delivered":
                    st.metric("✅ Delivery Status", "Delivered")
                else:
                    st.metric("📦 Estimated Delivery", delivery_display)
            
            # Tracking Number (if available)
            if order_data["tracking_number"]:
                st.info(f"📮 **Tracking Number:** `{order_data['tracking_number']}`")
            
            # --- Order Timeline ---
            with st.expander("📜 View Order Timeline", expanded=False):
                for event in order_data["history"]:
                    st.markdown(
                        f"""
                        <div class="timeline-event">
                            <span class="timeline-event-status">{event['status']}</span>
                            <span class="timeline-event-date">{event['date']}</span>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
            
            # --- Help Section ---
            st.divider()
            st.markdown(
                """
                <div class="help-section">
                    <h3>❓ Need More Help?</h3>
                    <p>If you have questions about your order or need further assistance, our support team is here for you.</p>
                    <div class="support-buttons">
                        <a href="mailto:support@northstar.com" class="support-button email">
                            <span class="material-symbols-rounded">mail</span>
                            Email Support
                        </a>
                        <a href="tel:+254-735-0199" class="support-button phone">
                            <span class="material-symbols-rounded">call</span>
                            Call Us
                        </a>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        except Exception as e:
            st.error(f"❌ Error retrieving order status: {str(e)}")
            st.info("Please try again later or contact our support team.")

# --- Footer ---
st.divider()
st.markdown(
    """
    <div class="footer-text">
        <p>
            <span class="material-symbols-rounded inline-icon" aria-hidden="true">schedule</span>
            Support available 24/7 &nbsp;|&nbsp;
            <span class="material-symbols-rounded inline-icon" aria-hidden="true">chat</span>
            <a href="/">Return to Home</a>
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