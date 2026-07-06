# Database Design

This project uses simulated ERP-style supply chain data. The structured data will initially be stored as CSV files and later loaded into BigQuery.

## Tables

### 1. Products
Stores product master data.

Columns:
- product_id
- product_name
- category
- brand
- unit_price
- supplier_id
- warehouse_id
- safety_stock
- reorder_point

### 2. Inventory
Stores current inventory levels.

Columns:
- inventory_id
- product_id
- warehouse_id
- current_stock
- reserved_stock
- available_stock
- last_updated

### 3. Suppliers
Stores supplier master data.

Columns:
- supplier_id
- supplier_name
- country
- lead_time_days
- quality_rating
- on_time_delivery_rate
- contact_email

### 4. Purchase Orders
Stores procurement transactions.

Columns:
- po_number
- supplier_id
- product_id
- quantity
- order_date
- expected_delivery_date
- actual_delivery_date
- status

### 5. Sales Orders
Stores customer demand transactions.

Columns:
- order_id
- customer_name
- product_id
- quantity
- order_date
- warehouse_id

### 6. Demand Forecast
Stores forecast versus actual demand.

Columns:
- forecast_id
- product_id
- month
- forecast_quantity
- actual_quantity
- mape

### 7. Warehouses
Stores warehouse master data.

Columns:
- warehouse_id
- warehouse_location
- capacity
- current_utilization
- manager_name

### 8. Shipments
Stores outbound shipment information.

Columns:
- shipment_id
- carrier
- warehouse_id
- destination
- status
- eta

### 9. Supplier Performance
Stores supplier KPI metrics.

Columns:
- performance_id
- supplier_id
- average_lead_time
- otif_rate
- defect_rate
- cost_score

### 10. Returns
Stores return and reverse logistics data.

Columns:
- return_id
- product_id
- return_reason
- warehouse_id
- quantity
- return_date