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

def translate_text(text, source_language, target_language):
    url = "https://text-translator2.p.rapidapi.com/translate"
    payload = {
        "source_language": source_language,
        "target_language": target_language,
        "text": text
    }
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "X-RapidAPI-Key": "864ad2ff57mshd1f224c4268230bp11ee28jsn58d9f3f8ad52",
        "X-RapidAPI-Host": "text-translator2.p.rapidapi.com"
    }
    response = requests.post(url, data=payload, headers=headers)
    if response.status_code == 200:
        result = response.json().get('data', {}).get('translatedText', '')
        return result
    else:
        st.error(f"Failed to translate. Status code: {response.status_code}")
        return None

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
  sentence_fr = translate_text(sentence, "fr")
  prediction = st.session_state.model.predict([sentence_fr])[0]
  st.write(f"The predicted difficulty level for this sentence in French is: {prediction}")
  """
  sentence_fr = translate_text(sentence, "en", "fr")
  st.write(f"The translated sentence in French is: {sentence_fr}")

