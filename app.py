import streamlit as st
from PIL import Image, ImageOps, ImageFilter
from fpdf import FPDF
import tempfile
import os

st.set_page_config(page_title="Adobe Scan Clone", layout="centered")

st.title("📄 Adobe Scan Style App")

uploaded_file = st.file_uploader(
    "Upload Document Image",
    type=["png", "jpg", "jpeg"]
)

def make_scan(image):
    # Convert to grayscale
    gray = ImageOps.grayscale(image)

    # Improve scan appearance
    bw = gray.point(lambda x: 0 if x < 150 else 255, '1')

    # Sharpen
    bw = bw.filter(ImageFilter.SHARPEN)

    return bw.convert("RGB")

def create_pdf(image):
    temp_image = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
    image.save(temp_image.name)

    pdf = FPDF()
    pdf.add_page()

    pdf.image(temp_image.name, x=10, y=10, w=190)

    temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(temp_pdf.name)

    return temp_pdf.name

if uploaded_file is not None:

    image = Image.open(uploaded_file)

    st.subheader("Original Image")
    st.image(image, use_container_width=True)

    if st.button("Convert to PDF"):

        scanned = make_scan(image)

        st.subheader("Scanned Version")
        st.image(scanned, use_container_width=True)

        pdf_file = create_pdf(scanned)

        with open(pdf_file, "rb") as f:
            st.download_button(
                "⬇ Download PDF",
                data=f,
                file_name="scanned_document.pdf",
                mime="application/pdf"
            )

        os.remove(pdf_file)
