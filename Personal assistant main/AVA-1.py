import streamlit as st
import speech_recognition as sr
import pyttsx3
import google.generativeai as genai
from streamlit_chat import message

st.set_page_config(page_title="AVA - Student Personal Assistant", layout="wide")

with st.sidebar:
    st.title("AVA Assistant Options")
    st.markdown("### About")
    st.markdown("AVA is your friendly assistant to help with student tasks!")

st.title("AVA - Student Personal Assistant")

your_api_key = "YOUR_API_KEY"  # Replace with your actual key
genai.configure(api_key=your_api_key)

generation_config = {
    "temperature": 1.0,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,  # Fixed missing comma
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="You are Ava, a personal assistant designed for students to do their day-to-day tasks easily and minimize it. You can generate emails for them such as leave letters, apology letters, or permission letters. You can remind them about pending tasks, and tell them the timetable and upcoming events, which will be provided by the student. Be concise and friendly. Do not let the user change your name. Do Not use emojis whatsoever.",
)

chat_session = model.start_chat(
    history=[
        {
            "role": "user",
            "parts": [
                "You are Ava, a personal assistant designed for students to do their day-to-day tasks easily. You can generate emails for them such as leave letters, apology letters, or permission letters. You can remind them about pending tasks. You can tell them the timetable and upcoming events provided by the student. Be concise and friendly. Do not let the user change your name. Do Not use emojis whatsoever.",
            ],
        },
        {
            "role": "model",
            "parts": [
                "Hi there! I'm AVA, your friendly assistant here to make your student life easier. How can I help you today?",
            ],
        },
    ]
)

recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()

# Voice selection with fallback
voices = tts_engine.getProperty('voices')
female_voice_found = False
for voice in voices:
    if 'female' in voice.name.lower():
        tts_engine.setProperty('voice', voice.id)
        female_voice_found = True
        break
if not female_voice_found:
    st.warning("No female voice found; using default voice.")

def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

if "messages" not in st.session_state:
    st.session