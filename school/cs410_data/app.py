import pandas as pd
import numpy as np
import streamlit as st
import joblib

# Define file name
file = 'penguin_model.joblib'

@st.cache_resource
def load_model(file):
    model = joblib.load(file)
    return model

try:
    model = load_model(file)
    
except FileNotFoundError:
    st.error("Error: Model File Not Found")
    st.stop()

with st.sidebar:
    st.title("Penguin classifier")
    st.write("Classify your penguin using Machine Learning!")

    island = st.selectbox("Island",
                       ["Biscoe",
                       "Dream Island",
                       "Torgersen"])
    bill_length = st.slider("Bill Lenght (mm)",
                               min_value=32.1,
                               max_value=59.6)
    bill_depth = st.slider("Bill Depth (mm)",
                               min_value=13.1,
                               max_value=21.5)
    flipper_length = st.slider("Flipper Length (mm)",
                               min_value=172,
                               max_value=231)
    body_mass = st.slider("Body mass (mm)",
                               min_value=2700,
                               max_value=6300)
    sex = st.selectbox("Sex", ["Male", "Female"])

    predict_button = st.button("Predict")

    
# Main app
st.header("Palmer Penguins Predictor")

if predict_button:
    
    features = np.array([[island,
                          bill_length,
                          bill_depth,
                          flipper_length,
                          body_mass,
                          sex]])
    feature_names = ["island_cat",
                     "bill_length_mm",
                     "bill_depth_mm",
                     "flipper_length_mm",
                     "body_mass_g",
                     "sex_cat"]
    feature_df = pd.DataFrame(features, columns=feature_names)

    prediction = model.predict(feature_df)[0]

    st.divider()
    
    st.success(f"Predicted class: {prediction}")
    st.balloons()