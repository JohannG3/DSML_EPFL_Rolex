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
import json

# Titre de l'application
st.title('Advanced Word Translator and Synonym Finder')

# Description
st.write("Enter a French word to get its English synonyms translated back into French.")

# API Keys (Placeholders ici, remplacez avec vos propres clés)
MYMEMORY_API_KEY = 'YOUR_MYMEMORY_API_KEY'
WORDS_API_KEY = 'YOUR_WORDS_API_KEY'
LIBRE_TRANSLATE_URL = 'https://libretranslate.com/translate'

# Fonction pour traduire un mot du français vers l'anglais
def translate_to_english(word):
    params = {
        "q": word,
        "langpair": "fr|en",
        "de": "jomboso3@gmail.com"  # Changez à votre email utilisé pour l'API
    }
    headers = {
        "X-RapidAPI-Key": "864ad2ff57mshd1f224c4268230bp11ee28jsn58d9f3f8ad52",
        "X-RapidAPI-Host": "translated-mymemory---translation-memory.p.rapidapi.com"
    }
    response = requests.get("https://translated-mymemory---translation-memory.p.rapidapi.com/get", params=params, headers=headers)
    return response.json()['responseData']['translatedText']

# Fonction pour obtenir des synonymes en anglais
def get_synonyms(word):
    url = f"https://wordsapiv1.p.rapidapi.com/words/{word}/synonyms"
    headers = {
        "X-RapidAPI-Key": "864ad2ff57mshd1f224c4268230bp11ee28jsn58d9f3f8ad52",
        "X-RapidAPI-Host": "wordsapiv1.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    return data['synonyms'] if 'synonyms' in data else []

# Fonction pour traduire des mots de l'anglais vers le français
def translate_to_french(words):
    data = {
        "q": ", ".join(words),
        "source": "en",
        "target": "fr",
        "format": "text"
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(LIBRE_TRANSLATE_URL, data=json.dumps(data), headers=headers)
    return response.json()['translatedText']

# Interaction avec l'utilisateur
french_word = st.text_input("French Word", "")

if st.button('Translate and Find Synonyms'):
    if french_word:
        # Traduction du français vers l'anglais
        english_word = translate_to_english(french_word)
        st.write(f"English translation: {english_word}")
        
        # Obtention des synonymes en anglais
        synonyms = get_synonyms(english_word)
        st.write(f"English synonyms: {', '.join(synonyms)}")
        
        # Traduction des synonymes vers le français
        if synonyms:
            french_synonyms = translate_to_french(synonyms)
            st.write(f"French translations of synonyms: {french_synonyms}")
        else:
            st.write("No synonyms found.")


