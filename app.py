import csv
import io
import zipfile

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


def read_batch_csv(uploaded_file):
    """Read a CSV file and separate valid rows from rejected rows."""
    valid_rows = []
    rejected_rows = []

    try:
        text = uploaded_file.getvalue().decode("utf-8-sig")
        reader = csv.DictReader(io.StringIO(text))

        if reader.fieldnames is None:
            return [], ["CSV file is empty or has no header row."]

        fieldnames = [
            field.strip().lower() if field else ""
            for field in reader.fieldnames
        ]

        if "name" not in fieldnames or "url" not in fieldnames:
            return [], [
                "CSV must contain both required columns: name and url."
            ]

        # Map normalized column names back to their original names.
        name_column = reader.fieldnames[fieldnames.index("name")]
        url_column = reader.fieldnames[fieldnames.index("url")]

        for row_number, row in enumerate(reader, start=2):
            name = (row.get(name_column) or "").strip()
            url = (row.get(url_column) or "").strip()

            if not name and not url:
                rejected_rows.append(
                    f"Row {row_number}: row contains only whitespace or is blank."
                )
                continue

            if not name:
                rejected_rows.append(
                    f"Row {row_number}: name is blank."
                )
                continue

            if not url:
                rejected_rows.append(
                    f"Row {row_number}: URL is blank."
                )
                continue

            valid_rows.append(
                {
                    "name": name,
                    "url": url,
                }
            )

    except UnicodeDecodeError:
        return [], ["The CSV file could not be read as UTF-8 text."]
    except csv.Error as error:
        return [], [f"CSV error: {error}"]

    return valid_rows, rejected_rows


def create_batch_zip(rows):
    """Generate one QR code per valid row and return an in-memory ZIP file."""
    zip_buffer = io.BytesIO()
    used_names = {}

    with zipfile.ZipFile(
        zip_buffer,
        mode="w",
        compression=zipfile.ZIP_DEFLATED,
    ) as zip_file:
        for row in rows:
            qr_image = generate_qr_code(row["url"])

            base_name = safe_filename(row["name"]) or "qr_code"

            if base_name in used_names:
                used_names[base_name] += 1
                file_name = f"{base_name}_{used_names[base_name]}.png"
            else:
                used_names[base_name] = 1
                file_name = f"{base_name}.png"

            png_buffer = io.BytesIO()
            qr_image.save(png_buffer, format="PNG")
            png_buffer.seek(0)

            zip_file.writestr(file_name, png_buffer.getvalue())

    zip_buffer.seek(0)
    return zip_buffer


st.title("QR Code Generator")

mode = st.radio(
    "Choose a mode",
    ["Single code", "Batch from CSV"],
    horizontal=True,
)


if mode == "Single code":
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
    elif len(user_input) > MAX_LENGTH:
        st.error("Please keep the input to 1,000 characters or fewer.")
    else:
        if looks_like_malformed_url(user_input):
            st.warning(
                "This looks like a malformed URL, "
                "but the QR code can still be generated."
            )

        size = st.slider(
            "Image size in pixels",
            min_value=MIN_SIZE,
            max_value=MAX_SIZE,
            value=300,
            step=10,
        )
        st.caption("Range: 200 to 1000 pixels.")

        foreground_color = st.color_picker(
            "Foreground color",
            "#000000",
        )
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

        st.image(
            qr_image,
            caption="Scannable QR code",
            use_container_width=False,
        )

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


else:
    st.write(
        "Upload a CSV file containing the columns `name` and `url`."
    )

    uploaded_file = st.file_uploader(
        "Upload CSV",
        type=["csv"],
    )

    if uploaded_file is not None:
        valid_rows, rejected_rows = read_batch_csv(uploaded_file)

        st.subheader("Batch Preview")

        col1, col2 = st.columns(2)
        col1.metric("Valid rows", len(valid_rows))
        col2.metric("Rejected rows", len(rejected_rows))

        if valid_rows:
            st.write("Valid rows:")
            st.dataframe(valid_rows, use_container_width=True)

        if rejected_rows:
            st.write("Rejected rows:")
            for message in rejected_rows:
                st.warning(message)

        if valid_rows:
            zip_buffer = create_batch_zip(valid_rows)

            st.success(
                f"{len(valid_rows)} QR code(s) are ready to download."
            )

            st.download_button(
                label="Download QR Codes ZIP",
                data=zip_buffer.getvalue(),
                file_name="qr_codes.zip",
                mime="application/zip",
            )
        else:
            st.error("No valid rows were found, so no QR codes were generated.")