import streamlit as st
import pandas as pd

from services.cart_service import add_to_cart
from services.inventory_service import (
    load_products,
    save_products,
    check_stock,
    deduct_stock
)
from services.sales_service import (
    load_sales,
    save_sale
)
from utils.calculations import (
    calculate_subtotal,
    calculate_tax,
    calculate_total
)

st.set_page_config(
    page_title="POS System",
    page_icon="🛒",
    layout="wide"
)

# -----------------------------
# Session State
# -----------------------------

if "cart" not in st.session_state:
    st.session_state.cart = []

# -----------------------------
# Load Data
# -----------------------------

products_df = load_products()

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

        st.warning(
            "No products are currently in stock."
        )

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

        price = float(product_row["Price"])
        stock = int(product_row["Stock"])

        with col2:

            quantity = st.number_input(
                "Quantity",
                min_value=1,
                max_value=stock,
                step=1
            )

        st.write(
            f"Price: ${price:.2f}"
        )

        st.write(
            f"Available Stock: {stock}"
        )

        # -----------------------------
        # Add To Cart
        # -----------------------------

        if st.button("Add to Cart"):

            st.session_state.cart = add_to_cart(
                st.session_state.cart,
                product,
                quantity,
                price
            )

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

        subtotal = calculate_subtotal(
            st.session_state.cart
        )

        tax = calculate_tax(
            subtotal
        )

        total = calculate_total(
            subtotal,
            tax
        )

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

                # Check stock for every cart item
                for item in st.session_state.cart:

                    if not check_stock(
                        products_df,
                        item["Product"],
                        item["Quantity"]
                    ):

                        enough_stock = False

                        st.error(
                            f"Not enough stock for "
                            f"{item['Product']}."
                        )

                if enough_stock:

                    # Deduct stock
                    for item in st.session_state.cart:

                        products_df = deduct_stock(
                            products_df,
                            item["Product"],
                            item["Quantity"]
                        )

                    save_products(
                        products_df
                    )

                    # Save sale
                    item_count = sum(
                        item["Quantity"]
                        for item
                        in st.session_state.cart
                    )

                    save_sale(
                        subtotal,
                        tax,
                        total,
                        item_count
                    )

                    # Clear cart
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

    total_units = products_df[
        "Stock"
    ].sum()

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

    sales_df = load_sales()

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

        total_revenue = sales_df[
            "Total"
        ].sum()

        total_transactions = len(
            sales_df
        )

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