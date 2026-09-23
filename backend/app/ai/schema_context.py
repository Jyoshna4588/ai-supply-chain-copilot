SUPPLY_CHAIN_SCHEMA = """
You have access to the following BigQuery dataset containing simulated
supply-chain ERP data.

DATASET TABLES
==============

1. products
-----------
Purpose:
Contains product master data.

Important columns:
- product_id: Unique product identifier.
- product_name: Human-readable product name.
- category: Product category.
- brand: Product brand.
- unit_price: Selling price per unit.
- unit_cost: Cost per unit.
- safety_stock: Minimum emergency inventory level.
- reorder_point: Inventory level at which replenishment should begin.

Primary key:
- product_id


2. inventory
------------
Purpose:
Contains product inventory by warehouse.

Important columns:
- product_id: Product identifier.
- warehouse_id: Warehouse identifier.
- current_stock: Physical stock quantity.
- reserved_stock: Stock allocated to existing orders.
- available_stock: Stock available for new orders.
- safety_stock: Minimum emergency inventory level.
- reorder_point: Replenishment trigger level.
- inventory_status: Inventory classification such as Low Stock,
  Healthy, or Overstock.

Relationships:
- inventory.product_id joins products.product_id.
- inventory.warehouse_id joins warehouses.warehouse_id.


3. warehouses
-------------
Purpose:
Contains warehouse master data.

Important columns:
- warehouse_id: Unique warehouse identifier.
- warehouse_name: Human-readable warehouse name.
- location: Warehouse location.
- capacity: Total warehouse capacity.
- utilization_rate: Percentage of capacity currently used.

Primary key:
- warehouse_id


4. suppliers
------------
Purpose:
Contains supplier master data.

Important columns:
- supplier_id: Unique supplier identifier.
- supplier_name: Human-readable supplier name.
- risk_profile: Supplier risk classification.
- lead_time_days: Expected supplier lead time.
- quality_rating: Supplier quality score.

Primary key:
- supplier_id


5. supplier_performance
-----------------------
Purpose:
Contains calculated supplier performance metrics.

Important columns:
- performance_id: Unique performance record identifier.
- supplier_id: Supplier identifier.
- supplier_name: Human-readable supplier name.
- risk_profile: Supplier risk classification.
- total_orders: Total purchase orders associated with the supplier.
- delayed_orders: Number of delayed purchase orders.
- delay_rate: Percentage of orders that were delayed.
- otif_rate: On-time and in-full delivery percentage.
- average_lead_time: Average supplier lead time in days.
- quality_rating: Supplier quality score.
- defect_rate: Percentage of defective supply.
- cost_score: Supplier cost-performance score.

Relationships:
- supplier_performance.supplier_id joins suppliers.supplier_id.


6. purchase_orders
------------------
Purpose:
Contains procurement purchase-order transactions.

Important columns may include:
- po_number: Unique purchase-order number.
- supplier_id: Supplier identifier.
- product_id: Product identifier.
- quantity: Ordered quantity.
- order_value: Total purchase-order value.
- order_date: Date when the order was placed.
- expected_delivery_date: Planned delivery date.
- actual_delivery_date: Actual delivery date, when available.
- status: Purchase-order status such as Open, Delivered, or Delayed.
- delay_reason: Reason for delayed delivery.

Relationships:
- purchase_orders.supplier_id joins suppliers.supplier_id.
- purchase_orders.product_id joins products.product_id.


7. sales_orders
---------------
Purpose:
Contains customer demand and sales-order transactions.

Important columns may include:
- sales_order_id: Unique sales-order identifier.
- product_id: Product identifier.
- warehouse_id: Fulfilling warehouse identifier.
- order_date: Customer order date.
- quantity: Ordered quantity.
- order_value: Sales-order value.
- status: Sales-order status.

Relationships:
- sales_orders.product_id joins products.product_id.
- sales_orders.warehouse_id joins warehouses.warehouse_id.


8. demand_forecast
------------------
Purpose:
Contains forecast and actual demand information.

Important columns may include:
- product_id: Product identifier.
- warehouse_id: Warehouse identifier.
- forecast_date: Forecast period.
- forecast_quantity: Predicted demand.
- actual_quantity: Actual observed demand.
- forecast_error: Difference between forecast and actual demand.

Relationships:
- demand_forecast.product_id joins products.product_id.
- demand_forecast.warehouse_id joins warehouses.warehouse_id.


9. shipments
------------
Purpose:
Contains shipment and transportation information.

Important columns may include:
- shipment_id: Unique shipment identifier.
- warehouse_id: Origin or responsible warehouse.
- expected_delivery_date: Planned shipment delivery date.
- actual_delivery_date: Actual shipment delivery date.
- status: Shipment status.
- delay_days: Number of days late.
- carrier: Transportation provider.

Relationships:
- shipments.warehouse_id joins warehouses.warehouse_id.


10. returns
-----------
Purpose:
Contains product-return transactions.

Important columns may include:
- return_id: Unique return identifier.
- product_id: Product identifier.
- warehouse_id: Warehouse identifier.
- return_date: Date of return.
- return_quantity: Quantity returned.
- return_reason: Reason for return.
- return_value: Financial value of the return.

Relationships:
- returns.product_id joins products.product_id.
- returns.warehouse_id joins warehouses.warehouse_id.


BIGQUERY SQL RULES
==================

- Use GoogleSQL syntax.
- Fully qualify tables using:
  `{project_id}.{dataset_id}.table_name`
- Generate only SELECT statements.
- Never generate INSERT, UPDATE, DELETE, MERGE, DROP, ALTER,
  CREATE, TRUNCATE, GRANT, or REVOKE statements.
- Use only tables and columns listed in this schema.
- Use explicit column names instead of SELECT *.
- Add LIMIT 100 unless the query returns an aggregate result.
- Use SAFE_DIVIDE when division could involve zero.
- Use meaningful aliases for calculated columns.
- Do not use information from tables outside the approved dataset.
"""