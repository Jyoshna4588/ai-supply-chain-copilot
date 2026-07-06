# API Design

The backend will be built using FastAPI.

## Current APIs

### GET /
Returns welcome message.

### GET /health
Returns application health status.

## Planned APIs

### GET /inventory
Returns inventory records.

### GET /inventory/low-stock
Returns products where available stock is below safety stock.

### GET /suppliers
Returns supplier master data.

### GET /suppliers/performance
Returns supplier performance KPIs.

### GET /purchase-orders
Returns purchase order data.

### GET /purchase-orders/delayed
Returns delayed purchase orders.

### GET /forecast
Returns demand forecast data.

### POST /chat
Accepts a natural language question and returns an AI-generated response.

Example request:
```json
{
  "question": "Which products should be reordered this week?"
}