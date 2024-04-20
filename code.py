import streamlit as st
import openai

# Assuming the API key is stored in Streamlit's secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

def translate_text(text, source_lang, target_lang):
    """Translate text from source_lang to target_lang using OpenAI's latest API."""
    prompt = f"Translate the following text from {source_lang} to {target_lang}: {text}"
    try:
        response = openai.Completion.create(
            model="gpt-3.5-turbo",  # Change this to "gpt-4" if available and appropriate
            prompt=prompt,
            max_tokens=512,
            temperature=0.5,
            top_p=1.0,
            n=1
        )
        return response['choices'][0]['text'].strip()
    except Exception as e:
        st.error(f"Failed to translate: {str(e)}")
        return ""

# Streamlit application setup
st.title('Real-time Language Translation Chatbot')
st.write('This chatbot translates your input text to a selected language using OpenAI.')

source_lang = st.selectbox('Source language:', ['English', 'Spanish', 'French', 'German', 'Chinese'])
target_lang = st.selectbox('Target language:', ['Spanish', 'English', 'French', 'German', 'Chinese'])

user_input = st.text_area("Enter text to translate:")
if st.button('Translate'):
    if user_input:
        translated_text = translate_text(user_input, source_lang, target_lang)
        st.text_area("Translated Text:", translated_text)
    else:
        st.error("Please enter text to translate.")
