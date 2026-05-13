
import streamlit as st
from PIL import Image, ImageOps, ImageFilter
from fpdf import FPDF
import tempfile
import os

st.set_page_config(page_title="Document Scanner", layout="centered")

st.title("📄 Document Scanner")
st.write("Upload a document image, convert it to black & white, and download it as a PDF.")

uploaded_file = st.file_uploader(
    "Upload an image",
    type=["jpg", "jpeg", "png"]
)

def process_image(image):
    # Convert to grayscale
    gray = ImageOps.grayscale(image)

    # Increase contrast for scan-like effect
    bw = gray.point(lambda x: 0 if x < 140 else 255, '1')

    # Slight sharpening
    bw = bw.filter(ImageFilter.SHARPEN)

    return bw.convert("RGB")

def image_to_pdf(image):
    # Save temporary image
    temp_img = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
    image.save(temp_img.name, "JPEG")

    # Create PDF
    pdf = FPDF()
    pdf.add_page()

    # A4 size
    page_width = 190
    img_width, img_height = image.size

    ratio = img_height / img_width
    pdf_height = page_width * ratio

    pdf.image(temp_img.name, x=10, y=10, w=page_width, h=pdf_height)

    temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(temp_pdf.name)

    return temp_pdf.name

if uploaded_file:
    image = Image.open(uploaded_file)

    st.subheader("Original Image")
    st.image(image, use_container_width=True)

    if st.button("Convert to Scan PDF"):
        with st.spinner("Processing..."):

            processed_image = process_image(image)

            st.subheader("Scanned Preview")
            st.image(processed_image, use_container_width=True)

            pdf_path = image_to_pdf(processed_image)

            with open(pdf_path, "rb") as pdf_file:
                st.download_button(
                    label="📥 Download PDF",
                    data=pdf_file,
                    file_name="scanned_document.pdf",
                    mime="application/pdf"
                )

            # Cleanup temp files
            os.unlink(pdf_path)
