import pandas as pd

PRODUCT_FILE = "data/products.csv"


def load_products():
    return pd.read_csv(PRODUCT_FILE)


def save_products(products_df):
    products_df.to_csv(
        PRODUCT_FILE,
        index=False
    )


def get_product(products_df, product_name):

    product = products_df[
        products_df["Product"] == product_name
    ]

    if product.empty:
        return None

    return product.iloc[0]


def check_stock(
    products_df,
    product_name,
    quantity
):

    product = get_product(
        products_df,
        product_name
    )

    if product is None:
        return False

    return quantity <= product["Stock"]


def deduct_stock(
    products_df,
    product_name,
    quantity
):

    products_df.loc[
        products_df["Product"] == product_name,
        "Stock"
    ] -= quantity

    return products_df

