import openai
import streamlit as st

# Ensure your OpenAI API key is loaded from a secure place
openai.api_key = st.secrets["OPENAI_API_KEY"]

def translate_text(input_text, target_language):
    try:
        response = openai.Completion.create(
            model="gpt-4",
            prompt=f"Translate this text to {target_language}: {input_text}",
            max_tokens=100,
            temperature=0.5,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        # Assuming the response format requires accessing 'choices'
        return response.choices[0].text.strip()
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return "Translation failed."

# Streamlit user interface setup
st.title("Real-time Language Translation with GPT-4")
input_text = st.text_area("Enter text to translate:")
languages = ["French", "Spanish", "German", "Chinese", "Japanese"]
target_language = st.selectbox("Select the target language:", languages)

if st.button("Translate"):
    if input_text:
        translated_text = translate_text(input_text, target_language)
        st.text_area("Translated Text", value=translated_text, height=250)
    else:
        st.warning("Please enter some text to translate.")
