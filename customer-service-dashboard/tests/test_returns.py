from datetime import date

from return_rules import MOCK_ORDERS, check_eligibility, find_order, refund_guidance


TODAY = date(2026, 8, 15)


def test_order_lookup_uses_order_number_only():
    assert find_order(" ns-1001 ") == MOCK_ORDERS["NS-1001"]
    assert find_order("unknown") is None


def test_recent_unused_item_is_eligible():
    result = check_eligibility(MOCK_ORDERS["NS-1001"], "Wrong size", True, TODAY)
    assert result["eligible"] is True
    assert result["escalate"] is False


def test_old_item_requires_review():
    result = check_eligibility(MOCK_ORDERS["NS-1003"], "Changed my mind", True, TODAY)
    assert result["eligible"] is False
    assert result["escalate"] is True


def test_final_sale_is_not_eligible():
    result = check_eligibility(MOCK_ORDERS["NS-1002"], "No longer needed", True, TODAY)
    assert result["eligible"] is False
    assert result["decision"] == "This item is final sale"


def test_damaged_item_uses_specialist_path_even_if_used():
    result = check_eligibility(MOCK_ORDERS["NS-1001"], "Damaged item", False, TODAY)
    assert result["eligible"] is True
    assert result["escalate"] is True


def test_recent_refund_explains_wait():
    result = refund_guidance(MOCK_ORDERS["NS-1004"], TODAY)
    assert result["status"] == "Refund issued"
    assert result["escalate"] is False


def test_overdue_refund_escalates():
    result = refund_guidance(MOCK_ORDERS["NS-1006"], TODAY)
    assert result["escalate"] is True
    assert "payment trace" in result["next_step"]


def test_received_return_explains_inspection():
    result = refund_guidance(MOCK_ORDERS["NS-1005"], TODAY)
    assert result["status"] == "Under inspection"
    assert result["escalate"] is False
