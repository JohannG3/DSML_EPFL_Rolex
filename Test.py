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

# Gérer l'état des entrées
if 'sentence' not in st.session_state:
    st.session_state.sentence = ""
if 'improved' not in st.session_state:
    st.session_state.improved = ""

# Prédiction de la difficulté et gestion des améliorations de phrase
sentence = st.text_input("Sentence", value=st.session_state.sentence, key="sentence")

if st.button('Predict'):
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
    improved_sentence = st.text_input("Improve your sentence to increase the difficulty level:", value=st.session_state.improved, key="improved")

    if st.button('Submit the improved sentence', key="submit_improved"):
        new_prediction = st.session_state.model.predict([improved_sentence])[0]
        st.write(f"The new predicted difficulty level for your improved sentence is: {new_prediction}")
        
        if new_prediction > st.session_state.current_prediction:
            st.success("Congratulations! The difficulty level of your sentence has increased.")
            # Button to start over
            if st.button('Enter a new sentence'):
                # Clear the text inputs
                st.session_state.sentence = ""
                st.session_state.improved = ""
                st.experimental_rerun()  # Restart the application
        else:
            st.error("The difficulty level has not increased. Try again!")
