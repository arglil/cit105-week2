import io

import streamlit as st
import qrcode
from PIL import Image

from functions import safe_filename


MAX_LENGTH = 1000
MIN_SIZE = 200
MAX_SIZE = 1000
MIN_BORDER = 1
MAX_BORDER = 10


def looks_like_malformed_url(text):
    """Return True when text seems like a malformed URL and False otherwise."""
    if not isinstance(text, str):
        return False

    text = text.strip()
    if not text:
        return False

    if text.startswith(("http://", "https://")):
        if " " in text:
            return True
        if "://" not in text:
            return True
        host = text.split("://", 1)[1]
        if not host or "/" not in host and "." not in host:
            return True
        return False

    if text.startswith("www."):
        return True

    if "http" in text.lower() or "://" in text:
        return True

    return False


def generate_qr_code(data, size=300, color="black", border=4):
    """Create a QR code image from text or a URL."""
    if size <= 0:
        raise ValueError("size must be greater than 0.")

    box_size = max(1, int(size / 29))
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)

    image = qr.make_image(fill_color=color, back_color="white")
    width, height = image.size
    if width != size or height != size:
        image = image.resize((size, size), resample=Image.Resampling.NEAREST)
    return image


st.title("QR Code Generator")
st.write("Enter text or a URL to make a QR code.")

user_input = st.text_area(
    "Your text or URL",
    value="",
    height=150,
    max_chars=MAX_LENGTH,
)

char_count = len(user_input)
st.caption(f"Characters: {char_count}/{MAX_LENGTH}")

if user_input.strip() == "":
    st.warning("Please enter text or a URL before generating a QR code.")
    st.stop()

if len(user_input) > MAX_LENGTH:
    st.error("Please keep the input to 1,000 characters or fewer.")
    st.stop()

if looks_like_malformed_url(user_input):
    st.warning(
        "This looks like a malformed URL, but the QR code can still be generated."
    )

size = st.slider(
    "Image size in pixels",
    min_value=MIN_SIZE,
    max_value=MAX_SIZE,
    value=300,
    step=10,
)
st.caption("Range: 200 to 1000 pixels.")

foreground_color = st.color_picker("Foreground color", "#000000")
st.caption("Pick any color for the QR code pattern.")

border_width = st.slider(
    "QR quiet-zone border width",
    min_value=MIN_BORDER,
    max_value=MAX_BORDER,
    value=4,
    step=1,
)
st.caption("Range: 1 to 10 modules.")

qr_image = generate_qr_code(
    user_input,
    size=size,
    color=foreground_color,
    border=border_width,
)

st.image(qr_image, caption="Scannable QR code", use_container_width=False)

file_name = safe_filename(user_input.strip()) or "qr_code"
file_name = file_name + ".png"

png_buffer = io.BytesIO()
qr_image.save(png_buffer, format="PNG")
png_buffer.seek(0)

st.download_button(
    label="Download PNG",
    data=png_buffer.getvalue(),
    file_name=file_name,
    mime="image/png",
)
