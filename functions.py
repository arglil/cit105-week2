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


def initials(full_name):
    """Return the uppercase initials of each word in a full name."""
    if not isinstance(full_name, str):
        raise TypeError("full_name must be a string.")

    words = full_name.split()
    if not words:
        return ""

    return "".join(word[0].upper() for word in words)


def is_valid_url(text):
    """Return True if text is a valid URL and False otherwise."""
    if not isinstance(text, str):
        return False

    text = text.strip()
    if not text:
        return False

    if any(ch.isspace() for ch in text):
        return False

    if "://" not in text:
        return False

    scheme, rest = text.split("://", 1)
    if scheme not in ("http", "https"):
        return False
    if not rest:
        return False

    domain = rest.split("/", 1)[0]
    if not domain or "." not in domain:
        return False

    return True


def truncate(text, limit=50):
    """Return text with an ellipsis if it exceeds the given character limit."""
    if not isinstance(text, str):
        raise TypeError("text must be a string.")
    if not isinstance(limit, int) or isinstance(limit, bool):
        raise TypeError("limit must be an integer.")
    if limit < 0:
        raise ValueError("limit must be non-negative.")

    if len(text) <= limit:
        return text

    if limit <= 3:
        return "." * limit

    return text[: limit - 3] + "..."
