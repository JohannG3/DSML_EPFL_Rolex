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

# Fonction pour obtenir des synonymes à partir de Free Dictionary API
def get_synonyms(word):
    try:
        api_url = f"https://api.dictionaryapi.dev/api/v2/entries/fr/{word}"
        response = requests.get(api_url)
        word_data = response.json()
        synonyms_list = []
        if 'title' in word_data:
            # Gère le cas où aucun synonyme n'est trouvé
            return "No synonyms found"
        else:
            # Parcourt les différentes significations pour extraire les synonymes
            for meaning in word_data[0]['meanings']:
                for definition in meaning['definitions']:
                    if 'synonyms' in definition:
                        synonyms_list.extend(definition['synonyms'])
            return ', '.join(set(synonyms_list)) if synonyms_list else "No synonyms found"
    except Exception as e:
        return "No synonyms found"

# Prédiction de la difficulté et gestion des améliorations de phrase
sentence = st.text_input("Sentence", "")

if st.button('Predict'):
    prediction = st.session_state.model.predict([sentence])[0]
    st.write(f"The predicted difficulty level for this sentence is: {prediction}")
    
    words = sentence.split()
    for word in words:
        synonyms = get_synonyms(word)
        if synonyms and synonyms != "No synonyms found":
            st.write(f"Synonyms for '{word}': {synonyms}")
        else:
            st.write(f"No synonyms found for '{word}'.")

    # Sauvegarder la prédiction initiale pour comparaison ultérieure
    st.session_state.current_prediction = prediction

# Interaction pour améliorer la phrase
if 'current_prediction' in st.session_state:
    improved_sentence = st.text_input("Improve your sentence to increase the difficulty level:", key="improved")

    if st.button('Submit the improved sentence', key="submit_improved"):
        new_prediction = st.session_state.model.predict([improved_sentence])[0]
        st.write(f"The new predicted difficulty level for your improved sentence is: {new_prediction}")
        
        if new_prediction > st.session_state.current_prediction:
            st.success("Congratulations! The difficulty level of your sentence has increased.")
            if st.button('Enter a new sentence'):
                st.session_state.clear()
                st.experimental_rerun()
        else:
            st.error("The difficulty level has not increased. Try again!")
