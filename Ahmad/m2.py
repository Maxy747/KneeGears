import re
import streamlit as st
import speech_recognition as sr
import pyttsx3
import google.generativeai as genai
from streamlit_chat import message  # Import streamlit-chat message component

# Initialize Streamlit app with a retractable sidebar
st.set_page_config(page_title="AVA - Student Personal Assistant", layout="wide")

# Sidebar for extra options, collapsible
with st.sidebar:
    st.title("AVA Assistant Options")
    st.markdown("### About")
    st.markdown("AVA is your friendly assistant to help with student tasks!")

# Main title in the app
st.title("AVA - Student Personal Assistant")

# Replace with your actual Gemini API key
your_api_key = "YOUR_ACTUAL_API_KEY"  # Make sure this is a valid API key
genai.configure(api_key=your_api_key)

# Initialize TTS engine
tts_engine = pyttsx3.init()

# Initialize speech recognition
recognizer = sr.Recognizer()

# Function to capture user speech and convert to text
def recognize_speech():
    with sr.Microphone() as source:
        st.write("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            st.write(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            st.write("Sorry, I did not understand that.")
        except sr.RequestError:
            st.write("Sorry, my speech service is down.")
    return ""

# Function to clean text by removing special symbols
def clean_text(text):
    cleaned_text = re.sub(r'[^\w\s]', '', text)
    return cleaned_text

# Function to convert text to speech
def speak_text(text):
    cleaned_text = clean_text(text)
    tts_engine.say(cleaned_text)
    tts_engine.runAndWait()

# Function to generate response using NLP model
def generate_response(user_input):
    try:
        response = genai.generate_text(prompt=user_input)
        return response.generations[0].text if response.generations else "Sorry, I couldn't generate a response."
    except Exception as e:
        st.write(f"Error generating response: {e}")
        return "I'm sorry, I couldn't generate a response."

# Main loop for chatbot interactions
st.write("You can either type or use voice to talk to AVA.")

# Text input box
text_input = st.text_input("Type your message here:")

# Button for speech input
if st.button("Talk to AVA"):
    user_input = recognize_speech()
    if user_input:
        response = generate_response(user_input)
        st.write(f"AVA: {response}")
        speak_text(response)

# Handle text input
if text_input:
    response = generate_response(text_input)
    st.write(f"AVA: {response}")
    speak_text(response)
