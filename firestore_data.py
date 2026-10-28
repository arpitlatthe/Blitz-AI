import pandas as pd
from firebase_config import db


def load_data_from_firestore():

    orders = db.collection("orders").stream()

    data = []

    for order in orders:
        data.append(order.to_dict())

    df = pd.DataFrame(data)

    if not df.empty:

        df["Date"] = pd.to_datetime(
            df["Date"]
        )

        numeric_columns = [
            "Quantity",
            "Sales",
            "Cost",
            "Profit"
        ]

        for column in numeric_columns:

            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

    return df