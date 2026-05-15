import streamlit as st
import json
from gtts import gTTS
from io import BytesIO
import base64

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Medicine Chatbot",
    page_icon="🩺",
    layout="centered"
)

# ---------------- LOAD JSON DATA ----------------
with open("symptom_medicine_mapping_dict.json", "r") as f:
    medicine_data = json.load(f)

# ---------------- SESSION STATE ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- SIDEBAR ----------------
st.sidebar.title("💬 Chat History")

for i, msg in enumerate(st.session_state.messages):
    st.sidebar.write(f"{i+1}. {msg['role'].capitalize()}")
    st.sidebar.write(msg["content"])
    st.sidebar.write("---")

# ---------------- MAIN TITLE ----------------
st.title("🧑‍⚕️ AI Medicine Recommendation Chatbot")

st.write(
    "Enter your symptoms and get medicine recommendations with voice output."
)

# ---------------- CHAT INPUT ----------------
prompt = st.chat_input("Enter your symptom...")

if prompt:

    # Store user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # Default response
    response = "❌ Sorry, I couldn't find medicine for that symptom."

    # Search medicine data
    for med, info in medicine_data.items():

        cause_text = info["cause"].lower()

        if (
            prompt.lower() in cause_text
            or cause_text in prompt.lower()
        ):

            response = f"""
✅ Symptom: {prompt}

🦠 Cause:
{info['cause']}

💊 Suggested Medicine:
{med}

📋 Usage:
{info['medicine']}
"""

            break

    # Store assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

# ---------------- DISPLAY CHAT ----------------
for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):

        st.write(msg["content"])

        # ---------------- VOICE OUTPUT ----------------
        if msg["role"] == "assistant":

            try:

                tts = gTTS(
                    text=msg["content"],
                    lang="en"
                )

                mp3_fp = BytesIO()

                tts.write_to_fp(mp3_fp)

                mp3_fp.seek(0)

                audio_bytes = mp3_fp.read()

                audio_base64 = base64.b64encode(
                    audio_bytes
                ).decode()

                audio_html = f"""
                    <audio controls>
                        <source
                        src="data:audio/mp3;base64,{audio_base64}"
                        type="audio/mp3">
                    </audio>
                """

                st.markdown(
                    audio_html,
                    unsafe_allow_html=True
                )

            except:
                st.warning("Voice generation failed.")
