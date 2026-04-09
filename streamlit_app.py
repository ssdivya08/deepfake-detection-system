import streamlit as st
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from PIL import Image
st.set_page_config(page_title="Deepfake Detector", layout="wide")
st.title("AI Deepfake Face Detection")

model = load_model("deepfake_detector.h5", compile=False)

IMG_SIZE = (160,160)

uploaded_file = st.file_uploader("Upload Face Image", type=["jpg","png","jpeg"])

if uploaded_file is not None:

    img = Image.open(uploaded_file)

    img_resized = img.resize(IMG_SIZE)
    img_array = image.img_to_array(img_resized)
    img_array = img_array/255.0
    img_array = np.expand_dims(img_array, axis=0)

    with st.spinner("Analyzing image..."):
        prediction = model.predict(img_array)[0][0]

    col1, col2 = st.columns(2)

    with col1:
        st.image(img, caption="Uploaded Image", use_container_width=True)

    with col2:

        if prediction > 0.5:
            st.success("Real Face")
        else:
            st.error("Fake Face")

        confidence = float(prediction)

        st.write("Confidence Score")
        st.progress(confidence)
        st.write(round(confidence*100,2), "%")
