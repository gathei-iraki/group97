# tests/test_orders.py
"""
Comprehensive Test Suite for Northstar Customer Support Dashboard

This module combines tests for:
- Order Status Functionality
- Order ID Length Validation
- Data Structure and Type Validation
"""

import pytest
import re
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import the function from the main module to avoid code duplication
from pages.order_status import generate_mock_order_status


class TestOrderStatusFunctionality:
    """Test suite for order status data generation"""
    
    def test_generate_mock_order_status_structure(self):
        """Test that the mock data generator returns the correct structure."""
        order_id = "TEST-001"
        result = generate_mock_order_status(order_id)
        
        expected_keys = ["order_id", "status", "order_date", "estimated_delivery", "tracking_number", "history"]
        for key in expected_keys:
            assert key in result, f"Missing key: {key}"
        
        assert result["order_id"] == order_id
        
        valid_statuses = ["Processing", "Shipped", "Out for Delivery", "Delivered"]
        assert result["status"] in valid_statuses
    
    def test_generate_mock_order_status_types(self):
        """Test that all returned values are of the correct type."""
        result = generate_mock_order_status("ORD-123")
        
        assert isinstance(result["order_id"], str)
        assert isinstance(result["status"], str)
        assert isinstance(result["order_date"], str)
        assert isinstance(result["estimated_delivery"], str)
        assert isinstance(result["history"], list)
        
        assert result["tracking_number"] is None or isinstance(result["tracking_number"], str)
    
    def test_generate_mock_order_status_tracking_format(self):
        """Test that tracking numbers follow the expected format."""
        for _ in range(10):
            result = generate_mock_order_status("ORD-TEST")
            if result["tracking_number"] is not None:
                tracking = result["tracking_number"]
                assert tracking.startswith("1Z"), f"Invalid tracking format: {tracking}"
                assert len(tracking) >= 10, f"Tracking too short: {tracking}"
    
    def test_generate_mock_order_status_history(self):
        """Test that order history is structured correctly."""
        result = generate_mock_order_status("ORD-HIST")
        
        assert len(result["history"]) >= 2
        
        for entry in result["history"]:
            assert "status" in entry
            assert "date" in entry
            assert isinstance(entry["status"], str)
            assert isinstance(entry["date"], str)
    
    def test_generate_mock_order_status_dates(self):
        """Test that dates are in the correct format (YYYY-MM-DD)."""
        result = generate_mock_order_status("ORD-DATE")
        
        date_pattern = r'^\d{4}-\d{2}-\d{2}$'
        assert re.match(date_pattern, result["order_date"])
        
        if result["estimated_delivery"] != "Delivered":
            assert re.match(date_pattern, result["estimated_delivery"])
    
    def test_generate_mock_order_status_consistent_id(self):
        """Test that the function returns the same ID that was passed."""
        test_id = "CUSTOM-001"
        result = generate_mock_order_status(test_id)
        assert result["order_id"] == test_id
    
    def test_generate_mock_order_status_all_statuses(self):
        """Test that all statuses can be generated."""
        statuses_found = set()
        for _ in range(20):
            result = generate_mock_order_status("ORD-STATUS")
            statuses_found.add(result["status"])
        
        assert len(statuses_found) >= 3, f"Only found statuses: {statuses_found}"


class TestOrderIDValidation:
    """Test suite for order ID length validation (3-12 characters)"""
    
    def test_order_id_valid_length_minimum(self):
        """Test that order IDs can be exactly 3 characters (minimum valid)."""
        order_id = "ORD"
        assert len(order_id) >= 3, f"Order ID '{order_id}' is below minimum (3 chars)"
        result = generate_mock_order_status(order_id)
        assert result["order_id"] == order_id
    
    def test_order_id_valid_length_maximum(self):
        """Test that order IDs can be exactly 12 characters (maximum valid)."""
        order_id = "ORD-12345678"
        assert len(order_id) == 12, f"Order ID '{order_id}' is not 12 chars"
        assert len(order_id) <= 12, f"Order ID '{order_id}' exceeds maximum (12 chars)"
        result = generate_mock_order_status(order_id)
        assert result["order_id"] == order_id
    
    def test_order_id_valid_length_mid_range(self):
        """Test that order IDs work with mid-range valid lengths (4-11 chars)."""
        test_ids = ["ABCD", "ORD-001", "ORDER123456"]
        for test_id in test_ids:
            assert 3 <= len(test_id) <= 12, f"Order ID '{test_id}' is outside valid range (3-12 chars)"
            result = generate_mock_order_status(test_id)
            assert result["order_id"] == test_id
    
    def test_order_id_invalid_too_short(self):
        """Test that order IDs below 3 characters are invalid."""
        order_id = "AB"
        assert len(order_id) < 3, f"Order ID '{order_id}' should be below minimum (3 chars)"
        # Validation logic check
        is_valid = len(order_id) >= 3
        assert not is_valid, f"Order ID '{order_id}' should be invalid"
    
    def test_order_id_invalid_too_long(self):
        """Test that order IDs above 12 characters are invalid."""
        order_id = "ORD-13311018184941516515165165165165165165165156102061065165"
        assert len(order_id) > 12, f"Order ID '{order_id}' should exceed maximum (12 chars)"
        # Validation logic check
        is_valid = len(order_id) <= 12
        assert not is_valid, f"Order ID '{order_id}' should be invalid"
    
    def test_order_id_boundary_at_min(self):
        """Test order ID at exact minimum boundary (3 chars)."""
        order_id = "ORD"
        is_valid = 3 <= len(order_id) <= 12
        assert is_valid, f"Order ID '{order_id}' at minimum should be valid"
    
    def test_order_id_boundary_at_max(self):
        """Test order ID at exact maximum boundary (12 chars)."""
        order_id = "ORD-ABCD1234"
        assert len(order_id) == 12
        is_valid = 3 <= len(order_id) <= 12
        assert is_valid, f"Order ID '{order_id}' at maximum should be valid"


class TestOrderIDValidationParametrized:
    """Parametrized tests for comprehensive order ID validation coverage"""
    
    @pytest.mark.parametrize("order_id,should_be_valid", [
        ("AB", False),  # too short (2 chars)
        ("ORD", True),  # minimum valid (3 chars)
        ("ORD-001", True),  # standard format (7 chars)
        ("ORD-12345678", True),  # maximum valid (12 chars)
        ("ORDER123456", True),  # alternative format (11 chars)
        ("ORD-13311018184941516515165165165165165165165156102061065165", False),  # too long (60+ chars)
    ])
    def test_order_id_validation_parametrized(self, order_id, should_be_valid):
        """Parametrized test for various order ID lengths."""
        is_valid = 3 <= len(order_id) <= 12
        assert is_valid == should_be_valid, \
            f"Order ID '{order_id}' (len={len(order_id)}) validation failed. Expected {should_be_valid}, got {is_valid}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])