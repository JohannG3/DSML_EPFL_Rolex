import streamlit as st
import requests
from joblib import load
from io import BytesIO

# Titre de l'application
st.title('Predicting sentence difficulty in French')

# Description
st.write("Enter a sentence in French to predict its difficulty level and get synonyms to enrich your vocabulary.")

# Chargement du modèle si pas déjà chargé
if 'model' not in st.session_state:
    url = 'https://github.com/JohannG3/DSML_EPFL_Rolex/blob/main/french_difficulty_predictor_model.joblib?raw=true'
    response = requests.get(url)
    st.session_state.model = load(BytesIO(response.content))

# Fonction pour obtenir des synonymes
def get_synonyms(word):
  synonyms = {
    "manger": ["consommer", "dévorer", "ingérer"],
    "pomme": ["fruit"],
    "perdu": ["égaré", "disparu", "paumé"]
  }
  return synonyms.get(word, [])

def handle_new_cycle():
  st.session_state['cycle'] = st.session_state.get('cycle', 0) + 1

if 'cycle' not in st.session_state:
  handle_new_cycle()

cycle_key = f"cycle_{st.session_state['cycle']}"

# Entrée de la phrase
sentence = st.text_input("Sentence", key=f"sentence_{cycle_key}")

if st.button('Predict', key=f"predict_{cycle_key}"):
  prediction = st.session_state.model.predict([sentence])[0]
  st.write(f"The predicted difficulty level for this sentence is: {prediction}")
   
  words = sentence.split()
  for word in words:
    synonyms = get_synonyms(word)
    if synonyms:
      st.write(f"Synonyms for '{word}': {', '.join(synonyms)}")

  st.session_state[f"current_prediction_{cycle_key}"] = prediction

# Interaction pour améliorer la phrase
if f"current_prediction_{cycle_key}" in st.session_state:
  improved_sentence = st.text_input("Improve your sentence to increase the difficulty level:", key=f"improved_{cycle_key}")

  if st.button('Submit the improved sentence', key=f"submit_improved_{cycle_key}"):
    new_prediction = st.session_state.model.predict([improved_sentence])[0]
    st.write(f"The new predicted difficulty level for your improved sentence is: {new_prediction}")
     
    if new_prediction > st.session_state[f"current_prediction_{cycle_key}"]:
      st.success("Congratulations! The difficulty level of your sentence has increased.")
      st.session_state[f"current_prediction_{cycle_key}"] = new_prediction # Update current prediction
      if st.button('Enter a new sentence', key=f"new_sentence_{cycle_key}"):
        # Reset session state and clear UI elements
        st.session_state['cycle'] = 0
        del st.session_state[f"current_prediction_{cycle_key}"]
        st.session_state[f"sentence_{cycle_key}"] = ""  # Clear sentence input
        handle_new_cycle()
    else:
      st.error("The difficulty level has not increased. Try again!")
