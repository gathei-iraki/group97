# Northstar Customer Support Dashboard

## About the platform

The Northstar Customer Support Dashboard is a Streamlit self-service MVP for Northstar Retail Co. It reduces repetitive support tickets by allowing customers to check an order's delivery status and get return or refund guidance without waiting for a support agent.

The prototype uses mock data and demonstrates the proposed customer experience. It does not connect to Northstar's live order, carrier, payment, or customer-support systems.

## Features

### Order-status tracking

- Accepts an order number from the customer.
- Simulates an order lookup.
- Displays Processing, Shipped, Out for Delivery, or Delivered status.
- Shows an order date, estimated delivery date, tracking number, and order timeline where applicable.
- Provides contact options when the customer needs additional help.

The current order-status prototype generates a mock status for demonstration; it does not retrieve a real shipment.

### Returns and refunds

- Checks whether an item meets the assumed 30-day return policy.
- Handles standard, final-sale, damaged, and incorrect-item scenarios.
- Creates a simulated return reference for an eligible request.
- Gives clear packing, shipping, next-step, and refund-timing guidance.
- Shows mock return and refund states, including under inspection, recently refunded, and overdue.
- Escalates exceptions and overdue refunds to a human support agent.
- Uses an order number only and does not request an email address.

### Interface

- Provides a responsive home dashboard for selecting a support service.
- Uses green action buttons and Google Material icons.
- Keeps order tracking and returns/refunds in separate guided pages.

## Requirements

- Python 3.10 or later
- `pip`
- A terminal or command prompt

## Setup

1. Open a terminal and enter the project directory:

   ```bash
   cd group97/customer-service-dashboard
   ```

2. Create a virtual environment if one does not already exist:

   ```bash
   python3 -m venv .venv
   ```

3. Activate the virtual environment on Linux or macOS:

   ```bash
   source .venv/bin/activate
   ```

   On Windows PowerShell, use:

   ```powershell
   .venv\Scripts\Activate.ps1
   ```

4. Install the project dependency:

   ```bash
   python -m pip install -r requirements.txt
   ```

## Running the platform

With the virtual environment activated, run:

```bash
streamlit run app.py
```

Streamlit will display a local address, usually:

```text
http://localhost:8501
```

Open that address in a browser. Select **Track my order** for the order-status flow or **Manage a return** for the returns/refunds flow. Stop the server by pressing `Ctrl+C` in the terminal.

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

When escalating a case, pass the order number, item, return reason, answers already supplied, current return/refund status, and return reference to the support agent. This prevents the customer from having to repeat information.

