import streamlit as st
import openai
from google.cloud import texttospeech

# Set up the Google Text-to-Speech client
client_tts = texttospeech.TextToSpeechClient()

# Function to convert text to speech
def text_to_speech(text, language_code):
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    response = client_tts.synthesize_speech(
        input=synthesis_input, 
        voice=voice, 
        audio_config=audio_config
    )
    return response.audio_content

# OpenAI API key setup
openai.api_key = st.secrets["OPENAI_API_KEY"]

def translate_text(input_text, target_language):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Specify GPT-4.0 model
            messages=[
                {"role": "system", "content": "You are a multilingual assistant."},
                {"role": "user", "content": f"Translate this to {target_language}: {input_text}"}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return "Failed to translate"

# Streamlit UI
st.title("Real-time Language Translation with GPT-4")
input_text = st.text_area("Enter text to translate:")
languages = ["French", "Spanish", "German", "Chinese", "Japanese"]
target_language = st.selectbox("Select the target language:", languages)

if st.button("Translate"):
    if input_text:
        translated_text = translate_text(input_text, target_language)
        st.text_area("Translated Text", value=translated_text, height=250, max_chars=None)
    else:
        st.warning("Please enter some text to translate.")
