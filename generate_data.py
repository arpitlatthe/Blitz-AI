import pandas as pd
import random
from datetime import datetime, timedelta

random.seed(42)

products = {
    "Laptop": ("Electronics", 55000, 45000),
    "Smartphone": ("Electronics", 30000, 24000),
    "Monitor": ("Electronics", 18000, 14000),
    "Headphones": ("Electronics", 5000, 3500),
    "Keyboard": ("Accessories", 2500, 1600),
    "Mouse": ("Accessories", 1200, 700),
    "Webcam": ("Accessories", 3500, 2200),
    "USB Hub": ("Accessories", 1800, 1000),
    "Office Chair": ("Furniture", 12000, 8500),
    "Desk": ("Furniture", 15000, 10500),
    "Bookshelf": ("Furniture", 9000, 6000),
    "Table Lamp": ("Furniture", 2500, 1400),
    "Tablet": ("Electronics", 22000, 17000),
    "Printer": ("Electronics", 14000, 10500),
    "External SSD": ("Electronics", 8000, 5500)
}

customers = [f"Customer_{i:03d}" for i in range(1, 101)]

regions = [
    "North",
    "South",
    "East",
    "West",
    "Central"
]

data = []

start_date = datetime(2025, 1, 1)

for order_number in range(1, 501):

    order_id = f"ORD{order_number:04d}"

    date = start_date + timedelta(
        days=random.randint(0, 364)
    )

    customer = random.choice(customers)

    product = random.choice(list(products.keys()))

    category, selling_price, cost_price = products[product]

    quantity = random.randint(1, 5)

    sales = selling_price * quantity

    cost = cost_price * quantity

    profit = sales - cost

    region = random.choice(regions)

    data.append([
        order_id,
        date.strftime("%Y-%m-%d"),
        customer,
        product,
        category,
        region,
        quantity,
        sales,
        cost,
        profit
    ])

df = pd.DataFrame(
    data,
    columns=[
        "Order_ID",
        "Date",
        "Customer",
        "Product",
        "Category",
        "Region",
        "Quantity",
        "Sales",
        "Cost",
        "Profit"
    ]
)

df.to_csv(
    "data/ecommerce_data.csv",
    index=False
)

print("✅ Dataset created successfully!")
print(f"Total Orders: {len(df)}")
print(f"Total Customers: {df['Customer'].nunique()}")
print(f"Total Revenue: ₹{df['Sales'].sum():,.0f}")
print(f"Total Profit: ₹{df['Profit'].sum():,.0f}")
