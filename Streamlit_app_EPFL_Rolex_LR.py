import streamlit as st
import requests
from joblib import load
from io import BytesIO

# Titre de l'application
st.title('Predicting sentence difficulty in French')

# Description
st.write("Enter a sentence in French to predict its difficulty level and get synonyms to enrich your vocabulary.")

# URL de votre modèle stocké sur GitHub
url = 'https://github.com/JohannG3/DSML_EPFL_Rolex/blob/main/french_difficulty_predictor_model.joblib?raw=true'

# Téléchargement et chargement du modèle
response = requests.get(url)
model = load(BytesIO(response.content))

# Entrée de l'utilisateur
sentence = st.text_input("Sentence", "")

"""
# Clé API pour Dicolink
api_key = 'YOUR_DICOLINK_API_KEY'

def get_synonyms(word):
    # Fonction pour obtenir les synonymes d'un mot en français
    api_url = f"https://api.dicolink.com/v1/mot/{word}/synonymes?limite=5&api_key={api_key}"
    response = requests.get(api_url)
    data = response.json()
    synonyms = [item['mot'] for item in data] if isinstance(data, list) else "Aucun synonyme trouvé"
    return ", ".join(synonyms)
"""

def get_synonyms(word):
    # Simuler une fonction de récupération de synonymes
    synonyms = {"manger": ["consommer", "dévorer", "ingérer"], "pomme": ["fruit"]}
    return synonyms.get(word, [])

if st.button('Predict'):
    prediction = model.predict([sentence])[0]
    st.write(f"The predicted difficulty level for this sentence is: {prediction}")
    
    # Afficher les synonymes pour chaque mot
    words = sentence.split()
    for word in words:
        synonyms = get_synonyms(word)
        st.write(f"Synonymes pour '{word}' : {synonyms}")
    
    # Demander à l'utilisateur d'améliorer sa phrase
    improved_sentence = st.text_input("Improve your sentence to increase the difficulty level:", "")
    if st.button('Submit the improved sentence'):
        new_prediction = model.predict([improved_sentence])[0]
        if new_prediction > prediction:
            st.success("Congratulations ! The difficulty level of your sentence has increased.")
        else:
            st.error("The difficulty level has not increased. Try again !")
