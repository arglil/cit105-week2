def celsius_to_fahrenheit(c):
    """Convert a temperature in Celsius to Fahrenheit."""
    if not isinstance(c, (int, float)) or isinstance(c, bool):
        raise TypeError("c must be a number (int or float).")
    return (c * 9 / 5) + 32
