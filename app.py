import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(
    page_title="POS System",
    page_icon="🛒",
    layout="wide"
)

# -----------------------------
# File Paths
# -----------------------------

PRODUCT_FILE = "data/products.csv"
SALES_FILE = "data/sales.csv"

# -----------------------------
# Load Data
# -----------------------------

products_df = pd.read_csv(PRODUCT_FILE)

if os.path.exists(SALES_FILE):
    sales_df = pd.read_csv(SALES_FILE)
else:
    sales_df = pd.DataFrame(
        columns=[
            "Date",
            "Subtotal",
            "GST",
            "Total",
            "Items"
        ]
    )

# -----------------------------
# Session State
# -----------------------------

if "cart" not in st.session_state:
    st.session_state.cart = []

# -----------------------------
# Navigation
# -----------------------------

st.title("POS System")

page = st.sidebar.radio(
    "Navigation",
    ["POS", "Inventory", "Sales"]
)

# -----------------------------
# POS Page
# -----------------------------

if page == "POS":

    st.header("Point of Sale")

    available_products = products_df[
        products_df["Stock"] > 0
    ]

    if available_products.empty:

        st.warning("No products are currently in stock.")

    else:

        col1, col2 = st.columns(2)

        with col1:

            product = st.selectbox(
                "Select Product",
                available_products["Product"].tolist()
            )

        product_row = products_df[
            products_df["Product"] == product
        ].iloc[0]

        price = product_row["Price"]
        stock = int(product_row["Stock"])

        with col2:

            quantity = st.number_input(
                "Quantity",
                min_value=1,
                max_value=stock,
                step=1
            )

        st.write(f"Price: ${price:.2f}")
        st.write(f"Available Stock: {stock}")

        # -----------------------------
        # Add to Cart
        # -----------------------------

        if st.button("Add to Cart"):

            item = {
                "Product": product,
                "Quantity": quantity,
                "Price": price,
                "Total": price * quantity
            }

            st.session_state.cart.append(item)

            st.success(
                f"Added {quantity} x {product}"
            )

    # -----------------------------
    # Cart
    # -----------------------------

    st.subheader("Cart")

    if len(st.session_state.cart) == 0:

        st.write("Cart is empty.")

    else:

        cart_df = pd.DataFrame(
            st.session_state.cart
        )

        st.dataframe(
            cart_df,
            use_container_width=True,
            hide_index=True
        )

        subtotal = cart_df["Total"].sum()
        tax = subtotal * 0.05
        total = subtotal + tax

        st.divider()

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Subtotal",
                f"${subtotal:.2f}"
            )

        with col2:

            st.metric(
                "GST",
                f"${tax:.2f}"
            )

        with col3:

            st.metric(
                "Total",
                f"${total:.2f}"
            )

        st.divider()

        checkout_col, clear_col = st.columns(2)

        # -----------------------------
        # Checkout
        # -----------------------------

        with checkout_col:

            if st.button(
                "Checkout",
                use_container_width=True
            ):

                enough_stock = True

                # Check all stock before completing sale
                for item in st.session_state.cart:

                    product_name = item["Product"]
                    quantity_needed = item["Quantity"]

                    current_stock = products_df.loc[
                        products_df["Product"] == product_name,
                        "Stock"
                    ].iloc[0]

                    if quantity_needed > current_stock:

                        enough_stock = False

                        st.error(
                            f"Not enough stock for {product_name}."
                        )

                if enough_stock:

                    # -----------------------------
                    # Deduct Inventory
                    # -----------------------------

                    for item in st.session_state.cart:

                        product_name = item["Product"]
                        quantity_sold = item["Quantity"]

                        products_df.loc[
                            products_df["Product"] == product_name,
                            "Stock"
                        ] -= quantity_sold

                    products_df.to_csv(
                        PRODUCT_FILE,
                        index=False
                    )

                    # -----------------------------
                    # Save Sale
                    # -----------------------------

                    new_sale = pd.DataFrame([
                        {
                            "Date": datetime.now().strftime(
                                "%Y-%m-%d %H:%M:%S"
                            ),
                            "Subtotal": subtotal,
                            "GST": tax,
                            "Total": total,
                            "Items": cart_df["Quantity"].sum()
                        }
                    ])

                    if os.path.exists(SALES_FILE):

                        new_sale.to_csv(
                            SALES_FILE,
                            mode="a",
                            header=False,
                            index=False
                        )

                    else:

                        new_sale.to_csv(
                            SALES_FILE,
                            index=False
                        )

                    st.session_state.cart = []

                    st.success(
                        "Sale completed successfully."
                    )

                    st.rerun()

        # -----------------------------
        # Clear Cart
        # -----------------------------

        with clear_col:

            if st.button(
                "Clear Cart",
                use_container_width=True
            ):

                st.session_state.cart = []

                st.rerun()

# -----------------------------
# Inventory Page
# -----------------------------

elif page == "Inventory":

    st.header("Inventory")

    st.dataframe(
        products_df,
        use_container_width=True,
        hide_index=True
    )

    total_units = products_df["Stock"].sum()

    inventory_value = (
        products_df["Price"]
        * products_df["Stock"]
    ).sum()

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Total Units",
            int(total_units)
        )

    with col2:

        st.metric(
            "Inventory Value",
            f"${inventory_value:.2f}"
        )

# -----------------------------
# Sales Page
# -----------------------------

elif page == "Sales":

    st.header("Sales History")

    if not os.path.exists(SALES_FILE):

        st.write(
            "No sales have been completed yet."
        )

    else:

        sales_df = pd.read_csv(SALES_FILE)

        if sales_df.empty:

            st.write(
                "No sales have been completed yet."
            )

        else:

            st.dataframe(
                sales_df,
                use_container_width=True,
                hide_index=True
            )

            total_revenue = sales_df["Total"].sum()

            total_transactions = len(sales_df)

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "Total Revenue",
                    f"${total_revenue:.2f}"
                )

            with col2:

                st.metric(
                    "Transactions",
                    total_transactions
                )