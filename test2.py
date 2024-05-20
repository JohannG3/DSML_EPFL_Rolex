import streamlit as st
import requests
from joblib import load
from io import BytesIO
import nltk
from nltk.corpus import stopwords

# Téléchargez les stop words la première fois
nltk.download('stopwords')

# Chargement des stop words pour le français
french_stopwords = set(stopwords.words('french'))

st.title('Amélioration de la difficulté d\'une phrase en français')

# Chargement du modèle prédictif
if 'model' not in st.session_state:
    model_url = 'https://github.com/JohannG3/DSML_EPFL_Rolex/blob/main/french_difficulty_predictor_model.joblib?raw=true'
    response = requests.get(model_url)
    st.session_state.model = load(BytesIO(response.content))

# Fonctions auxiliaires pour la traduction et la récupération des synonymes
def translate_text(text, source_lang, target_lang):
    translate_url = "https://text-translator2.p.rapidapi.com/translate"
    payload = f"source_language={source_lang}&target_language={target_lang}&text={text}"
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "X-RapidAPI-Key": "864ad2ff57mshd1f224c4268230bp11ee28jsn58d9f3f8ad52",
        "X-RapidAPI-Host": "text-translator2.p.rapidapi.com"
    }
    response = requests.post(translate_url, data=payload, headers=headers)
    if response.status_code == 200 and 'data' in response.json():
        return response.json()['data']['translatedText']
    return "Translation error"

def get_synonyms(word):
    # Vérifiez si le mot est un stop word
    if word.lower() in french_stopwords:
        return []  # Retourne une liste vide si c'est un stop word
    synonyms_url = f"https://wordsapiv1.p.rapidapi.com/words/{word}/synonyms"
    headers = {
        'x-rapidapi-host': "wordsapiv1.p.rapidapi.com",
        'x-rapidapi-key': "864ad2ff57mshd1f224c4268230bp11ee28jsn58d9f3f8ad52"
    }
    response = requests.get(synonyms_url, headers=headers)
    if response.status_code == 200 and 'synonyms' in response.json():
        return response.json()['synonyms']
    return []

# Interface utilisateur
sentence = st.text_input("Entrez une phrase en français")

if st.button('Analyser la phrase'):
    # Prédiction de la difficulté
    difficulty = st.session_state.model.predict([sentence])[0]
    st.write(f"Niveau de difficulté prédit pour cette phrase en français : {difficulty}")
    
    # Traduction de la phrase en anglais
    english_translation = translate_text(sentence, 'fr', 'en')
    st.write(f"Traduction en anglais : {english_translation}")
    
    # Obtention et traduction des synonymes
    words = english_translation.split()
    synonyms_list = {word: get_synonyms(word) for word in words}
    synonyms_translated = {word: [translate_text(syn, 'en', 'fr') for syn in synonyms_list[word]] for word in synonyms_list}
    
    # Affichage des synonymes
    for word, syns in synonyms_translated.items():
        st.write(f"Synonymes de {word} : {', '.join(syns)}")
    
    # Demande de nouvelle phrase
    new_sentence = st.text_input("Entrez une nouvelle phrase pour essayer d'améliorer le niveau de difficulté")
    if new_sentence:
        new_difficulty = st.session_state.model.predict([new_sentence])[0]
        if new_difficulty > difficulty:
            st.success("Félicitations ! Le niveau de difficulté de votre phrase a augmenté.")
        else:
            st.error("Le niveau de difficulté n'a pas augmenté. Essayez encore !")
