import streamlit as st
import google.generativeai as genai
import speech_recognition as sr
import pyttsx3
from datetime import datetime
import json
import re
import threading

# Configure Gemini API
genai.configure(api_key='AIzaSyDsp-Q1M2CM548oSCoAAO_UCAaeM2dOdVI')
model = genai.GenerativeModel('gemini-pro')

# Initialize speech recognition
recognizer = sr.Recognizer()

# Initialize session state with default values
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'user_info' not in st.session_state:
    st.session_state.user_info = {}
if 'current_question_index' not in st.session_state:
    st.session_state.current_question_index = 0
if 'questioning_mode' not in st.session_state:
    st.session_state.questioning_mode = False
if 'memory' not in st.session_state:
    st.session_state.memory = {
        'name': None,
        'preferences': {},
        'context': []
    }

# Question flow for recipes
RECIPE_QUESTIONS = [
    "What are your dietary preferences? Do you have any allergies or restrictions?",
    "What is your current lifestyle like? Are you active or sedentary?",
    "What are your cooking skills and how much time do you have to cook?"
]

def create_tts_engine():
    engine = pyttsx3.init()
    return engine

def clean_text_for_speech(text):
    """Clean text to contain only alphanumeric characters and basic punctuation"""
    cleaned_text = re.sub(r'[^a-zA-Z0-9\s.,?!]', ' ', text)
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    cleaned_text = re.sub(r'\s+([.,?!])', r'\1', cleaned_text)
    return cleaned_text.strip()

def text_to_speech(text):
    """Convert text to speech using only alphanumeric characters"""
    try:
        engine = create_tts_engine()
        cleaned_text = clean_text_for_speech(text)
        engine.say(cleaned_text)
        engine.runAndWait()
        engine.stop()
        del engine
    except Exception as e:
        st.error(f"Speech Error: {str(e)}")

def speak_in_thread(text):
    """Run text-to-speech in a separate thread"""
    thread = threading.Thread(target=text_to_speech, args=(text,))
    thread.start()

def update_memory(user_input, bot_response):
    """Update bot's memory based on conversation"""
    # Extract name if mentioned
    name_match = re.search(r"my name is (\w+)", user_input.lower())
    if name_match:
        st.session_state.memory['name'] = name_match.group(1).capitalize()
    
    # Store recent context
    st.session_state.memory['context'].append({
        'user_input': user_input,
        'bot_response': bot_response,
        'timestamp': str(datetime.now())
    })
    
    # Keep only last 10 conversations for context
    if len(st.session_state.memory['context']) > 10:
        st.session_state.memory['context'] = st.session_state.memory['context'][-10:]

def get_memory_context():
    """Get relevant context from memory"""
    context = ""
    if st.session_state.memory['name']:
        context += f"The user's name is {st.session_state.memory['name']}. "
    
    # Add recent conversation context
    if st.session_state.memory['context']:
        context += "Recent conversations:\n"
        for conv in st.session_state.memory['context'][-3:]:  # Last 3 conversations
            context += f"User: {conv['user_input']}\nAssistant: {conv['bot_response']}\n"
    
    return context

def get_bot_response(user_input):
    """Get response from Gemini API for general queries"""
    memory_context = get_memory_context()
    
    # Special handling for name query
    if user_input.lower().strip() in ["my name is?", "what is my name?", "what's my name?"]:
        if st.session_state.memory['name']:
            return f"Your name is {st.session_state.memory['name']}."
        else:
            return "I don't know your name yet. You can tell me by saying 'My name is [your name]'."
    
    context = f"""You are MAX, a professional diet planning assistant. Keep responses focused on nutrition and diet advice. 
Be direct and concise. Always use the user's name if available.

Memory Context:
{memory_context}"""
    
    prompt = f"{context}\nUser: {user_input}\nMAX:"
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return "I apologize, but I'm having trouble generating a response right now. Could you please try again?"

def handle_user_input(user_input):
    """Process user input and update chat history"""
    if not user_input.strip():
        return
        
    # Add user message to chat history
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_input
    })
    
    # Process the input and get response
    if "healthy recipes" in user_input.lower():
        st.session_state.questioning_mode = True
        st.session_state.current_question_index = 0
        bot_response = RECIPE_QUESTIONS[0]
    else:
        bot_response = get_bot_response(user_input)
    
    # Update memory and add bot response to chat history
    update_memory(user_input, bot_response)
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": bot_response
    })
    
    # Handle speech in a separate thread
    speak_in_thread(bot_response)
    
    # Clear the input field by forcing a rerun
    st.session_state.user_message = ""

# Streamlit UI
st.title("MAX - Your Personal Diet Planning Assistant")
st.write("I can help you create a personalized diet plan. You can type or speak!")

# Create a container for chat history
chat_container = st.container()

# Create a container for input
input_container = st.container()

with input_container:
    # Create columns for input field and buttons
    col1, col2 = st.columns([4, 1])
    
    with col1:
        # Use a key different from the session state key to avoid conflicts
        user_input = st.text_input(
            "Your message",
            key="input_field",
            value=st.session_state.get('user_message', ''),
            on_change=lambda: handle_user_input(st.session_state.input_field) if st.session_state.input_field else None
        )
    
    with col2:
        speak_button = st.button("🎤 Speak")

# Handle speech input
if speak_button:
    with sr.Microphone() as source:
        st.write("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5)
            user_input = recognizer.recognize_google(audio)
            handle_user_input(user_input)
        except Exception as e:
            st.error("Could not understand audio")

# Display chat history in the container
with chat_container:
    st.write("Chat History:")
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.write("You:", message["content"])
            st.write("---")
        else:
            st.markdown(f"**MAX:** {message['content']}")
            st.write("---")

# Clear chat button
if st.button("Clear Chat"):
    st.session_state.chat_history = []
    st.session_state.user_info = {}
    st.session_state.current_question_index = 0
    st.session_state.questioning_mode = False
    st.session_state.memory = {'name': None, 'preferences': {}, 'context': []}