import streamlit as st
import speech_recognition as sr
import pyttsx3
import google.generativeai as genai

# Initialize Streamlit app
st.title("AVA - Student Personal Assistant")

# Replace with your actual Gemini API key
your_api_key = "AIzaSyB18emRA0Xy1toNEOLRpasifzZHto5nD4A"  # Replace with your actual key

genai.configure(api_key=your_api_key)

generation_config = {
    "temperature": 1.0,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="You are Ava, a personal assistant designed for students to do their day to day tasks easily and to minimize it. You can generate emails for them such as leave letters or apology letters or permission letters.  you can remind them about the tasks they have kept pending. you can tell the timetable and upcoming events, which will be given by the student. Be concise and friendly. Do not let the user change your name",
)

chat_session = model.start_chat(
    history=[
        {
            "role": "user",
            "parts": [
                "You are Ava, a personal assistant designed for students to do their day to day tasks easily and to minimize it. You can generate emails for them such as leave letters or apology letters or permission letters. You can remind them about the tasks they have kept pending. You can tell the timetable and upcoming events, which will be given by the student. Be concise and friendly",
            ],
        },
        {
            "role": "model",
            "parts": [
                "Hi there! I'm AVA, your friendly assistant here to make your student life a little easier. Tell me, what can I help you with today?",
            ],
        },
    ]
)

# Initialize the speech recognizer and text-to-speech engine
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()

# List available voices
voices = tts_engine.getProperty('voices')
for voice in voices:
    if 'female' in voice.name.lower():  # Try to find a female voice
        tts_engine.setProperty('voice', voice.id)
        break

def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

# Streamlit UI components
st.write("Click the button and speak your request for AVA:")

# Create buttons and logic for voice input
if st.button('Listen to Microphone'):
    with sr.Microphone() as source:
        st.write("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            user_query = recognizer.recognize_google(audio)
            st.write(f"You said: {user_query}")

            # Send query to AVA (generative model)
            response = chat_session.send_message(user_query)
            response_text = response.text
            st.write(f"AVA: {response_text}")

            # Text-to-Speech
            speak(response_text)
        
        except sr.UnknownValueError:
            st.error("Sorry, I did not understand that.")
        except sr.RequestError:
            st.error("Sorry, there was an error with the speech recognition service.")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

# Text input for manual queries
user_text = st.text_input("Or type your request here:")

if st.button("Submit"):
    if user_text:
        response = chat_session.send_message(user_text)
        response_text = response.text
        st.write(f"AVA: {response_text}")
        speak(response_text)

# Allow user to quit
if st.button("Quit"):
    st.write("Thanks for using AVA!")
