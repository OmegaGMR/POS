import streamlit as st

st.set_page_config(
    page_title="POS System",
    page_icon="🛒",
    layout="wide"
)

st.title("POS System")

page = st.sidebar.radio(
    "Navigation",
    ["POS", "Inventory", "Sales"]
)

if page == "POS":
    st.header("Point of Sale")

    product = st.selectbox(
        "Select Product",
        ["Coffee", "Muffin", "Sandwich", "Water"]
    )

    quantity = st.number_input(
        "Quantity",
        min_value=1,
        step=1
    )

    if st.button("Add to Cart"):
        st.success(f"Added {quantity} x {product}")

elif page == "Inventory":
    st.header("Inventory")

    st.write("Inventory page")

elif page == "Sales":
    st.header("Sales History")

    st.write("Sales page")