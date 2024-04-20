import streamlit as st
import requests
import json
from streamlit_chat import message

# Assuming other imports and initializations are already done

# Set up ElevenLabs API credentials securely
API_KEY = st.secrets["e014db3674e9b676cf019f33a018ff57"]

def convert_text_to_speech(text, voice="en-US-Wavenet-A"):
    """Convert text to speech using ElevenLabs API."""
    url = "https://api.elevenlabs.io/speech"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "text": text,
        "model": voice
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['audioUrl']
    else:
        return "Error in text-to-speech conversion"

# Modify your chat handling to include a text-to-speech option
if prompt := st.chat_input("Your question"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Handle translation or normal conversation here
    response = conversation.predict(input=prompt)
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)

    # Option to convert response to speech
    if st.button("Hear it"):
        audio_url = convert_text_to_speech(response)
        if "Error" not in audio_url:
            st.audio(audio_url)
        else:
            st.error("Failed to convert text to speech.")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
