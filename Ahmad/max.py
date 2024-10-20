import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import google.generativeai as genai
from streamlit_chat import message
import html
import io
import pyttsx3
import threading

# Initialize Streamlit app with a retractable sidebar
st.set_page_config(page_title="MAX - Student Personal Assistant", layout="wide")

# Sidebar for extra options, collapsible
with st.sidebar:
    st.title("MAX Assistant Options")
    st.markdown("You can manage MAX's settings here.")
    st.markdown("### About")
    st.markdown("MAX is your friendly assistant to help with student tasks!")

# Main title in the app
st.title("MAX - THE ASSISTANT")

# Replace with your Gemini API key
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
    system_instruction="You are Max, a personal assistant designed for students to do their day-to-day tasks easily and minimize it. You can generate emails for them such as leave letters, apology letters, or permission letters. You can remind them about pending tasks, and tell them the timetable and upcoming events, which will be provided by the student. Be concise and friendly. Do not let the user change your name.",
)

chat_session = model.start_chat(
    history=[
        {
            "role": "user",
            "parts": [
                "You are Max, a personal assistant designed for students to do their day-to-day tasks easily. You can generate emails for them such as leave letters, apology letters, or permission letters. You can remind them about pending tasks. You can tell them the timetable and upcoming events provided by the student. Be concise and friendly.",
            ],
        },
        {
            "role": "model",
            "parts": [
                "Hi there! I'm MAX, your friendly assistant here to make your student life easier. How can I help you today?",
            ],
        },
    ]
)

# Initialize the speech recognizer
recognizer = sr.Recognizer()

# Initialize the text-to-speech engine
tts_engine = pyttsx3.init()

def speak(text):
    def run_speak():
        tts_engine.say(text)
        tts_engine.runAndWait()
    threading.Thread(target=run_speak).start()

# Layout of the chat
chat_container = st.container()

# Streamlit UI components for conversation
with chat_container:
    st.write("Talk to MAX:")

    # Message history display as bubbles
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    for i, msg in enumerate(st.session_state["messages"]):
        if msg['role'] == 'user':
            message(html.escape(msg['content']), is_user=True, key=f"{i}_user")
        else:
            message(html.escape(msg['content']), is_user=False, key=f"{i}_max")

# Bottom input bar with a single mic button
with st.container():
    col1, col2 = st.columns([10, 1])

    # Text input
    with col1:
        user_text = st.text_input("Your message", key="message_input")

    # Mic button for voice input and TTS
    with col2:
        if st.button("🎤"):
            with sr.Microphone() as source:
                st.write("Listening...")
                recognizer.adjust_for_ambient_noise(source, duration=1)
                try:
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                    user_query = recognizer.recognize_google(audio)
                    st.write(f"You said: {user_query}")

                    # Send query to MAX (generative model)
                    response = chat_session.send_message(user_query)
                    response_text = response.text

                    # Save the message and response
                    st.session_state["messages"].append({"role": "user", "content": user_query})
                    st.session_state["messages"].append({"role": "max", "content": response_text})
                    message(html.escape(user_query), is_user=True, key=f"{len(st.session_state['messages'])}_user")
                    message(html.escape(response_text), is_user=False, key=f"{len(st.session_state['messages'])}_max")

                    # Text-to-Speech
                    speak(response_text)

                except sr.UnknownValueError:
                    st.error("Sorry, I did not understand that.")
                except sr.RequestError:
                    st.error("Sorry, there was an error with the speech recognition service.")
                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")

    # Handle text input submission
    if user_text and st.button("Send", key="send_message"):
        # Send user query to the model and get the response
        response = chat_session.send_message(user_text)
        response_text = response.text

        # Save the message and response
        st.session_state["messages"].append({"role": "user", "content": user_text})
        st.session_state["messages"].append({"role": "max", "content": response_text})
        message(html.escape(user_text), is_user=True, key=f"{len(st.session_state['messages'])}_user")
        message(html.escape(response_text), is_user=False, key=f"{len(st.session_state['messages'])}_max")

        # Text-to-Speech
        speak(response_text)

# Allow user to quit
if st.button("Quit"):
    st.write("Thanks for using MAX!")