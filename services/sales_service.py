import pandas as pd
import os
from datetime import datetime

SALES_FILE = "data/sales.csv"


def load_sales():

    if not os.path.exists(SALES_FILE):

        return pd.DataFrame(
            columns=[
                "Date",
                "Subtotal",
                "GST",
                "Total",
                "Items",
                "OrderDetails"
            ]
        )

    return pd.read_csv(SALES_FILE)


def save_sale(
    subtotal,
    tax,
    total,
    item_count,
    cart
):

    os.makedirs("data", exist_ok=True)

    order_details = ", ".join(
        f"{item['Product']} x{item['Quantity']}"
        for item in cart
    )

    new_sale = pd.DataFrame([
        {
            "Date": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "Subtotal": float(subtotal),
            "GST": float(tax),
            "Total": float(total),
            "Items": int(item_count),
            "OrderDetails": order_details
        }
    ])

    existing_sales = load_sales()

    updated_sales = pd.concat(
        [
            existing_sales,
            new_sale
        ],
        ignore_index=True
    )

    updated_sales.to_csv(
        SALES_FILE,
        index=False
    )