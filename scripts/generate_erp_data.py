import random
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

random.seed(42)


def random_date(start_date: datetime, end_date: datetime) -> datetime:
    days_between = (end_date - start_date).days
    return start_date + timedelta(days=random.randint(0, days_between))


SUPPLIER_PROFILES = [
    ("SUP001", "Dell Technologies", "USA", "Reliable"),
    ("SUP002", "HP Inc.", "USA", "Reliable"),
    ("SUP003", "Lenovo Group", "China", "Average"),
    ("SUP004", "Samsung Electronics", "South Korea", "Reliable"),
    ("SUP005", "Logitech", "Switzerland", "Average"),
    ("SUP006", "Sony Corporation", "Japan", "Delayed"),
    ("SUP007", "Canon Inc.", "Japan", "Average"),
    ("SUP008", "LG Electronics", "South Korea", "Reliable"),
    ("SUP009", "Apex Packaging", "Mexico", "Delayed"),
    ("SUP010", "Global Textile Supply", "Vietnam", "Delayed"),
    ("SUP011", "FreshSource Foods", "USA", "Average"),
    ("SUP012", "Prime Auto Parts", "Canada", "Reliable"),
    ("SUP013", "MedLife Supplies", "India", "Average"),
    ("SUP014", "Urban Home Goods", "USA", "Reliable"),
    ("SUP015", "Nova Beauty Supply", "France", "Average"),
    ("SUP016", "Keystone Office Products", "USA", "Reliable"),
    ("SUP017", "Riverstone Traders", "India", "Delayed"),
    ("SUP018", "Summit Industrial", "USA", "Average"),
    ("SUP019", "MetroGoods Wholesale", "Mexico", "Reliable"),
    ("SUP020", "Titan Manufacturing", "China", "Delayed"),
]


PRODUCT_TEMPLATES = {
    "Electronics": [
        "Laptop", "Monitor", "Wireless Mouse", "Keyboard", "Tablet",
        "Smartphone", "Printer", "Router", "Bluetooth Speaker", "Headphones"
    ],
    "Home Goods": [
        "Coffee Maker", "Vacuum Cleaner", "Air Purifier", "Desk Lamp",
        "Storage Rack", "Cookware Set", "Bedding Set", "Dining Chair"
    ],
    "Apparel": [
        "T-Shirt", "Jeans", "Jacket", "Sneakers", "Hoodie",
        "Formal Shirt", "Dress", "Backpack"
    ],
    "Grocery": [
        "Organic Rice", "Olive Oil", "Cereal Box", "Protein Bar",
        "Coffee Beans", "Pasta Pack", "Snack Box", "Tea Pack"
    ],
    "Health": [
        "Vitamin Pack", "First Aid Kit", "Thermometer", "Protein Powder",
        "Sanitizer Pack", "Health Monitor"
    ],
    "Beauty": [
        "Face Cream", "Shampoo", "Conditioner", "Body Lotion",
        "Makeup Kit", "Perfume"
    ],
    "Office Supplies": [
        "Notebook", "Printer Paper", "Desk Organizer", "Ballpoint Pen",
        "File Folder", "Whiteboard Marker"
    ],
    "Automotive": [
        "Car Battery", "Engine Oil", "Brake Pads", "Wiper Blades",
        "Air Filter", "Tire Inflator"
    ],
}


def generate_suppliers():
    rows = []

    for supplier_id, supplier_name, country, risk_profile in SUPPLIER_PROFILES:
        if risk_profile == "Reliable":
            lead_time = random.randint(5, 12)
            on_time = round(random.uniform(92, 98), 2)
            quality = round(random.uniform(4.4, 5.0), 2)
        elif risk_profile == "Average":
            lead_time = random.randint(10, 20)
            on_time = round(random.uniform(80, 91), 2)
            quality = round(random.uniform(3.8, 4.5), 2)
        else:
            lead_time = random.randint(18, 35)
            on_time = round(random.uniform(62, 79), 2)
            quality = round(random.uniform(3.2, 4.1), 2)

        rows.append({
            "supplier_id": supplier_id,
            "supplier_name": supplier_name,
            "country": country,
            "risk_profile": risk_profile,
            "lead_time_days": lead_time,
            "quality_rating": quality,
            "on_time_delivery_rate": on_time,
            "contact_email": f"supplychain@{supplier_name.lower().replace(' ', '').replace('.', '')}.com"
        })

    return pd.DataFrame(rows)


def generate_warehouses():
    data = [
        ("WH001", "Dallas Distribution Center", "Dallas, TX", 100000, "Avery Johnson", 88.5),
        ("WH002", "Chicago Fulfillment Center", "Chicago, IL", 85000, "Sophia Martinez", 91.2),
        ("WH003", "Atlanta Regional Warehouse", "Atlanta, GA", 90000, "Daniel Lee", 72.4),
        ("WH004", "Seattle Distribution Hub", "Seattle, WA", 75000, "Mia Thompson", 68.9),
        ("WH005", "New York Metro DC", "New York, NY", 95000, "Ethan Brown", 96.8),
        ("WH006", "Los Angeles Import Hub", "Los Angeles, CA", 110000, "Olivia Davis", 94.5),
        ("WH007", "Phoenix Regional DC", "Phoenix, AZ", 70000, "Noah Wilson", 57.3),
        ("WH008", "Miami Export Hub", "Miami, FL", 80000, "Emma Garcia", 83.6),
    ]

    return pd.DataFrame([
        {
            "warehouse_id": warehouse_id,
            "warehouse_name": name,
            "warehouse_location": location,
            "capacity": capacity,
            "current_utilization": utilization,
            "manager_name": manager
        }
        for warehouse_id, name, location, capacity, manager, utilization in data
    ])


def generate_products(suppliers_df, warehouses_df, number_of_products=500):
    brands = ["Apex", "Nova", "Prime", "Urban", "Zenith", "Core", "Fresh", "Metro"]
    suppliers = suppliers_df["supplier_id"].tolist()
    warehouses = warehouses_df["warehouse_id"].tolist()

    products = []

    for i in range(1, number_of_products + 1):
        category = random.choice(list(PRODUCT_TEMPLATES.keys()))
        item_type = random.choice(PRODUCT_TEMPLATES[category])
        brand = random.choice(brands)

        product_name = f"{brand} {item_type} Model {random.randint(100, 999)}"

        safety_stock = random.randint(80, 450)
        reorder_point = safety_stock + random.randint(75, 350)

        products.append({
            "product_id": f"PROD{i:05d}",
            "product_name": product_name,
            "category": category,
            "brand": brand,
            "unit_price": round(random.uniform(5, 1200), 2),
            "supplier_id": random.choice(suppliers),
            "warehouse_id": random.choice(warehouses),
            "safety_stock": safety_stock,
            "reorder_point": reorder_point
        })

    return pd.DataFrame(products)


def generate_inventory(products_df):
    inventory = []

    # Business scenarios:
    # 20% low stock, 10% overstock, rest normal.
    for idx, product in products_df.iterrows():
        scenario = random.choices(
            ["low_stock", "overstock", "normal"],
            weights=[20, 10, 70],
            k=1
        )[0]

        safety_stock = int(product["safety_stock"])
        reorder_point = int(product["reorder_point"])

        if scenario == "low_stock":
            current_stock = random.randint(0, max(1, safety_stock - 1))
        elif scenario == "overstock":
            current_stock = random.randint(reorder_point + 500, reorder_point + 1800)
        else:
            current_stock = random.randint(safety_stock, reorder_point + 400)

        reserved_stock = random.randint(0, min(current_stock, 200))
        available_stock = current_stock - reserved_stock

        inventory_status = (
            "Low Stock" if available_stock < safety_stock
            else "Overstock" if current_stock > reorder_point + 500
            else "Healthy"
        )

        inventory.append({
            "inventory_id": f"INV{idx + 1:06d}",
            "product_id": product["product_id"],
            "warehouse_id": product["warehouse_id"],
            "current_stock": current_stock,
            "reserved_stock": reserved_stock,
            "available_stock": available_stock,
            "safety_stock": safety_stock,
            "reorder_point": reorder_point,
            "inventory_status": inventory_status,
            "last_updated": datetime.now().strftime("%Y-%m-%d")
        })

    return pd.DataFrame(inventory)


def generate_purchase_orders(products_df, suppliers_df, number_of_orders=3000):
    purchase_orders = []
    start_date = datetime(2025, 1, 1)
    end_date = datetime(2026, 6, 30)

    delay_reasons = [
        "Port congestion",
        "Carrier capacity shortage",
        "Supplier production delay",
        "Customs clearance delay",
        "Weather disruption",
        "Raw material shortage"
    ]

    supplier_profile_map = suppliers_df.set_index("supplier_id")["risk_profile"].to_dict()

    for i in range(1, number_of_orders + 1):
        product = products_df.sample(1).iloc[0]
        supplier_id = product["supplier_id"]
        risk_profile = supplier_profile_map[supplier_id]

        order_date = random_date(start_date, end_date)

        if risk_profile == "Reliable":
            planned_lead = random.randint(5, 14)
            status = random.choices(
                ["Delivered", "In Transit", "Delayed", "Open", "Cancelled"],
                weights=[72, 14, 5, 7, 2],
                k=1
            )[0]
        elif risk_profile == "Average":
            planned_lead = random.randint(10, 22)
            status = random.choices(
                ["Delivered", "In Transit", "Delayed", "Open", "Cancelled"],
                weights=[60, 15, 12, 10, 3],
                k=1
            )[0]
        else:
            planned_lead = random.randint(18, 35)
            status = random.choices(
                ["Delivered", "In Transit", "Delayed", "Open", "Cancelled"],
                weights=[45, 18, 25, 9, 3],
                k=1
            )[0]

        expected_delivery_date = order_date + timedelta(days=planned_lead)

        if status == "Delivered":
            actual_delivery_date = expected_delivery_date + timedelta(days=random.randint(-3, 5))
            delay_reason = ""
        elif status == "Delayed":
            actual_delivery_date = expected_delivery_date + timedelta(days=random.randint(6, 25))
            delay_reason = random.choice(delay_reasons)
        else:
            actual_delivery_date = None
            delay_reason = ""

        quantity = random.randint(50, 2500)
        order_value = round(quantity * float(product["unit_price"]), 2)

        purchase_orders.append({
            "po_number": f"PO{i:06d}",
            "supplier_id": supplier_id,
            "product_id": product["product_id"],
            "quantity": quantity,
            "unit_price": product["unit_price"],
            "order_value": order_value,
            "order_date": order_date.strftime("%Y-%m-%d"),
            "expected_delivery_date": expected_delivery_date.strftime("%Y-%m-%d"),
            "actual_delivery_date": actual_delivery_date.strftime("%Y-%m-%d") if actual_delivery_date else "",
            "status": status,
            "delay_reason": delay_reason
        })

    return pd.DataFrame(purchase_orders)


def generate_sales_orders(products_df, number_of_orders=10000):
    sales_orders = []
    start_date = datetime(2025, 1, 1)
    end_date = datetime(2026, 6, 30)

    customer_names = [
        "NorthStar Retail", "BlueWave Stores", "Urban Cart",
        "FreshMart", "QuickBuy", "ValueHub", "SmartShop",
        "DailyNeeds", "MetroBasket", "PrimeOutlet"
    ]

    for i in range(1, number_of_orders + 1):
        product = products_df.sample(1).iloc[0]
        order_date = random_date(start_date, end_date)

        # Seasonal spikes for grocery and apparel
        if product["category"] in ["Grocery", "Apparel"] and order_date.month in [11, 12]:
            quantity = random.randint(20, 120)
        else:
            quantity = random.randint(1, 50)

        sales_orders.append({
            "order_id": f"SO{i:07d}",
            "customer_name": random.choice(customer_names),
            "product_id": product["product_id"],
            "quantity": quantity,
            "order_date": order_date.strftime("%Y-%m-%d"),
            "warehouse_id": product["warehouse_id"],
            "sales_value": round(quantity * float(product["unit_price"]), 2)
        })

    return pd.DataFrame(sales_orders)


def generate_demand_forecast(products_df):
    forecast_rows = []
    months = pd.date_range(start="2025-01-01", end="2026-06-01", freq="MS")
    sample_products = products_df.sample(120, random_state=42)

    forecast_id = 1

    for _, product in sample_products.iterrows():
        base_demand = random.randint(500, 5000)

        for month in months:
            seasonal_multiplier = 1.0

            if product["category"] in ["Grocery", "Apparel"] and month.month in [11, 12]:
                seasonal_multiplier = random.uniform(1.25, 1.75)

            forecast_qty = int(base_demand * seasonal_multiplier)

            # 15% of records have high forecast error
            if random.random() < 0.15:
                actual_qty = max(0, forecast_qty + random.randint(-1500, 1500))
            else:
                actual_qty = max(0, forecast_qty + random.randint(-350, 350))

            mape = abs(actual_qty - forecast_qty) / actual_qty * 100 if actual_qty else 0

            forecast_rows.append({
                "forecast_id": f"FC{forecast_id:07d}",
                "product_id": product["product_id"],
                "month": month.strftime("%Y-%m"),
                "forecast_quantity": forecast_qty,
                "actual_quantity": actual_qty,
                "mape": round(mape, 2),
                "forecast_accuracy_status": "High Error" if mape > 20 else "Acceptable"
            })

            forecast_id += 1

    return pd.DataFrame(forecast_rows)


def generate_shipments(purchase_orders_df, warehouses_df):
    shipments = []
    carriers = ["FedEx", "UPS", "DHL", "XPO Logistics", "J.B. Hunt", "Ryder"]
    destinations = ["Dallas, TX", "Chicago, IL", "Atlanta, GA", "Seattle, WA", "New York, NY"]

    for i in range(1, 2501):
        po = purchase_orders_df.sample(1).iloc[0]

        if po["status"] == "Delayed":
            status = random.choices(
                ["Delayed", "Exception", "In Transit"],
                weights=[65, 20, 15],
                k=1
            )[0]
        else:
            status = random.choices(
                ["Delivered", "In Transit", "Delayed", "Exception"],
                weights=[65, 20, 10, 5],
                k=1
            )[0]

        eta = random_date(datetime(2025, 1, 1), datetime(2026, 7, 31))

        shipments.append({
            "shipment_id": f"SHP{i:06d}",
            "po_number": po["po_number"],
            "carrier": random.choice(carriers),
            "warehouse_id": random.choice(warehouses_df["warehouse_id"].tolist()),
            "destination": random.choice(destinations),
            "status": status,
            "eta": eta.strftime("%Y-%m-%d")
        })

    return pd.DataFrame(shipments)


def generate_returns(products_df, number_of_returns=1200):
    returns = []
    reasons = ["Damaged", "Wrong Item", "Late Delivery", "Quality Issue", "Customer Changed Mind"]

    for i in range(1, number_of_returns + 1):
        product = products_df.sample(1).iloc[0]
        return_date = random_date(datetime(2025, 1, 1), datetime(2026, 6, 30))

        # Higher returns for Electronics and Apparel
        if product["category"] in ["Electronics", "Apparel"]:
            quantity = random.randint(3, 25)
        else:
            quantity = random.randint(1, 12)

        returns.append({
            "return_id": f"RET{i:06d}",
            "product_id": product["product_id"],
            "return_reason": random.choice(reasons),
            "warehouse_id": product["warehouse_id"],
            "quantity": quantity,
            "return_date": return_date.strftime("%Y-%m-%d")
        })

    return pd.DataFrame(returns)


def generate_supplier_performance(suppliers_df, purchase_orders_df):
    performance_rows = []

    for _, supplier in suppliers_df.iterrows():
        supplier_orders = purchase_orders_df[purchase_orders_df["supplier_id"] == supplier["supplier_id"]]

        total_orders = len(supplier_orders)
        delayed_orders = len(supplier_orders[supplier_orders["status"] == "Delayed"])
        delivered_orders = len(supplier_orders[supplier_orders["status"] == "Delivered"])

        delay_rate = round((delayed_orders / total_orders) * 100, 2) if total_orders else 0
        otif_rate = round(100 - delay_rate, 2)

        if supplier["risk_profile"] == "Reliable":
            defect_rate = round(random.uniform(0.5, 2.5), 2)
            cost_score = round(random.uniform(80, 95), 2)
        elif supplier["risk_profile"] == "Average":
            defect_rate = round(random.uniform(2.5, 5.5), 2)
            cost_score = round(random.uniform(65, 82), 2)
        else:
            defect_rate = round(random.uniform(5.5, 10.0), 2)
            cost_score = round(random.uniform(45, 68), 2)

        performance_rows.append({
            "performance_id": f"PERF{len(performance_rows) + 1:04d}",
            "supplier_id": supplier["supplier_id"],
            "supplier_name": supplier["supplier_name"],
            "risk_profile": supplier["risk_profile"],
            "total_orders": total_orders,
            "delayed_orders": delayed_orders,
            "delay_rate": delay_rate,
            "otif_rate": otif_rate,
            "average_lead_time": supplier["lead_time_days"],
            "quality_rating": supplier["quality_rating"],
            "defect_rate": defect_rate,
            "cost_score": cost_score
        })

    return pd.DataFrame(performance_rows)


def main():
    print("Generating realistic simulated ERP supply chain data...\n")

    suppliers_df = generate_suppliers()
    warehouses_df = generate_warehouses()
    products_df = generate_products(suppliers_df, warehouses_df)
    inventory_df = generate_inventory(products_df)
    purchase_orders_df = generate_purchase_orders(products_df, suppliers_df)
    sales_orders_df = generate_sales_orders(products_df)
    demand_forecast_df = generate_demand_forecast(products_df)
    shipments_df = generate_shipments(purchase_orders_df, warehouses_df)
    returns_df = generate_returns(products_df)
    supplier_performance_df = generate_supplier_performance(suppliers_df, purchase_orders_df)

    datasets = {
        "suppliers.csv": suppliers_df,
        "warehouses.csv": warehouses_df,
        "products.csv": products_df,
        "inventory.csv": inventory_df,
        "purchase_orders.csv": purchase_orders_df,
        "sales_orders.csv": sales_orders_df,
        "demand_forecast.csv": demand_forecast_df,
        "shipments.csv": shipments_df,
        "returns.csv": returns_df,
        "supplier_performance.csv": supplier_performance_df,
    }

    for file_name, dataframe in datasets.items():
        output_path = DATA_DIR / file_name
        dataframe.to_csv(output_path, index=False)
        print(f"Created {file_name} with {len(dataframe)} rows")

    print("\nERP data generation completed successfully!")
    print("Business scenarios included:")
    print("- Low-stock products")
    print("- Overstocked products")
    print("- Delayed suppliers")
    print("- High forecast error")
    print("- Warehouse utilization risk")
    print("- Shipment delays")
    print("- Return spikes")


if __name__ == "__main__":
    main()