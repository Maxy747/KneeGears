import streamlit as st

def app():
    st.title("Telegram")
    st.write("This is the Telegram page where you can integrate Telegram functionalities.")

    # Provide a link to the Telegram chatbot
    st.write("For academic assistance, you can chat with our Telegram bot:")
    
    # Replace 'your_telegram_bot_link' with the actual link to your Telegram bot
    telegram_bot_link = "https://t.me/Max_SPA_bot"
    st.markdown(f"[Click here to chat with the Telegram bot]({telegram_bot_link})", unsafe_allow_html=True)
    
    st.write("The bot can help you with various academic tasks, including reminders, answering questions, and more.")
