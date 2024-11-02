import streamlit as st
import speech_recognition as sr
import pyttsx3
import google.generativeai as genai
from streamlit_chat import message
import re

def app():
    # Initialize Streamlit app with a retractable sidebar
    st.set_page_config(page_title="MEDI - Personal Health Assistant", layout="wide")

    # Sidebar for extra options, collapsible
    with st.sidebar:
        st.title("MEDI - Your Health Assistant")
        st.markdown("You can ask MEDI anything related to your diet and prescriptions.")
        st.markdown("### About")
        st.markdown("MEDI helps you manage your dietary needs and understand medical prescriptions easily!")

    # Main title in the app
    st.title("MEDI - Your Personal Health Assistant")

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
        system_instruction="You are MEDI, a personal health assistant designed to help users manage their dietary needs and understand medical prescriptions easily. You can generate personalized meal plans based on users' medical conditions and dietary preferences. You can also interpret and simplify doctors' prescriptions into easy-to-understand language. Additionally, you can remind users about their dietary goals and provide information on upcoming health-related events. Be concise, friendly, and supportive.",
    )

    # Initialize chat session with an introduction from MEDI
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    "You are MEDI, a personal health assistant designed to help users manage their dietary needs and understand medical prescriptions easily. You can generate personalized meal plans based on users' medical conditions and dietary preferences. You can also interpret and simplify doctors' prescriptions into easy-to-understand language. Additionally, you can remind users about their dietary goals and provide information on upcoming health-related events. Be concise, friendly, and supportive.",
                ],
            },
            {
                "role": "model",
                "parts": [
                    "Hi there! I'm MEDI, your friendly health assistant here to help you with your diet and prescriptions. How can I assist you today?",
                ],
            },
        ]
    )

    # Initialize the speech recognizer and text-to-speech engine
    recognizer = sr.Recognizer()
    tts_engine = pyttsx3.init()

    # List available voices and set a female voice if available
    voices = tts_engine.getProperty('voices')
    for voice in voices:
        if 'female' in voice.name.lower():
            tts_engine.setProperty('voice', voice.id)
            break

    def clean_text(text):
        return re.sub(r'[^a-zA-Z0-9\s]', '', text)

    def speak(text):
        cleaned_text = clean_text(text)
        try:
            tts_engine.say(cleaned_text)
            tts_engine.runAndWait()
        except RuntimeError as e:
            if str(e) == 'run loop already started':
                pass

    # Ensure messages list is initialized in the session state
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
        # Introduce MEDI when starting for the first time
        introduction_text = "Hi there! I'm MEDI, your friendly health assistant here to help you with your diet and prescriptions."
        st.session_state["messages"].append({"role": "assistant", "content": introduction_text})
        speak(introduction_text)

    # Display existing messages from the chat history using streamlit-chat
    for i, message_dict in enumerate(st.session_state["messages"]):
        if message_dict["role"] == "user":
            message(message_dict["content"], is_user=True, key=str(i))
        else:
            message(message_dict["content"], key=str(i))

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

                # Send query to MEDI (generative model)
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

        # Add MEDI's response to the chat history
        st.session_state["messages"].append({"role": "assistant", "content": response_text})

        # Display the messages
        message(user_text, is_user=True)
        message(response_text)

        # Text-to-Speech (speak out the response)
        speak(response_text)

    # Allow user to quit
    if st.button("Quit"):
        st.write("Thanks for using MEDI!")

# Call the app function to run the chatbot
if __name__ == "__main__":
    app()
    #nigga