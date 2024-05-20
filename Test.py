"""
import streamlit as st
import requests
from joblib import load
from io import BytesIO

# Titre de l'application
st.title('Predicting sentence difficulty in French with Synonym Enhancement')

# Description
st.write("Enter a sentence in French to predict its difficulty level, translate to English, get synonyms in English, and translate them back to French.")

# Chargement du modèle si pas déjà chargé
if 'model' not in st.session_state:
    url = 'https://github.com/JohannG3/DSML_EPFL_Rolex/blob/main/french_difficulty_predictor_model.joblib?raw=true'
    response = requests.get(url)
    st.session_state.model = load(BytesIO(response.content))



# Fonction pour obtenir des synonymes avec WordsAPI
def get_synonyms(word):
    url = f"https://wordsapiv1.p.rapidapi.com/words/{word}/synonyms"
    headers = {
        'x-rapidapi-host': "wordsapiv1.p.rapidapi.com",
        'x-rapidapi-key': "864ad2ff57mshd1f224c4268230bp11ee28jsn58d9f3f8ad52"  # Replace YOUR_RAPIDAPI_KEY with your actual key from RapidAPI
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data['synonyms'] if 'synonyms' in data else []
    return []

# Prédiction de la difficulté et gestion des traductions et synonymes
sentence = st.text_input("Sentence in French", "")

if st.button('Predict and Enhance'):
    # Traduire de français à anglais
    
    
    # Obtenir des synonymes en anglais
    english_words = sentence.split()
    synonyms = {word: get_synonyms(word) for word in english_words}
    

    
    st.write("Synonyms translated back to French:")
    for word, syns in synonyms.items():
        st.write(f"{word} (EN) -> {', '.join(syns)} (FR)")

    # Effectuer la prédiction de difficulté en français
    prediction = st.session_state.model.predict([sentence])[0]
    st.write(f"The predicted difficulty level for this sentence in French is: {prediction}")
    """

import streamlit as st
import requests
from joblib import load
from io import BytesIO

# Titre de l'application
st.title('Predicting sentence difficulty in French with Synonym Enhancement')

# Description
st.write("Enter a sentence in French to predict its difficulty level, translate to English, get synonyms in English, and translate them back to French.")

# Chargement du modèle si pas déjà chargé
if 'model' not in st.session_state:
    url = 'https://github.com/JohannG3/DSML_EPFL_Rolex/blob/main/french_difficulty_predictor_model.joblib?raw=true'
    response = requests.get(url)
    st.session_state.model = load(BytesIO(response.content))

def translate_text(text, target_language="fr"):
    url = "https://opentranslator.p.rapidapi.com/translate"
    payload = {
        "text": text,
        "target": target_language
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "864ad2ff57mshd1f224c4268230bp11ee28jsn58d9f3f8ad52",
        "X-RapidAPI-Host": "opentranslator.p.rapidapi.com"
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        response_data = response.json()
        # Check deeply nested structure with safe guards
        if (response_data and isinstance(response_data, list) and
            response_data[0].get('status') == 'SUCCESS' and
            response_data[0].get('result') and
            isinstance(response_data[0]['result'], list) and
            len(response_data[0]['result']) > 0 and
            isinstance(response_data[0]['result'][0], list) and
            len(response_data[0]['result'][0]) > 0):
            # Correctly access the 'text' field inside the nested list
            translated_text = response_data[0]['result'][0][0]
            return translated_text
        else:
            st.error("Failed to get a valid translation. Check API response structure: " + str(response_data))
            return "Translation error"
    else:
        st.error("HTTP error occurred with status code: " + str(response.status_code))
        return "Translation error"

# Fonction pour obtenir des synonymes avec WordsAPI
def get_synonyms(word):
    url = f"https://wordsapiv1.p.rapidapi.com/words/{word}/synonyms"
    headers = {
        'x-rapidapi-host': "wordsapiv1.p.rapidapi.com",
        'x-rapidapi-key': "864ad2ff57mshd1f224c4268230bp11ee28jsn58d9f3f8ad52"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data['synonyms'] if 'synonyms' in data else []
    return []

# Prédiction de la difficulté et gestion des traductions et synonymes
sentence = st.text_input("Sentence in French", "")

if st.button('Predict and Enhance'):    
    """
    # Obtenir des synonymes en anglais
    english_words = sentence.split()
    synonyms = {word: get_synonyms(word) for word in english_words}
    
    # Traduire les synonymes en français
    synonyms_in_french = {}
    for word, syn_list in synonyms.items():
        french_synonyms = [translate_text(syn, "fr") for syn in syn_list]
        synonyms_in_french[word] = french_synonyms

    st.write("English synonyms and their French translations:")
    for word, syns in synonyms_in_french.items():
        st.write(f"{word} (EN) -> {', '.join(syns)} (FR)")

    # Effectuer la prédiction de difficulté en français
    prediction = st.session_state.model.predict([sentence])[0]
    st.write(f"The predicted difficulty level for this sentence in French is: {prediction}")
    """
    sentence_fr = translate_text(sentence, "fr")
    st.write(f"The translated sentence in French is: {sentence_fr}")
