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

# Fonction pour traduire du français vers l'anglais
def translate_to_english(text):
    url = 'https://opentranslator.p.rapidapi.com/translate'
    headers = {
        'content-type': 'application/json',
        'X-RapidAPI-Key': '864ad2ff57mshd1f224c4268230bp11ee28jsn58d9f3f8ad52',
        'X-RapidAPI-Host': 'opentranslator.p.rapidapi.com'
    }
    data = {
        'text': text,
        'target': 'en'
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        response_data = response.json()
        # Check if response is a list and extract data accordingly
        if isinstance(response_data, list):
            # Assuming the relevant data is in the first item of the list
            return response_data[0].get('translated_text', 'No translation found')
        elif isinstance(response_data, dict):
            return response_data.get('translated_text', 'No translation found')
    return "Translation failed!"

# Fonction pour obtenir des synonymes en anglais
def get_synonyms(word):
    url = f"https://wordsapiv1.p.rapidapi.com/words/{word}/synonyms"
    headers = {'X-RapidAPI-Key': '864ad2ff57mshd1f224c4268230bp11ee28jsn58d9f3f8ad52'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        response_data = response.json()
        # Check if response is a dictionary and extract synonyms
        if 'synonyms' in response_data:
            return response_data['synonyms']
    return []

# Fonction pour traduire de l'anglais vers le français
def translate_to_french(text):
    url = 'https://opentranslator.p.rapidapi.com/translate'
    headers = {
        'content-type': 'application/json',
        'X-RapidAPI-Key': '864ad2ff57mshd1f224c4268230bp11ee28jsn58d9f3f8ad52',
        'X-RapidAPI-Host': 'opentranslator.p.rapidapi.com'
    }
    data = {
        'text': text,
        'target': 'fr'
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        response_data = response.json()
        # Check if response is a list and extract data accordingly
        if isinstance(response_data, list):
            return response_data[0].get('translated_text', 'No translation found')
        elif isinstance(response_data, dict):
            return response_data.get('translated_text', 'No translation found')
    return "Translation failed!"

# Interaction utilisateur
sentence = st.text_input("Enter a French sentence")

if st.button('Process'):
    # Traduction en anglais
    english_translation = translate_to_english(sentence)
    st.write(f"English translation: {english_translation}")
    
    # Extraction des mots et obtention des synonymes
    words = english_translation.split()
    all_synonyms = {}
    for word in words:
        synonyms = get_synonyms(word)
        all_synonyms[word] = synonyms
    
    st.write("Synonyms in English:")
    for word, synonyms in all_synonyms.items():
        st.write(f"{word}: {', '.join(synonyms)}")
    
    # Traduction des synonymes en français
    synonyms_in_french = {}
    for word, synonyms in all_synonyms.items():
        french_synonyms = []
        for synonym in synonyms:
            translated_synonym = translate_to_french(synonym)
            french_synonyms.append(translated_synonym)
        synonyms_in_french[word] = french_synonyms
    
    st.write("French translations of English synonyms:")
    for word, synonyms in synonyms_in_french.items():
        st.write(f"{word}: {', '.join(synonyms)}")
