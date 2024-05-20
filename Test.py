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

def translate_text(input_text, source_lang, target_lang):
    url = "https://libretranslate.com/translate"
    payload = {
        "q": input_text,
        "source": source_lang,
        "target": target_lang,
        "format": "text"
    }
    headers = {"accept": "application/json", "Content-Type": "application/x-www-form-urlencoded"}
    try:
        response = requests.post(url, data=payload, headers=headers)
        response_data = response.json()
        if 'translatedText' in response_data:
            return response_data['translatedText']
        else:
            # Gestion si la clé 'translatedText' n'est pas présente dans la réponse
            st.error("Failed to translate. The API response was: " + str(response_data))
            return None  # Ou vous pouvez retourner une chaîne vide ou un message d'erreur spécifique
    except Exception as e:
        st.error("Error during translation: " + str(e))
        return None


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
    translated_to_english = translate_text(sentence, "fr", "en")
    st.write(f"Translated to English: {translated_to_english}")
    
    # Obtenir des synonymes en anglais
    english_words = translated_to_english.split()
    synonyms = {word: get_synonyms(word) for word in english_words}
    
    # Traduire les synonymes de retour en français
    synonyms_translated = {word: [translate_text(syn, "en", "fr") for syn in synonyms[word]] for word in synonyms}
    
    st.write("Synonyms translated back to French:")
    for word, syns in synonyms_translated.items():
        st.write(f"{word} (EN) -> {', '.join(syns)} (FR)")

    # Effectuer la prédiction de difficulté en français
    prediction = st.session_state.model.predict([sentence])[0]
    st.write(f"The predicted difficulty level for this sentence in French is: {prediction}")

