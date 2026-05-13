
import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.title("Document Scanner")

uploaded = st.file_uploader("Upload image", type=["jpg", "png", "jpeg"])

if uploaded:
    file_bytes = np.asarray(bytearray(uploaded.read()), dtype=np.uint8)

    img = cv2.imdecode(file_bytes, 1)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]

    st.image(thresh, channels="GRAY")
