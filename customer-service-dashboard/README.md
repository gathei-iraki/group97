# Northstar Customer Support Dashboard

This Streamlit MVP provides self-service support for order tracking and returns/refunds.

## Returns and refunds sample scenarios

Use the following order numbers to demonstrate and test the returns/refunds flow:

| Sample order number | Scenario | Expected outcome |
|---|---|---|
| `NS-1001` | Recent unused standard item | Eligible; creates `RET-1001` and provides return instructions |
| `NS-1002` | Final-sale item | Not eligible; explains the final-sale exclusion |
| `NS-1003` | Item is outside the 30-day return window | Requests a human review for a possible exception |
| `NS-1001` | Damaged or incorrect item | Creates a specialist return path and escalates the request |
| `NS-1004` | Recently issued refund | Explains the expected 5–10 day processing period |
| `NS-1005` | Return is under inspection | Explains the current status and what happens next |
| `NS-1006` | Issued refund is overdue | Escalates the request for a payment trace |
| Any invalid value | Order not found | Allows the customer to retry and does not invent an order status |

## Human escalation rules

Escalate the following cases to Northstar's support team:

- Damaged or incorrect items
- Requests outside the standard return window
- Exceptions involving an item's condition
- Lost return parcels
- Orders that cannot be verified
- System or data-retrieval failures
- Customers who dispute an automated decision
- Refunds delayed beyond the promised processing period


