import streamlit as st
import requests

st.title("Medical Assistant Chatbot 💬")

# Backend API URL
API_URL = "http://localhost:8000/chat/chat"

# Chat input
user_input = st.text_input("You:", "")

if st.button("Send") and user_input.strip():
    with st.spinner("Thinking..."):
        try:
            response = requests.post(API_URL, json={"message": user_input})
            if response.status_code == 200:
                st.markdown("**Assistant:**")
                st.success(response.json().get("response", "No response"))
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"Failed to connect to backend: {e}")