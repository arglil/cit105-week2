def celsius_to_fahrenheit(c):
    """Convert a temperature in Celsius to Fahrenheit."""
    if not isinstance(c, (int, float)) or isinstance(c, bool):
        raise TypeError("c must be a number (int or float).")
    return (c * 9 / 5) + 32


def line_total(price, qty):
    """Return the total cost for a given price and quantity."""
    if not isinstance(price, (int, float)) or isinstance(price, bool):
        raise TypeError("price must be a number (int or float).")
    if not isinstance(qty, (int, float)) or isinstance(qty, bool):
        raise TypeError("qty must be a number (int or float).")
    if qty < 0:
        raise ValueError("qty must be non-negative.")
    return price * qty
