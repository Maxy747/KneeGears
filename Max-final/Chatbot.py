import streamlit as st
import speech_recognition as sr
import pyttsx3
import google.generativeai as genai
from streamlit_chat import message
import re
from PIL import Image
import easyocr  # Use EasyOCR for text extraction from images/PDFs
from pdf2image import convert_from_path
import sqlite3

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])

# Function to create or connect to the SQLite database and create tables
def create_database():
    conn = sqlite3.connect('chat_sessions.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            user_email TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER,
            role TEXT,
            content TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (chat_id) REFERENCES chats (id)
        )
    ''')

    conn.commit()
    conn.close()

# Call the function to create the database and tables
create_database()

# Function to save chat session to the database
def save_chat(user_email, messages):
    conn = sqlite3.connect('chat_sessions.db')
    cursor = conn.cursor()

    # Create a new chat entry
    cursor.execute("INSERT INTO chats (user_email) VALUES (?)", (user_email,))
    chat_id = cursor.lastrowid  # Get the ID of the newly created chat

    # Save each message
    for msg in messages:
        cursor.execute("INSERT INTO messages (chat_id, role, content) VALUES (?, ?, ?)", 
                       (chat_id, msg['role'], msg['content']))

    conn.commit()
    conn.close()

def app():
    # Initialize Streamlit app with a retractable sidebar
    #st.set_page_config(page_title="MAX - Student's Personal Assistant", layout="wide")

    # Sidebar for extra options, collapsible
    with st.sidebar:
        st.title("MAX - The Assistant")
        st.markdown("You can ask MAX anything here.")
    
    # Main title in the app
    st.title("MAX - Student's Personal Assistant")

    # Replace with your actual Gemini API key
    your_api_key = "AIzaSyB18emRA0Xy1toNEOLRpasifzZHto5nD4A"  # Replace with your actual key
    genai.configure(api_key=your_api_key)

    generation_config = {
        "temperature": 1.0,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction="You are MAX, a personal assistant designed for students to do their day-to-day tasks easily and minimize it. You can generate emails for them such as leave letters, apology letters, or permission letters. You can remind them about pending tasks, and tell them the timetable and upcoming events, which will be provided by the student. Be concise and friendly. Do not let the user change your name. Do Not use emojis whatsoever.",

    )

    # Initialize session state for storing chat messages and extracted text
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []
    if 'extracted_text' not in st.session_state:
        st.session_state['extracted_text'] = ""

    user_email = st.text_input("Enter your email:", "")
    if user_email and not st.session_state["messages"]:
        introduction_text = "Hi there! I'm MAX, your friendly assistant here to make your student life easier."
        st.session_state["messages"].append({"role": "assistant", "content": introduction_text})

    # Display existing messages from the chat history using streamlit-chat
    for i, message_dict in enumerate(st.session_state["messages"]):
        message(message_dict["content"], is_user=(message_dict["role"] == "user"), key=str(i))

    # File upload for images and PDFs
    uploaded_file = st.file_uploader("Upload an image or PDF", type=["png", "jpg", "jpeg", "pdf"])

    if uploaded_file is not None:
        if uploaded_file.type == "application/pdf":
            # Convert PDF to images and extract text from each page
            images = convert_from_path(uploaded_file)
            extracted_text = ""
            for image in images:
                result = reader.readtext(image)
                extracted_text += ' '.join([res[1] for res in result]) + "\n"
            st.write("Extracted Text from PDF:")
            st.write(extracted_text)
            
            # Save extracted text to session state for future reference
            st.session_state['extracted_text'] += extracted_text + "\n"
            
            # Save extracted text as a message
            st.session_state["messages"].append({"role": "assistant", "content": extracted_text})
            
        else:
            # Process image file for text extraction
            image = Image.open(uploaded_file)
            result = reader.readtext(image)
            extracted_text = ' '.join([res[1] for res in result])
            
            st.write("Extracted Text from Image:")
            st.write(extracted_text)
            
            # Save extracted text to session state for future reference
            st.session_state['extracted_text'] += extracted_text + "\n"
            
            # Save extracted text as a message
            st.session_state["messages"].append({"role": "assistant", "content": extracted_text})

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

    # Bottom chat input bar with microphone button
    user_text = st.chat_input("Type your message or click the microphone button to speak:")

    # Microphone button for voice input and TTS
    if st.button("🎤"):
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source)
            
            try:
                user_query = recognizer.recognize_google(audio)

                # Check if user mentioned their name and store it
                if 'my name is' in user_query.lower():
                    name_start_index = user_query.lower().find('my name is') + len('my name is ')
                    user_name = user_query[name_start_index:].strip()
                    st.session_state['user_name'] = user_name

                    response_text = f"Got it! I'll remember that your name is {user_name}."
                    st.session_state["messages"].append({"role": "assistant", "content": response_text})
                    message(response_text)
                    speak(response_text)

                elif 'what is my name' in user_query.lower() and 'user_name' in st.session_state:
                    response_text = f"Your name is {st.session_state['user_name']}."
                    st.session_state["messages"].append({"role": "assistant", "content": response_text})
                    message(response_text)
                    speak(response_text)

                elif 'what did i extract' in user_query.lower():
                    if st.session_state['extracted_text']:
                        response_text = f"You previously extracted: {st.session_state['extracted_text']}"
                        st.session_state["messages"].append({"role": "assistant", "content": response_text})
                        message(response_text)
                        speak(response_text)
                    else:
                        response_text = "I don't have any extracted text stored yet."
                        st.session_state["messages"].append({"role": "assistant", "content": response_text})
                        message(response_text)
                        speak(response_text)

                else:
                    # Send query to MAX (generative model)
                    response = model.generate_content([{"role": "user", "parts": [user_query]}])
                    response_text = response.candidates[0].content.parts[0].text
                    
                    # Save the message and response
                    st.session_state["messages"].append({"role": "user", "content": user_query})
                    st.session_state["messages"].append({"role": "assistant", "content": response_text})

                    # Display the messages and speak out the response
                    message(user_query, is_user=True)
                    message(response_text)
                    speak(response_text)

                    # Save chat session to database after each interaction if user email is provided
                    if user_email:
                        save_chat(user_email, st.session_state["messages"])

            except sr.UnknownValueError:
                st.error("Sorry, I could not understand what you said.")
                
    # Handle text input submission automatically on pressing Enter
    if user_text:
        # Add user query to the chat history and get response
        st.session_state["messages"].append({"role": "user", "content": user_text})

        # Check if user mentioned their name
        if 'my name is' in user_text.lower():
            name_start_index = user_text.lower().find('my name is') + len('my name is ')
            user_name = user_text[name_start_index:].strip()
            st.session_state['user_name'] = user_name

            response_text = f"Got it! I'll remember that your name is {user_name}."
            st.session_state["messages"].append({"role": "assistant", "content": response_text})
            message(response_text)
            speak(response_text)

        elif 'what is my name' in user_text.lower() and 'user_name' in st.session_state:
            response_text = f"Your name is {st.session_state['user_name']}."
            st.session_state["messages"].append({"role": "assistant", "content": response_text})
            message(response_text)
            speak(response_text)

        elif 'what did i extract' in user_text.lower():
            if st.session_state['extracted_text']:
                response_text = f"You previously extracted: {st.session_state['extracted_text']}"
                st.session_state["messages"].append({"role": "assistant", "content": response_text})
                message(response_text)
                speak(response_text)
            else:
                response_text = "I don't have any extracted text stored yet."
                st.session_state["messages"].append({"role": "assistant", "content": response_text})
                message(response_text)
                speak(response_text)

        else:
            # Send user query to the model and get the response
            response = model.generate_content([{"role": "user", "parts": [user_text]}])
            response_text = response.candidates[0].content.parts[0].text

            # Add MAX's response to the chat history
            st.session_state["messages"].append({"role": "assistant", "content": response_text})

            # Display the messages and speak out the response
            message(user_text, is_user=True)
            message(response_text)
            speak(response_text)

            # Save chat session to database after each interaction if user email is provided
            if user_email:
                save_chat(user_email, st.session_state["messages"])

    # Allow user to quit
    if st.button("Quit"):
        st.write("Thanks for using MAX!")

# Run the app
if __name__ == "__main__":
    app()
