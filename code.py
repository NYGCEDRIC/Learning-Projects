import streamlit as st
import openai

# Load your OpenAI API key securely
openai.api_key = st.secrets["OPENAI_API_KEY"]

def translate_text(text, source_lang, target_lang):
    """ Translate text from source_lang to target_lang using OpenAI's GPT-4. """
    prompt = f"Translate the following text from {source_lang} to {target_lang}: {text}"
    response = openai.Completion.create(
        model="text-davinci-003",  # Replace with "gpt-4" once available in your account
        prompt=prompt,
        max_tokens=512,
        temperature=0.5,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    return response.choices[0].text.strip()

st.title('Real-time Language Translation Chatbot')
st.write('This chatbot translates your input text to a selected language using OpenAI GPT-4.')

# Select source and target languages
source_lang = st.selectbox('Select source language:', ['English', 'Spanish', 'French', 'German', 'Chinese'])
target_lang = st.selectbox('Select target language:', ['Spanish', 'English', 'French', 'German', 'Chinese'])

# User input for translation
user_input = st.text_area("Enter the text you want to translate:", height=200)
if st.button('Translate'):
    if user_input:
        translated_text = translate_text(user_input, source_lang, target_lang)
        st.text_area("Translated Text:", translated_text, height=200)
    else:
        st.error("Please enter some text to translate.")

