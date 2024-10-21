import streamlit as st

def app():
    st.title("Home Page")
    st.write("Welcome to the Academic Assistance Platform!")
    
    # Project Description
    st.subheader("About Our Project")
    st.write("""
        This platform is designed to assist students with their academic needs, offering a range of tools 
        and services to make studying more efficient and manageable. Our aim is to support students 
        in achieving their academic goals by providing personalized assistance, resources, and 
        communication tools.
    """)
    
    # Project Uses
    st.subheader("How This Platform Can Help You")
    st.write("""
        - **Chatbot Assistance**: Use the chatbot feature to get quick answers to academic questions, 
          generate study materials, or receive help with assignments.
        - **Task Reminders**: Set up reminders for important tasks and deadlines to keep your studies on track.
        - **Telegram Integration**: Chat with our Telegram bot for on-the-go academic support. 
          The bot can help answer questions, provide study tips, and even remind you about your upcoming deadlines.
        - **Academic Resources**: Access a variety of educational resources, including study guides, 
          tutoring services, and online learning tools.
    """)
    
    st.write("We are here to make your academic journey smoother and more enjoyable. Explore the features and start using the tools to enhance your learning experience!")
