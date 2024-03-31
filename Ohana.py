import os

import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai
import google.api_core.exceptions



# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Get to know Ohana",
    page_icon="🪄",  # Favicon emoji
    layout="wide",  # Page layout option
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('bert')


# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role


# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])


# Display the chatbot's title on the page
st.title("👱🏼‍♀️ Ohana : One place stop for all your queries!")

# Display the chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Input field for user's message
user_prompt = st.chat_input("Shoot Ohana with your queries...")
if user_prompt:
    try:
        # Add user's message to chat and display it
        st.chat_message("user").markdown(user_prompt)

        # Send user's message to Gemini-Pro and get the response
        gemini_response = st.session_state.chat_session.send_message(user_prompt)

        # Display Gemini-Pro's response
        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)

    except google.api_core.exceptions.InternalServerError as e:
        st.error(f"Internal Server Error: {e}")
        # Log the error for further investigation
