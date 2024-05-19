import streamlit as st
import requests
from joblib import load
from io import BytesIO

# Title of the app
st.title('Predicting sentence difficulty in French')

# Description
st.write("Enter a sentence in French to predict its difficulty level.")

url = 'https://github.com/JohannG3/DSML_EPFL_Rolex/blob/main/french_difficulty_predictor_model.joblib?raw=true'

# Load the model
response = requests.get(url)
model = load(BytesIO(response.content))

# Input from user
sentence = st.text_input("Sentence", "")

if st.button('Predict'):
    prediction = model.predict([sentence])[0]
    st.write(f"The predicted difficulty level for this sentence is: {prediction}")
