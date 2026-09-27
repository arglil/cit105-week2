# QR Code Generator Specification

Build a QR code generator as a Streamlit application.

## Inputs

- Accept text or a URL from the user.
- State the maximum input length.

## Outputs

- Show a preview of the generated code on screen.
- Provide a download button for the PNG file.
- Define the downloaded filename.

## Options

- Let the user set the image size.
- Let the user choose the foreground color.
- Let the user set the quiet zone border.

## Error Handling

- Reject empty input with a clear message.
- Flag input that looks like a malformed URL.
- Reject input that is only whitespace.

## Constraints

- Name the library to use: qrcode plus Pillow.
- Generate the image in memory, not as a temporary file.
- Put generation in its own function, separate from the interface.

## Specification Completeness

100%. Nothing is left undefined.
