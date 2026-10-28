import pandas as pd
import os


def load_data_from_firestore():

    file_path = os.path.join(
        os.path.dirname(__file__),
        "data",
        "ecommerce_data.csv"
    )

    df = pd.read_csv(file_path)

    df["Date"] = pd.to_datetime(df["Date"])

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