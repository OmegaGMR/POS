def add_to_cart(
    cart,
    product,
    quantity,
    price
):

    for item in cart:

        if item["Product"] == product:

            item["Quantity"] += quantity

            item["Total"] = (
                item["Quantity"]
                * item["Price"]
            )

            return cart

    cart.append(
        {
            "Product": product,
            "Quantity": quantity,
            "Price": price,
            "Total": price * quantity
        }
    )

    return cart



