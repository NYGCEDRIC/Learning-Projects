import streamlit as st
from transformers import pipeline

# Load the translation model pipeline
translator = pipeline("translation", model="facebook/nllb-200-distilled-600M")

# Streamlit interface
st.title("Multilingual Translation App")
input_text = st.text_area("Enter the text you want to translate:", height=150)
source_language = st.text_input("Enter the source language code (e.g., 'en'):")
target_language = st.text_input("Enter the target language code (e.g., 'fr'):")

if st.button("Translate"):
    if input_text and source_language and target_language:
        # Performing translation
        try:
            translation = translator(input_text, forced_bos_token_id=translator.tokenizer.get_lang_id(lang=target_language))
            translated_text = translation[0]['translation_text']
            st.write("Translated Text:", translated_text)
        except Exception as e:
            st.error(f"An error occurred during translation: {str(e)}")
    else:
        st.warning("Please fill in all the fields.")
