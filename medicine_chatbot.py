import streamlit as st
import json
from gtts import gTTS
from io import BytesIO
import base64
from googletrans import Translator

# Load data
with open("symptom_medicine_mapping_dict.json", "r") as f:
    medicine_data = json.load(f)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar for chat history
st.sidebar.title("💬 Chat History")
for i, msg in enumerate(st.session_state.messages):
    st.sidebar.write(f"{i+1}. {msg['role'].capitalize()}: {msg['content']}")

st.title("🧑‍⚕️ Medicine Chatbot")
translator = Translator()

# Chat input
if prompt := st.chat_input("Enter your symptom..."):
    # Store user input
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Find related medicine
    response = "Sorry, I couldn't find any medicine for that symptom."
    for med, info in medicine_data.items():
        if prompt.lower() in info["cause"].lower():
            response = f"Symptom: {prompt}\nCause: {info['cause']}\nSuggested medicine: {med}\nConditions: {info['medicine']}"
            break

    # Translate response (example: Hindi)
    target_lang = "hi"  # change this dynamically as per user selection
    translated = translator.translate(response, dest=target_lang).text

    # Store bot response
    st.session_state.messages.append({"role": "bot", "content": translated})

# Display chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

        # Voice output for bot
        if msg["role"] == "bot":
            tts = gTTS(msg["content"], lang="hi")  # use same lang as translation
            mp3_fp = BytesIO()
            tts.write_to_fp(mp3_fp)
            mp3_fp.seek(0)
            audio_bytes = mp3_fp.read()
            audio_base64 = base64.b64encode(audio_bytes).decode()
            audio_html = f"""
                <audio autoplay controls>
                <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
                </audio>
            """
            st.markdown(audio_html, unsafe_allow_html=True)
