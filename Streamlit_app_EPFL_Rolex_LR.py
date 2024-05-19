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

# Nouvelle session de prédiction
def new_prediction_session():
    with st.container():
        sentence = st.text_input("Sentence", key=f'sentence_{st.session_state.session_count}')
        if st.button('Predict', key=f'predict_{st.session_state.session_count}'):
            if sentence:
                prediction = st.session_state.model.predict([sentence])[0]
                st.write(f"The predicted difficulty level for this sentence is: {prediction}")
                
                words = sentence.split()
                for word in words:
                    synonyms = get_synonyms(word)
                    if synonyms:
                        st.write(f"Synonyms for '{word}': {', '.join(synonyms)}")
                
                st.session_state['current_prediction'] = prediction

        # Interaction pour améliorer la phrase
        if 'current_prediction' in st.session_state:
            improved_sentence = st.text_input("Improve your sentence to increase the difficulty level:", key=f'improved_{st.session_state.session_count}')
            if st.button('Submit the improved sentence', key=f"submit_improved_{st.session_state.session_count}"):
                new_prediction = st.session_state.model.predict([improved_sentence])[0]
                st.write(f"The new predicted difficulty level for your improved sentence is: {new_prediction}")
                
                if new_prediction > st.session_state['current_prediction']:
                    st.success("Congratulations! The difficulty level of your sentence has increased.")
                else:
                    st.error("The difficulty level has not increased. Try again!")

# Initialisation du compteur de sessions s'il n'existe pas
if 'session_count' not in st.session_state:
    st.session_state.session_count = 0

# Bouton pour démarrer une nouvelle session de prédiction
if st.button("Enter a new sentence"):
    st.session_state.session_count += 1
    new_prediction_session()
else:
    new_prediction_session()
