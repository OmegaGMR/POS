import pandas as pd
import os
from datetime import datetime

SALES_FILE = "data/sales.csv"


def load_sales():

    if os.path.exists(SALES_FILE):

        return pd.read_csv(SALES_FILE)

    return pd.DataFrame(
        columns=[
            "Date",
            "Subtotal",
            "GST",
            "Total",
            "Items"
        ]
    )


def save_sale(
    subtotal,
    tax,
    total,
    item_count
):

    sale = pd.DataFrame([
        {
            "Date": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "Subtotal": subtotal,
            "GST": tax,
            "Total": total,
            "Items": item_count
        }
    ])

    if os.path.exists(SALES_FILE):

        sale.to_csv(
            SALES_FILE,
            mode="a",
            header=False,
            index=False
        )

    else:

        sale.to_csv(
            SALES_FILE,
            index=False
        )