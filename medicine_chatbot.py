import streamlit as st
import json
from gtts import gTTS
from io import BytesIO
import base64
from googletrans import Translator

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Medicine Chatbot", page_icon="🩺")

# ---------------- LOAD JSON DATA ----------------
with open("symptom_medicine_mapping_dict.json", "r") as f:
    medicine_data = json.load(f)

# ---------------- SESSION STATE ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- TRANSLATOR ----------------
translator = Translator()

# ---------------- SIDEBAR ----------------
st.sidebar.title("💬 Chat History")

for i, msg in enumerate(st.session_state.messages):
    st.sidebar.write(f"{i+1}. {msg['role'].capitalize()}:")
    st.sidebar.write(msg["content"])
    st.sidebar.write("---")

# ---------------- TITLE ----------------
st.title("🧑‍⚕️ AI Medicine Recommendation Chatbot")

st.write("Enter your symptom and get medicine suggestions with voice output.")

# ---------------- LANGUAGE SELECTION ----------------
language_options = {
    "English": "en",
    "Hindi": "hi",
    "Telugu": "te",
    "Tamil": "ta"
}

selected_language = st.selectbox(
    "🌍 Select Language",
    list(language_options.keys())
)

target_lang = language_options[selected_language]

# ---------------- CHAT INPUT ----------------
prompt = st.chat_input("Enter your symptom...")

if prompt:

    # Store user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # ---------------- FIND MEDICINE ----------------
    response = "❌ Sorry, I couldn't find any medicine for that symptom."

    for med, info in medicine_data.items():

        cause_text = info["cause"].lower()

        # Better matching
        if prompt.lower() in cause_text or cause_text in prompt.lower():

            response = f"""
✅ Symptom: {prompt}

🦠 Cause:
{info['cause']}

💊 Suggested Medicine:
{med}

📋 Conditions:
{info['medicine']}
"""
            break

    # ---------------- TRANSLATE ----------------
    try:
        translated_response = translator.translate(
            response,
            dest=target_lang
        ).text
    except:
        translated_response = response

    # Store assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": translated_response
    })

# ---------------- DISPLAY CHAT ----------------
for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):

        st.write(msg["content"])

        # ---------------- TEXT TO SPEECH ----------------
        if msg["role"] == "assistant":

            try:
                tts = gTTS(
                    text=msg["content"],
                    lang=target_lang
                )

                mp3_fp = BytesIO()
                tts.write_to_fp(mp3_fp)
                mp3_fp.seek(0)

                audio_bytes = mp3_fp.read()

                audio_base64 = base64.b64encode(audio_bytes).decode()

                audio_html = f"""
                    <audio controls>
                        <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
                    </audio>
                """

                st.markdown(audio_html, unsafe_allow_html=True)

            except:
                st.warning("Voice generation failed.")
