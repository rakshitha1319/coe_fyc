import streamlit as st
from PIL import Image
import cv2
import numpy as np

st.title("AI Document Scanner")

file = st.file_uploader("Upload Image")

if file:
    image = Image.open(file)
    img = np.array(image)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    scan = cv2.adaptiveThreshold(
        gray,255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,2
    )

    st.image(scan, caption="Scanned Image")
