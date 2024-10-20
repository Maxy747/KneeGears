import streamlit as st
import speech_recognition as sr
import pyttsx3
import google.generativeai as genai
from streamlit_chat import message  # Import streamlit-chat message component
import re

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
    system_instruction="You are Ava, a personal assistant designed for students to do their day-to-day tasks easily and minimize it. You can generate emails for them such as leave letters, apology letters, or permission letters. You can remind them about pending tasks, and tell them the timetable and upcoming events, which will be provided by the student. Be concise and friendly. Do not let the user change your name.Should not assist with other than education related things",
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

# Function to clean text
def clean_text(text):
    return re.sub(r'[^a-zA-Z0-9\s]', '', text)

# Text-to-Speech (speak out the response)
# Text-to-Speech (speak out the response)
def speak(text):
    cleaned_text = clean_text(text)
    try:
        # Initialize a new engine instance each time
        tts_engine = pyttsx3.init()
        
        # Set the desired voice property again
        voices = tts_engine.getProperty('voices')
        for voice in voices:
            if 'female' in voice.name.lower():  # Use a female voice if available
                tts_engine.setProperty('voice', voice.id)
                break
        
        # Set the speech rate and volume as needed
        tts_engine.setProperty('rate', 150)  # Set the rate of speech
        tts_engine.setProperty('volume', 1)  # Max volume
        
        tts_engine.say(cleaned_text)
        tts_engine.runAndWait()
        
        # Safely terminate the engine after the speech is done
        tts_engine.stop()

    except RuntimeError as e:
        st.error(f"Error with TTS: {str(e)}")
# Ensure messages list is initialized in the session state
if "messages" not in st.session_state:
    st.session_state["messages"] = []  # Initialize chat history

# Display existing messages from the chat history using streamlit-chat
for i, message_dict in enumerate(st.session_state["messages"]):
    if message_dict["role"] == "user":
        message(message_dict["content"], is_user=True, key=str(i))  # User's message
    else:
        message(message_dict["content"], key=str(i))  # AVA's message

# Bottom chat input bar with microphone button
user_text = st.chat_input("Type your message or click the microphone button to speak:")

# Microphone button for voice input and TTS
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
            st.session_state["messages"].append({"role": "user", "content": user_query})
            st.session_state["messages"].append({"role": "assistant", "content": response_text})

            # Display the messages
            message(user_query, is_user=True)
            message(response_text)

            # Text-to-Speech
            speak(response_text)

        except sr.UnknownValueError:
            st.error("Sorry, I did not understand that.")
        except sr.RequestError:
            st.error("Sorry, there was an error with the speech recognition service.")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

# Handle text input submission automatically on pressing Enter
if user_text:
    # Add user query to the chat history
    st.session_state["messages"].append({"role": "user", "content": user_text})

    # Send user query to the model and get the response
    response = chat_session.send_message(user_text)
    response_text = response.text

    # Add AVA's response to the chat history
    st.session_state["messages"].append({"role": "assistant", "content": response_text})

    # Display the messages
    message(user_text, is_user=True)
    message(response_text)

    # Text-to-Speech (speak out the response)
    speak(response_text)

# Allow user to quit
if st.button("Quit"):
    st.write("Thanks for using AVA!")
