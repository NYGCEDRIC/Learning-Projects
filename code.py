import streamlit as st
import requests

# ElevenLabs API credentials and endpoints
API_KEY = st.secrets["ELEVENLABS_API_KEY"]
TRANSLATE_URL = "https://api.elevenlabs.io/translate"
SPEECH_URL = "https://api.elevenlabs.io/speech"

def translate_text(text, target_lang):
    """Translate text to the specified language using ElevenLabs API."""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "text": text,
        "targetLanguage": target_lang
    }
    response = requests.post(TRANSLATE_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json().get('translatedText', 'Translation failed')
    else:
        st.error(f"Failed to translate text: {response.text}")
        return None

def convert_text_to_speech(text, language):
    """Convert translated text to speech using ElevenLabs API."""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "text": text,
        "model": language
    }
    response = requests.post(SPEECH_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json().get('audioUrl', 'Failed to convert text to speech')
    else:
        st.error(f"Failed to generate audio: {response.text}")
        return None


# Streamlit user interface
st.title("Translation and Text-to-Speech Chatbot")

input_text = st.text_input("Enter text to translate:")
target_language = st.selectbox("Choose the language to translate to:", ["fr", "de", "es", "it", "jp"])
output_mode = st.radio("Do you want the output as text or audio?", ["Text", "Audio"])

if st.button("Translate"):
    translated_text = translate_text(input_text, target_language)
    if output_mode == "Text":
        st.text_area("Translated Text:", value=translated_text, height=200)
    elif output_mode == "Audio":
        audio_url = convert_text_to_speech(translated_text, target_language)
        if "Failed" not in audio_url:
            st.audio(audio_url)
        else:
            st.error("Failed to generate audio. Please try again.")
