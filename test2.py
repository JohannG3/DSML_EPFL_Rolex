import streamlit as st
import requests
from dotenv import load_dotenv
import os

# Charger les variables d'environnement
load_dotenv()

# Récupérer la clé API depuis les variables d'environnement
API_KEY = os.getenv('RAPIDAPI_KEY')

headers = {
    'content-type': 'application/json',
    'X-RapidAPI-Key': "864ad2ff57mshd1f224c4268230bp11ee28jsn58d9f3f8ad52",
    'X-RapidAPI-Host': 'opentranslator.p.rapidapi.com'
}

url = 'https://opentranslator.p.rapidapi.com/translate'

def translate_text(text, target_language):
    payload = {
        "text": text,
        "target": target_language
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()['translatedText']
    else:
        return "Erreur lors de la traduction"

# Interface Streamlit
st.title('Traducteur Français-Anglais')

# Entrée de l'utilisateur
user_input = st.text_area("Entrez une phrase en français:")

# Bouton pour traduire
if st.button('Traduire'):
    translation = translate_text(user_input, 'en')
    st.write('Traduction en anglais :', translation)

