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

# -----------------------------
# Page Setup
# -----------------------------

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
# Load Product Data
# -----------------------------

products_df = load_products()

# -----------------------------
# Main Title
# -----------------------------

st.title("POS System")

# -----------------------------
# Navigation
# -----------------------------

page = st.sidebar.radio(
    "Navigation",
    [
        "POS",
        "Inventory",
        "Sales"
    ]
)

# =========================================================
# POS PAGE
# =========================================================

if page == "POS":

    st.header("Point of Sale")

    # -----------------------------
    # Available Products
    # -----------------------------

    available_products = products_df[
        products_df["Stock"] > 0
    ]

    if available_products.empty:

        st.warning(
            "No products are currently in stock."
        )

    else:

        col1, col2 = st.columns(2)

        # -----------------------------
        # Product Selection
        # -----------------------------

        with col1:

            product = st.selectbox(
                "Select Product",
                available_products["Product"].tolist()
            )

        # Get selected product row
        product_row = products_df[
            products_df["Product"] == product
        ].iloc[0]

        price = float(
            product_row["Price"]
        )

        stock = int(
            product_row["Stock"]
        )

        # -----------------------------
        # Quantity Selection
        # -----------------------------

        with col2:

            quantity = st.number_input(
                "Quantity",
                min_value=1,
                max_value=stock,
                step=1
            )

        # -----------------------------
        # Product Information
        # -----------------------------

        st.write(
            f"Price: ${price:.2f}"
        )

        st.write(
            f"Available Stock: {stock}"
        )

        # -----------------------------
        # Add To Cart
        # -----------------------------

        if st.button(
            "Add to Cart"
        ):

            st.session_state.cart = add_to_cart(
                st.session_state.cart,
                product,
                quantity,
                price
            )

            st.success(
                f"Added {quantity} x {product}"
            )

    # =====================================================
    # CART
    # =====================================================

    st.subheader("Cart")

    if len(st.session_state.cart) == 0:

        st.write(
            "Cart is empty."
        )

    else:

        # -----------------------------
        # Cart DataFrame
        # -----------------------------

        cart_df = pd.DataFrame(
            st.session_state.cart
        )

        st.dataframe(
            cart_df,
            use_container_width=True,
            hide_index=True
        )

        # -----------------------------
        # Calculations
        # -----------------------------

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

        # -----------------------------
        # Totals
        # -----------------------------

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

        # =================================================
        # CHECKOUT
        # =================================================

        with checkout_col:

            if st.button(
                "Checkout",
                use_container_width=True
            ):

                enough_stock = True

                # -----------------------------
                # Check Inventory
                # -----------------------------

                for item in st.session_state.cart:

                    stock_available = check_stock(
                        products_df,
                        item["Product"],
                        item["Quantity"]
                    )

                    if not stock_available:

                        enough_stock = False

                        st.error(
                            f"Not enough stock for "
                            f"{item['Product']}."
                        )

                # -----------------------------
                # Complete Sale
                # -----------------------------

                if enough_stock:

                    # Deduct inventory
                    for item in st.session_state.cart:

                        products_df = deduct_stock(
                            products_df,
                            item["Product"],
                            item["Quantity"]
                        )

                    # Save updated inventory
                    save_products(
                        products_df
                    )

                    # -----------------------------
                    # Count Items Sold
                    # -----------------------------

                    item_count = sum(
                        item["Quantity"]
                        for item in st.session_state.cart
                    )

                    # -----------------------------
                    # Save Sale
                    # -----------------------------

                    save_sale(
                        subtotal,
                        tax,
                        total,
                        item_count,
                        st.session_state.cart
                    )

                    # -----------------------------
                    # Clear Cart
                    # -----------------------------

                    st.session_state.cart = []

                    st.success(
                        "Sale completed successfully."
                    )

                    st.rerun()

        # =================================================
        # CLEAR CART
        # =================================================

        with clear_col:

            if st.button(
                "Clear Cart",
                use_container_width=True
            ):

                st.session_state.cart = []

                st.rerun()

# =========================================================
# INVENTORY PAGE
# =========================================================

elif page == "Inventory":

    st.header(
        "Inventory"
    )

    # -----------------------------
    # Inventory Table
    # -----------------------------

    st.dataframe(
        products_df,
        use_container_width=True,
        hide_index=True
    )

    # -----------------------------
    # Inventory Metrics
    # -----------------------------

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

# =========================================================
# SALES PAGE
# =========================================================

elif page == "Sales":

    st.header(
        "Sales History"
    )

    # -----------------------------
    # Load Sales Data
    # -----------------------------

    sales_df = load_sales()

    if sales_df.empty:

        st.write(
            "No sales have been completed yet."
        )

    else:

        # -----------------------------
        # Sales Table
        # -----------------------------

        st.dataframe(
            sales_df,
            use_container_width=True,
            hide_index=True
        )

        # -----------------------------
        # Sales Metrics
        # -----------------------------

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