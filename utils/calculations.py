def calculate_subtotal(cart):
    subtotal = 0

    for item in cart:
        subtotal += item["Total"]

    return subtotal


def calculate_tax(subtotal, tax_rate=0.05):
    return subtotal * tax_rate


def calculate_total(subtotal, tax):
    return subtotal + tax

from utils.calculations import (
    calculate_subtotal,
    calculate_tax,
    calculate_total
)

subtotal = calculate_subtotal(st.session_state.cart)

tax = calculate_tax(subtotal)

total = calculate_total(subtotal, tax)

