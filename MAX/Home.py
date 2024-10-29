import streamlit as st

def app():
    # Set page title and icon
    #st.set_page_config(page_title="Academic Assistance Platform", page_icon="🎓")

    # Custom CSS for styling
    st.markdown("""
        <style>
            .title {
                text-align: center;
                color: #4CAF50;  /* Green color */
                font-size: 2.5em;
                margin-bottom: 20px;
            }
            .subheader {
                color: #f9f9f9;
                font-size: 1.8em;
                margin-top: 20px;
            }
            .content {
                font-size: 1.1em;
                line-height: 1.6;
            }
            .feature-list {
                background-color: #f9f9f9; /* Light grey background */
                border-radius: 5px;
                padding: 15px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
        </style>
    """, unsafe_allow_html=True)

    # Page content
    st.markdown('<h1 class="title">Home Page</h1>', unsafe_allow_html=True)
    st.write("Welcome to the Academic Assistance Platform!")

    # Project Description
    st.markdown('<h2 class="subheader">About Our Project</h2>', unsafe_allow_html=True)
    st.markdown("""
        <div class="content">
        This platform is designed to assist students with their academic needs, offering a range of tools 
        and services to make studying more efficient and manageable. Our aim is to support students 
        in achieving their academic goals by providing personalized assistance, resources, and 
        communication tools.
        </div>
    """, unsafe_allow_html=True)
    
    # Project Uses
    st.markdown('<h2 class="subheader">How This Platform Can Help You</h2>', unsafe_allow_html=True)
    
    st.markdown('<div class="feature-list">', unsafe_allow_html=True)
    st.write("""
        - **Chatbot Assistance**: Use the chatbot feature to get quick answers to academic questions, 
          generate study materials, or receive help with assignments.
        - **Task Reminders**: Set up reminders for important tasks and deadlines to keep your studies on track.
        - **Telegram Integration**: Chat with our Telegram bot for on-the-go academic support. 
          The bot can help answer questions, provide study tips, and even remind you about your upcoming deadlines.
        - **Academic Resources**: Access a variety of educational resources, including study guides, 
          tutoring services, and online learning tools.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
        <div class="content">
        We are here to make your academic journey smoother and more enjoyable. Explore the features and start using the tools to enhance your learning experience!
        </div>
    """, unsafe_allow_html=True)
