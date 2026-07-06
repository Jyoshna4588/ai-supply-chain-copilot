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
    random_days = random.randint(0, days_between)
    return start_date + timedelta(days=random_days)


def generate_suppliers():
    countries = ["USA", "Mexico", "Canada", "India", "China", "Vietnam"]
    supplier_names = [
        "Alpha Manufacturing", "BrightSource Logistics", "CoreTech Supplies",
        "Delta Components", "Evergreen Packaging", "FastLine Distribution",
        "Global Parts Co", "Horizon Industrial", "Innovex Materials",
        "JetStream Suppliers", "Keystone Electronics", "Liberty Wholesale",
        "MetroGoods", "Nova Retail Supply", "Orion Components",
        "PrimeSource", "Quantum Packaging", "Riverstone Traders",
        "Summit Supply Group", "Titan Manufacturing"
    ]

    suppliers = []
    for i, name in enumerate(supplier_names, start=1):
        suppliers.append({
            "supplier_id": f"SUP{i:03d}",
            "supplier_name": name,
            "country": random.choice(countries),
            "lead_time_days": random.randint(5, 30),
            "quality_rating": round(random.uniform(3.5, 5.0), 2),
            "on_time_delivery_rate": round(random.uniform(70, 98), 2),
            "contact_email": f"contact{i}@{name.lower().replace(' ', '').replace(',', '')}.com"
        })

    return pd.DataFrame(suppliers)


def generate_warehouses():
    warehouses = [
        ("WH001", "Dallas, TX", 100000, "Avery Johnson"),
        ("WH002", "Chicago, IL", 85000, "Sophia Martinez"),
        ("WH003", "Atlanta, GA", 90000, "Daniel Lee"),
        ("WH004", "Seattle, WA", 75000, "Mia Thompson"),
        ("WH005", "New York, NY", 95000, "Ethan Brown"),
        ("WH006", "Los Angeles, CA", 110000, "Olivia Davis"),
        ("WH007", "Phoenix, AZ", 70000, "Noah Wilson"),
        ("WH008", "Miami, FL", 80000, "Emma Garcia"),
    ]

    data = []
    for warehouse_id, location, capacity, manager in warehouses:
        data.append({
            "warehouse_id": warehouse_id,
            "warehouse_location": location,
            "capacity": capacity,
            "current_utilization": round(random.uniform(55, 95), 2),
            "manager_name": manager
        })

    return pd.DataFrame(data)


def generate_products(suppliers_df, warehouses_df, number_of_products=500):
    categories = [
        "Electronics", "Home Goods", "Apparel", "Grocery",
        "Health", "Beauty", "Office Supplies", "Automotive"
    ]
    brands = ["Apex", "Nova", "Prime", "Urban", "Zenith", "Core", "Fresh", "Metro"]

    products = []
    for i in range(1, number_of_products + 1):
        category = random.choice(categories)
        product_name = f"{random.choice(brands)} {category} Item {i}"

        safety_stock = random.randint(50, 500)
        reorder_point = safety_stock + random.randint(50, 300)

        products.append({
            "product_id": f"PROD{i:05d}",
            "product_name": product_name,
            "category": category,
            "brand": random.choice(brands),
            "unit_price": round(random.uniform(5, 500), 2),
            "supplier_id": random.choice(suppliers_df["supplier_id"].tolist()),
            "warehouse_id": random.choice(warehouses_df["warehouse_id"].tolist()),
            "safety_stock": safety_stock,
            "reorder_point": reorder_point
        })

    return pd.DataFrame(products)


def generate_inventory(products_df):
    inventory = []

    for idx, row in products_df.iterrows():
        current_stock = random.randint(0, 1200)
        reserved_stock = random.randint(0, min(current_stock, 200))
        available_stock = current_stock - reserved_stock

        inventory.append({
            "inventory_id": f"INV{idx + 1:06d}",
            "product_id": row["product_id"],
            "warehouse_id": row["warehouse_id"],
            "current_stock": current_stock,
            "reserved_stock": reserved_stock,
            "available_stock": available_stock,
            "safety_stock": row["safety_stock"],
            "reorder_point": row["reorder_point"],
            "last_updated": datetime.now().strftime("%Y-%m-%d")
        })

    return pd.DataFrame(inventory)


def generate_purchase_orders(products_df, suppliers_df, number_of_orders=3000):
    purchase_orders = []
    start_date = datetime(2025, 1, 1)
    end_date = datetime(2026, 6, 30)

    statuses = ["Delivered", "In Transit", "Delayed", "Open", "Cancelled"]

    for i in range(1, number_of_orders + 1):
        product = products_df.sample(1).iloc[0]
        supplier_id = product["supplier_id"]

        order_date = random_date(start_date, end_date)
        expected_delivery_date = order_date + timedelta(days=random.randint(5, 30))

        status = random.choices(
            statuses,
            weights=[60, 15, 12, 10, 3],
            k=1
        )[0]

        if status == "Delivered":
            actual_delivery_date = expected_delivery_date + timedelta(days=random.randint(-3, 5))
        elif status == "Delayed":
            actual_delivery_date = expected_delivery_date + timedelta(days=random.randint(6, 20))
        else:
            actual_delivery_date = None

        purchase_orders.append({
            "po_number": f"PO{i:06d}",
            "supplier_id": supplier_id,
            "product_id": product["product_id"],
            "quantity": random.randint(50, 2000),
            "order_date": order_date.strftime("%Y-%m-%d"),
            "expected_delivery_date": expected_delivery_date.strftime("%Y-%m-%d"),
            "actual_delivery_date": actual_delivery_date.strftime("%Y-%m-%d") if actual_delivery_date else "",
            "status": status
        })

    return pd.DataFrame(purchase_orders)


def generate_sales_orders(products_df, warehouses_df, number_of_orders=10000):
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

        sales_orders.append({
            "order_id": f"SO{i:07d}",
            "customer_name": random.choice(customer_names),
            "product_id": product["product_id"],
            "quantity": random.randint(1, 50),
            "order_date": order_date.strftime("%Y-%m-%d"),
            "warehouse_id": product["warehouse_id"]
        })

    return pd.DataFrame(sales_orders)


def generate_demand_forecast(products_df):
    forecast_rows = []

    months = pd.date_range(start="2025-01-01", end="2026-06-01", freq="MS")

    sample_products = products_df.sample(100, random_state=42)

    forecast_id = 1
    for _, product in sample_products.iterrows():
        for month in months:
            forecast_qty = random.randint(500, 5000)
            actual_qty = max(0, forecast_qty + random.randint(-500, 500))
            mape = abs(actual_qty - forecast_qty) / actual_qty * 100 if actual_qty else 0

            forecast_rows.append({
                "forecast_id": f"FC{forecast_id:07d}",
                "product_id": product["product_id"],
                "month": month.strftime("%Y-%m"),
                "forecast_quantity": forecast_qty,
                "actual_quantity": actual_qty,
                "mape": round(mape, 2)
            })

            forecast_id += 1

    return pd.DataFrame(forecast_rows)


def generate_shipments(purchase_orders_df, warehouses_df):
    shipments = []
    carriers = ["FedEx", "UPS", "DHL", "XPO Logistics", "J.B. Hunt", "Ryder"]
    destinations = ["Dallas, TX", "Chicago, IL", "Atlanta, GA", "Seattle, WA", "New York, NY"]

    for i in range(1, 2501):
        po = purchase_orders_df.sample(1).iloc[0]

        status = random.choice(["Delivered", "In Transit", "Delayed", "Exception"])

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


def generate_returns(products_df, warehouses_df, number_of_returns=1200):
    reasons = ["Damaged", "Wrong Item", "Late Delivery", "Quality Issue", "Customer Changed Mind"]
    returns = []

    for i in range(1, number_of_returns + 1):
        product = products_df.sample(1).iloc[0]
        return_date = random_date(datetime(2025, 1, 1), datetime(2026, 6, 30))

        returns.append({
            "return_id": f"RET{i:06d}",
            "product_id": product["product_id"],
            "return_reason": random.choice(reasons),
            "warehouse_id": random.choice(warehouses_df["warehouse_id"].tolist()),
            "quantity": random.randint(1, 20),
            "return_date": return_date.strftime("%Y-%m-%d")
        })

    return pd.DataFrame(returns)


def main():
    suppliers_df = generate_suppliers()
    warehouses_df = generate_warehouses()
    products_df = generate_products(suppliers_df, warehouses_df)
    inventory_df = generate_inventory(products_df)
    purchase_orders_df = generate_purchase_orders(products_df, suppliers_df)
    sales_orders_df = generate_sales_orders(products_df, warehouses_df)
    demand_forecast_df = generate_demand_forecast(products_df)
    shipments_df = generate_shipments(purchase_orders_df, warehouses_df)
    returns_df = generate_returns(products_df, warehouses_df)

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
    }

    for file_name, dataframe in datasets.items():
        output_path = DATA_DIR / file_name
        dataframe.to_csv(output_path, index=False)
        print(f"Created {output_path} with {len(dataframe)} rows")

    print("\nERP data generation completed successfully!")


if __name__ == "__main__":
    main()