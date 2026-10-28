import pandas as pd
from firebase_config import db


CSV_PATH = "data/ecommerce_data.csv"


df = pd.read_csv(CSV_PATH)


print("Uploading data to Firebase Firestore...")


collection = db.collection("orders")


for _, row in df.iterrows():

    order_id = str(row["Order_ID"])

    data = {
        "Order_ID": order_id,
        "Date": str(row["Date"]),
        "Customer": str(row["Customer"]),
        "Product": str(row["Product"]),
        "Category": str(row["Category"]),
        "Region": str(row["Region"]),
        "Quantity": int(row["Quantity"]),
        "Sales": float(row["Sales"]),
        "Cost": float(row["Cost"]),
        "Profit": float(row["Profit"])
    }

    collection.document(order_id).set(data)


print(f"✅ {len(df)} orders uploaded to Firebase Firestore!")