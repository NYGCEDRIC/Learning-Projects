import streamlit as st
import requests
import json
from streamlit_chat import message

# Assuming other imports and initializations are already done

# Set up ElevenLabs API credentials securely
API_KEY = st.secrets["ELEVENLABS_API_KEY"]

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

# Initialize session state variables for storing messages if they don't exist
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Your existing code to handle chat input and responses
if prompt := st.chat_input("Your question"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Assuming 'conversation' and 'response' handling here
    response = "Simulated response"  # Replace with your response logic
    st.session_state.messages.append({"role": "assistant", "content": response})

# Display chat history
for message in st.session_state.messages:
    with st.container():
        if message["role"] == "user":
            st.write("User: " + message["content"])
        else:
            st.write("Assistant: " + message["content"])
