from datetime import date
from pathlib import Path

import streamlit as st

from return_rules import check_eligibility, find_order, refund_guidance


st.set_page_config(page_title="Returns & refunds | Northstar", page_icon="↩️")
css_path = Path(__file__).parents[1] / "styles.css"
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

st.title("Returns & refunds")
st.caption("Check eligibility, start a return, or understand the progress of a refund.")
st.info("MVP policy: standard items may be returned unused and in original packaging within 30 days of delivery. Final-sale items are excluded.")

task = st.radio(
    "What would you like to do?",
    [
        "Check eligibility or start a return",
        "Track a return or refund",
        "Report a damaged or incorrect item",
    ],
)

order_number = st.text_input(
    "Order number",
    placeholder="For example, NS-1001",
    help="Demo orders: NS-1001 to NS-1006. No email address is required.",
).strip()

if task == "Track a return or refund":
    if st.button("Check status", type="primary", use_container_width=True):
        order = find_order(order_number)
        if not order:
            st.error("We could not find that order number. Check it and try again. No status has been assumed.")
        else:
            result = refund_guidance(order, date.today())
            st.subheader(result["status"])
            st.write(result["message"])
            st.write(f"**Next step:** {result['next_step']}")
            if result["escalate"]:
                st.warning("Human help is recommended for this request.")
                st.link_button("Contact support", "mailto:support@northstar.com?subject=Refund%20help")
else:
    special_issue = task == "Report a damaged or incorrect item"
    reasons = ["Damaged item", "Wrong item received"] if special_issue else [
        "Changed my mind", "Wrong size", "No longer needed", "Damaged item", "Wrong item received"
    ]
    reason = st.selectbox("Reason for return", reasons)
    condition_ok = st.checkbox(
        "The item is unused, unworn and in its original packaging",
        disabled=reason in {"Damaged item", "Wrong item received"},
        help="This condition is not required for a damaged or incorrect item.",
    )
    if st.button("Check return", type="primary", use_container_width=True):
        order = find_order(order_number)
        if not order:
            st.error("We could not find that order number. Check it and try again.")
        else:
            result = check_eligibility(order, reason, condition_ok, date.today())
            st.session_state["return_result"] = result
            st.session_state["return_order"] = order.order_number
            st.session_state["return_item"] = order.item
            st.session_state["return_reason"] = reason

    result = st.session_state.get("return_result")
    if result and st.session_state.get("return_order") == order_number.upper():
        st.subheader(result["decision"])
        st.write(result["reason"])
        st.write(f"**Next step:** {result['next_step']}")
        if result["eligible"]:
            if st.button("Create return request", use_container_width=True):
                reference = f"RET-{order_number.upper().replace('NS-', '')}"
                st.session_state["created_return"] = reference
            if reference := st.session_state.get("created_return"):
                st.success(f"Return request created. Reference: {reference}")
                st.markdown(
                    f"""
                    1. Pack **{st.session_state['return_item']}** securely in its original packaging where possible.
                    2. Write return reference **{reference}** clearly on the parcel.
                    3. Use the return label Northstar supplies with the production service. Label generation is simulated in this MVP.
                    4. Keep proof of postage. After inspection, the refund goes to the original payment method and normally appears within **5–10 days**.
                    """
                )
        if result["escalate"]:
            st.warning("This request will need support-team review. Include the order number, item, reason and return reference if one was created.")
            st.link_button("Contact support", "mailto:support@northstar.com?subject=Return%20review")

with st.expander("Return and refund policy used by this MVP"):
    st.markdown(
        """
        - Return window: 30 days from delivery.
        - Standard condition: unused, unworn and in original packaging.
        - Final-sale items: not returnable unless damaged or incorrect.
        - Damaged or incorrect items: free-return specialist path.
        - Change-of-mind shipping cost: requires Northstar confirmation.
        - Refund destination: original payment method.
        - Refund timing: normally 5–10 days after inspection/issue.
        - Exchanges: not supported in the MVP; return and reorder.

        These are demonstration assumptions and must be approved by Northstar before launch.
        """
    )

