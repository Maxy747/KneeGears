import streamlit as st
from streamlit_option_menu import option_menu
import Home
import Chatbot
import Telegram

# Set page configuration
#st.set_page_config(page_title="Multipage App", layout="wide")

# Sidebar for navigation
with st.sidebar:
    selected = option_menu(
        menu_title="Navigation",  # required
        options=["Home", "Chatbot", "Telegram"],  # required
        icons=["house", "robot", "send"],  # optional
        menu_icon="cast",  # optional
        default_index=0,  # optional
        styles={
            "container": {"padding": "0!important", "background-color": "#262730"},
            "icon": {"color": "white", "font-size": "25px"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "grey"},
            "nav-link-selected": {"background-color": "#02ab21"},
        },
    )

# Run the appropriate app based on the selected menu option
if selected == "Home":
    Home.app()
if selected == "Chatbot":
    Chatbot.app()
if selected == "Telegram":
    Telegram.app()





