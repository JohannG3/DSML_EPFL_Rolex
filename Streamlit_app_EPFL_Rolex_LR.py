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

# Gestion des cycles de phrases
if 'cycle_count' not in st.session_state:
    st.session_state.cycle_count = 0

def new_sentence_cycle():
    st.session_state.cycle_count += 1

sentence = st.text_input("Sentence", key=f"sentence_{st.session_state.cycle_count}")

if st.button('Predict', key=f"predict_{st.session_state.cycle_count}"):
    prediction = st.session_state.model.predict([sentence])[0]
    st.write(f"The predicted difficulty level for this sentence is: {prediction}")
    
    words = sentence.split()
    for word in words:
        synonyms = get_synonyms(word)
        if synonyms:
            st.write(f"Synonyms for '{word}': {', '.join(synonyms)}")

    # Sauvegarder la prédiction initiale pour comparaison ultérieure
    st.session_state.current_prediction = prediction

# Interaction pour améliorer la phrase
if 'current_prediction' in st.session_state:
    improved_sentence = st.text_input("Improve your sentence to increase the difficulty level:", key=f"improved_{st.session_state.cycle_count}")

    if st.button('Submit the improved sentence', key=f"submit_improved_{st.session_state.cycle_count}"):
        new_prediction = st.session_state.model.predict([improved_sentence])[0]
        st.write(f"The new predicted difficulty level for your improved sentence is: {new_prediction}")
        
        if new_prediction > st.session_state.current_prediction:
            st.success("Congratulations! The difficulty level of your sentence has increased.")
            st.session_state.current_prediction = new_prediction  # Mise à jour de la prédiction actuelle
            if st.button('Enter a new sentence', key=f"new_sentence_{st.session_state.cycle_count}"):
                new_sentence_cycle()
        else:
            st.error("The difficulty level has not increased. Try again!")
