import streamlit as st
import openai
from google.cloud import texttospeech

# Initialize Google Text-to-Speech client
client_tts = texttospeech.TextToSpeechClient()

def translate_text(text, target_lang):
    """Use OpenAI to translate text."""
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Translate the following text to {target_lang}: {text}",
            max_tokens=60
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Failed to translate: {str(e)}"

def text_to_speech(text, language_code):
    """Convert text to speech using Google Text-to-Speech."""
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(language_code=language_code, ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    response = client_tts.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
    return response.audio_content

# Streamlit UI
st.title("Real-time Language Translation Chatbot")
input_text = st.text_input("Enter text to translate:")
target_language = st.selectbox("Select target language:", ["Spanish", "French", "German", "Chinese", "Japanese"])
output_mode = st.radio("Select output mode:", ["Text", "Audio"])

if st.button("Translate"):
    translated_text = translate_text(input_text, target_language)
    if output_mode == "Text":
        st.text_area("Translated Text", value=translated_text, height=250)
    elif output_mode == "Audio":
        audio_content = text_to_speech(translated_text, "en-US")  # Adjust language code as needed
        st.audio(audio_content, format='audio/mp3')
