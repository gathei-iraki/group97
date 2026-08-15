"""Return/refund rules and mock data for the Northstar MVP.

The policy values in this module are assumptions for demonstration. Northstar
must approve them before launch and replace the mock records with live data.
"""

from dataclasses import dataclass
from datetime import date


RETURN_WINDOW_DAYS = 30
REFUND_MIN_DAYS = 5
REFUND_MAX_DAYS = 10


@dataclass(frozen=True)
class Order:
    order_number: str
    item: str
    delivered_on: date
    final_sale: bool = False
    return_status: str = "Not started"
    refund_issued_on: date | None = None


MOCK_ORDERS = {
    "NS-1001": Order("NS-1001", "Everyday trainers", date(2026, 8, 8)),
    "NS-1002": Order("NS-1002", "Final-sale jacket", date(2026, 8, 10), final_sale=True),
    "NS-1003": Order("NS-1003", "Classic backpack", date(2026, 6, 20)),
    "NS-1004": Order(
        "NS-1004",
        "Linen shirt",
        date(2026, 7, 24),
        return_status="Refund issued",
        refund_issued_on=date(2026, 8, 12),
    ),
    "NS-1005": Order(
        "NS-1005", "Running shorts", date(2026, 7, 18), return_status="Under inspection"
    ),
    "NS-1006": Order(
        "NS-1006",
        "Canvas tote",
        date(2026, 7, 10),
        return_status="Refund issued",
        refund_issued_on=date(2026, 7, 24),
    ),
}


def find_order(order_number: str) -> Order | None:
    """Look up an order without collecting an email address."""
    return MOCK_ORDERS.get(order_number.strip().upper())


def check_eligibility(
    order: Order,
    reason: str,
    unused_and_packaged: bool,
    today: date,
) -> dict[str, str | bool]:
    """Return an explainable decision and the customer's next action."""
    if reason in {"Damaged item", "Wrong item received"}:
        return {
            "eligible": True,
            "decision": "Specialist return available",
            "reason": "Damaged and incorrect items use Northstar's free-return process.",
            "next_step": "Create the request below. Keep the item and packaging for review.",
            "escalate": True,
        }

    days_since_delivery = (today - order.delivered_on).days
    if days_since_delivery > RETURN_WINDOW_DAYS:
        return {
            "eligible": False,
            "decision": "Outside the standard return window",
            "reason": f"This order was delivered {days_since_delivery} days ago; the assumed policy allows {RETURN_WINDOW_DAYS} days.",
            "next_step": "Ask the support team to review whether an exception applies.",
            "escalate": True,
        }
    if order.final_sale:
        return {
            "eligible": False,
            "decision": "This item is final sale",
            "reason": "Final-sale items are not returnable under the assumed policy.",
            "next_step": "Contact support if the item arrived damaged or was not the item ordered.",
            "escalate": False,
        }
    if not unused_and_packaged:
        return {
            "eligible": False,
            "decision": "A manual review is needed",
            "reason": "Standard returns must be unused, unworn and in their original packaging.",
            "next_step": "Ask the support team to review the item's condition.",
            "escalate": True,
        }
    return {
        "eligible": True,
        "decision": "This item is eligible for return",
        "reason": f"It is within the {RETURN_WINDOW_DAYS}-day window and meets the condition requirements.",
        "next_step": "Create the return below, then pack the item securely.",
        "escalate": False,
    }


def refund_guidance(order: Order, today: date) -> dict[str, str | bool]:
    """Explain refund progress, timeline and when a person should step in."""
    if order.refund_issued_on:
        elapsed = (today - order.refund_issued_on).days
        overdue = elapsed > REFUND_MAX_DAYS
        return {
            "status": "Refund issued",
            "message": f"Northstar issued the refund on {order.refund_issued_on:%d %B %Y} to the original payment method.",
            "next_step": (
                "The expected bank-processing period has passed. Contact support for a payment trace."
                if overdue
                else f"Allow {REFUND_MIN_DAYS}–{REFUND_MAX_DAYS} days for the payment provider to display it."
            ),
            "escalate": overdue,
        }
    if order.return_status == "Under inspection":
        return {
            "status": "Under inspection",
            "message": "Northstar has received the return and is checking the item.",
            "next_step": f"When approved, the refund will go to the original payment method and normally appear within {REFUND_MIN_DAYS}–{REFUND_MAX_DAYS} days.",
            "escalate": False,
        }
    return {
        "status": order.return_status,
        "message": "No active refund was found for this order.",
        "next_step": "Start a return first, or contact support if you already sent the parcel.",
        "escalate": False,
    }
