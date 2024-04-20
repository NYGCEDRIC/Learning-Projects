import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory

# Initialize session state variables
if 'buffer_memory' not in st.session_state:
    st.session_state.buffer_memory = ConversationBufferWindowMemory(k=3, return_messages=True)

if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role": "assistant", "content": "How can I help you today?"}
    ]

# Assuming the API key is securely loaded from environment or Streamlit secrets
# Load your Chat Model (Change this to any model you prefer, ensure it supports translation)
llm = ChatOpenAI(model="gpt-4", api_key=st.secrets["OPENAI_API_KEY"])  # Update model to GPT-4 for translation capability

conversation = ConversationChain(memory=st.session_state.buffer_memory, llm=llm)

# User interface for the chatbot
st.title("🗣️ Language Translation Chatbot")
st.subheader("㈻ Seamlessly communicate across language barriers")

# Language selection
target_language = st.selectbox("Select the target language:", ["French", "Spanish", "German", "Chinese", "Japanese", "English"])

if prompt := st.chat_input("Your question"):
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages:
    with st.container():  # Updated to use `container` for better compatibility
        st.write(f"{message['role'].capitalize()}: {message['content']}")

# Generate a response and translate if needed
if st.session_state.messages[-1]["role"] != "assistant":
    with st.container():  # Using container for assistant's message
        with st.spinner("Translating and responding..."):
            # Translating the user's input before generating a response
            translation_prompt = f"Translate this to {target_language}: {prompt}"
            translated_input = llm.generate(translation_prompt)
            response = conversation.predict(input=translated_input)
            st.write(f"Assistant (in {target_language}): {response}")
            st.session_state.messages.append({"role": "assistant", "content": response})
