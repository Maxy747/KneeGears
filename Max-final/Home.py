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

    # Custom CSS for credits at the bottom-right
    custom_css = """
    <style>
    .credits {
        position: fixed;
        bottom: 10px;
        right: 10px;
        font-size: 14px;
        color: rgba(0, 0, 0, 0.5);  /* Translucent color */
        background-color: rgba(255, 255, 255, 0.3);  /* Light translucent background */
        padding: 5px 10px;
        border-radius: 5px;
        z-index: 1000;
    }
    </style>
    """

    # Inject the CSS
    st.markdown(custom_css, unsafe_allow_html=True)

    # Credits
    st.markdown('<div class="credits">Credits: Kneegears | Members: Mazin, Aswin, Libin, Ahmad</div>', unsafe_allow_html=True)

# Call the app function to run the Streamlit app
if __name__ == '__main__':
    app()
