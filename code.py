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

# Function to translate text using ChatGPT
def translate_text(input_text, target_language):
    prompt = f"Translate this text to {target_language}: {input_text}"
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=500
    )
    return response.choices[0].text.strip()

# Streamlit interface
st.title("Real-time Language Translation Chatbot")
input_text = st.text_area("Enter text to translate:")
languages = {"French": "fr", "Spanish": "es", "German": "de", "Chinese": "zh", "Japanese": "ja"}
target_language = st.selectbox("Select the target language:", list(languages.keys()))
output_mode = st.radio("Output mode:", ["Text", "Audio"])

if st.button("Translate"):
    if input_text:
        translated_text = translate_text(input_text, target_language)
        if output_mode == "Text":
            st.text_area("Translated Text", value=translated_text, height=250, max_chars=None)
        elif output_mode == "Audio":
            language_code = f"{languages[target_language]}-US"  # Simplified mapping, adjust as needed
            audio_content = text_to_speech(translated_text, language_code)
            st.audio(audio_content, format='audio/mp3')
    else:
        st.error("Please enter some text to translate.")

