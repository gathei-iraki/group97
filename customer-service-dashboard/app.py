import streamlit as st

st.set_page_config(
    page_title="Northstar Customer Support",
    page_icon="🛒",
    layout="centered"
)

st.title("Northstar Customer Support")

st.write(
    "Welcome to Northstar Retail Co. Self-Service Support."
)

st.write(
    "Choose an option below to get help with your order."
)

st.subheader("How can we help you today?")

order_status = st.button("Check Order Status")
returns = st.button("Returns & Refunds")

if order_status:
    st.info("Order Status service will be available here.")

if returns:
    st.info("Returns & Refunds service will be available here.")

st.divider()

st.caption(
    "If your issue cannot be resolved here, please contact Customer Support."
)