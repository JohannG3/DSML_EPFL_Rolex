import streamlit as st
import requests

def translate_text(text, target_language="en"):
    url = "https://opentranslator.p.rapidapi.com/translate"
    payload = {
        "text": text,
        "target": target_language
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "YOUR_RAPIDAPI_KEY",
        "X-RapidAPI-Host": "opentranslator.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()['translatedText']
    else:
        return "Erreur de traduction"

def main():
    st.title('Traducteur de Français vers Anglais')
    user_input = st.text_area("Entrez une phrase en français que vous voulez traduire en anglais:")

    if st.button("Traduire"):
        translation = translate_text(user_input)
        st.text_area("Traduction en anglais:", translation, height=150)

if __name__ == "__main__":
    main()
