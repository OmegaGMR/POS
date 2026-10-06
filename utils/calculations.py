def calculate_subtotal(cart):

    subtotal = 0

    for item in cart:
        subtotal += item["Total"]

    return subtotal


def calculate_tax(subtotal, tax_rate=0.05):

    return subtotal * tax_rate


def calculate_total(subtotal, tax):

    return subtotal + tax