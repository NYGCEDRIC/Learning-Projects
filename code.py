import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory

# Initialize session state variables for message history and memory buffer
if 'buffer_memory' not in st.session_state:
    st.session_state.buffer_memory = ConversationBufferWindowMemory(k=3, return_messages=True)

if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role": "assistant", "content": "Welcome! How can I help you today?"}
    ]

# Initialize the language model (assuming API key is securely loaded from Streamlit secrets)
llm = ChatOpenAI(model="gpt-4", api_key=st.secrets["OPENAI_API_KEY"])  # Specify the model to use
conversation = ConversationChain(memory=st.session_state.buffer_memory, llm=llm)

# User interface setup
st.title("🗣️ Multilingual Translation Chatbot")
st.subheader("Communicate seamlessly across diverse languages")

# Language selection for translation
languages = {
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Chinese": "zh",
    "Japanese": "ja",
    "English": "en",
    "Kinyarwanda": "rw",
    "Swahili": "sw",
    "Hindi": "hi"
}
target_language = st.selectbox("Select the target language:", list(languages.keys()))

# Input from the user
if prompt := st.text_input("Enter your message:"):
    st.session_state.messages.append({"role": "user", "content": prompt})

# Display the conversation history
for message in st.session_state.messages:
    with st.container():
        st.write(f"{message['role'].capitalize()}: {message['content']}")

# Translate and generate responses
if st.session_state.messages[-1]["role"] != "assistant":
    with st.container():
        with st.spinner("Translating and responding..."):
            # Create a refined prompt for translation
            refined_prompt = f"Translate the following English text to {target_language}: '{prompt}'"
            translated_prompt = llm.generate(refined_prompt)
            response = conversation.predict(input=translated_prompt)
            st.write(f"Assistant (in {target_language}): {response}")
            st.session_state.messages.append({"role": "assistant", "content": response})
