# Import necessary libraries
import streamlit as st
import google.generativeai as gen_ai
from my_module import setup_generative_model

GOOGLE_API_KEY = "AIzaSyANEPbvNBIhE_VHGGe1pV5f2vu0_7-BJ6Y"

# Initialize the generative model with the API key
model = setup_generative_model(GOOGLE_API_KEY)

# Streamlit app setup
st.title("Fitness and Nutrition Chatbot")

# Initialize session state for conversation history
if 'conversation' not in st.session_state:
    st.session_state.conversation = []

# Function to handle sending messages
def send_message(message):
    # Append user message to conversation history
    st.session_state.conversation.append(f"You: {message}")
    
    # Generate response using the generative model
    response = model.generate(prompt=message, max_length=50)
    
    # Append model response to conversation history
    st.session_state.conversation.append(f"Chatbot: {response}")
    
    # Clear input box after sending the message
    st.session_state.message = ""

# User input
user_message = st.text_input("Message", key="message")

# Send button
if st.button("Send"):
    send_message(user_message)

# Display conversation history
st.text_area("Conversation", value="\n".join(st.session_state.conversation), height=300)
