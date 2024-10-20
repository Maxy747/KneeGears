import streamlit as st
import speech_recognition as sr
import pyttsx3
import google.generativeai as genai

# Initialize Streamlit app with a retractable sidebar
st.set_page_config(page_title="AVA - Student Personal Assistant", layout="wide")

# Sidebar for extra options, collapsible
with st.sidebar:
    st.title("AVA Assistant Options")
    st.markdown("You can manage AVA's settings here.")
    st.markdown("### About")
    st.markdown("AVA is your friendly assistant to help with student tasks!")

# Main title in the app
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
    system_instruction="You are Ava, a personal assistant designed for students to do their day-to-day tasks easily and minimize it. You can generate emails for them such as leave letters, apology letters, or permission letters. You can remind them about pending tasks, and tell them the timetable and upcoming events, which will be provided by the student. Be concise and friendly. Do not let the user change your name.",
)

chat_session = model.start_chat(
    history=[
        {
            "role": "user",
            "parts": [
                "You are Ava, a personal assistant designed for students to do their day-to-day tasks easily. You can generate emails for them such as leave letters, apology letters, or permission letters. You can remind them about pending tasks. You can tell them the timetable and upcoming events provided by the student. Be concise and friendly.",
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
######################################################################
# Helper function to display chat messages as text bubbles
def display_chat_bubble(user_message, ava_message):
    col1, col2 = st.columns([1, 4])  # Two columns for alternating messages
    with col1:
        st.image("https://user-images.githubusercontent.com/800545/63263114-a9207000-c265-11e9-815f-dbc7c605bc92.png", width=40)  # Placeholder user avatar
    with col2:
        st.markdown(f'<div style="background-color:#E2F0F9; padding: 10px; border-radius: 10px;"><strong>User:</strong> {user_message}</div>', unsafe_allow_html=True)

    col2, col1 = st.columns([4, 1])  # Reverse for AVA's response
    with col2: 
        st.markdown(f'<div style="background-color:#D5E8D4; padding: 10px; border-radius: 10px;"><strong>AVA:</strong> {ava_message}</div>', unsafe_allow_html=True)
    with col1:
        st.image("https://user-images.githubusercontent.com/800545/63263082-91e19480-c265-11e9-9951-431b27a6ea7b.png", width=40)  # Placeholder AVA avatar

# Layout of the chat
chat_container = st.container()

# Streamlit UI components for conversation
with chat_container:
    st.write("Talk to AVA:")

    # Message history display as bubbles
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    for message in st.session_state["messages"]:
        display_chat_bubble(message['user'], message['ava'])

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

                    # Send query to AVA (generative model)
                    response = chat_session.send_message(user_query)
                    response_text = response.text

                    # Save the message and response
                    st.session_state["messages"].append({"user": user_query, "ava": response_text})
                    display_chat_bubble(user_query, response_text)

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
        st.session_state["messages"].append({"user": user_text, "ava": response_text})
        display_chat_bubble(user_text, response_text)

        # Text-to-Speech
        speak(response_text)

# Allow user to quit
if st.button("Quit"):
    st.write("Thanks for using AVA!")
