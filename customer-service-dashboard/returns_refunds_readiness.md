# Northstar Returns & Refunds 

## What works

- Customers can check standard return eligibility using an order number; no email address is collected.
- The flow explains the decision, reason, next action and expected timeline.
- Eligible customers can create a simulated return reference and receive packing guidance.
- Damaged and incorrect items follow a free-return specialist-review path.
- Customers can see mock return/refund states including under inspection, recently issued and overdue.
- Policy exceptions and overdue refunds are directed to human support with the context to provide.



## Human escalation rules

Escalate damaged/incorrect items, out-of-window requests, condition exceptions, lost parcels, unverifiable orders, system failures, disputed decisions and refunds beyond the promised period. Pass the order number, item, reason, answers, current status and return reference so customers do not repeat themselves.

## Demo and acceptance scenarios

| Order | Scenario | Expected outcome |
|---|---|---|
| NS-1001 | Recent unused standard item | Eligible; creates `RET-1001` and gives instructions |
| NS-1002 | Final-sale item | Not eligible; explains the exclusion |
| NS-1003 | Outside 30 days | Requests human exception review |
| NS-1001 | Damaged or incorrect item | Creates specialist path and escalates |
| NS-1004 | Recently issued refund | Explains the 5–10 day wait |
| NS-1005 | Return under inspection | Explains what happens next |
| NS-1006 | Overdue issued refund | Escalates for a payment trace |
| Invalid value | Order not found | Allows retry and does not invent a status |


