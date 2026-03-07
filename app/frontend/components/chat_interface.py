"""
Chat Interface Component
"""

import streamlit as st

class ChatInterface:
    def __init__(self):
        if 'messages' not in st.session_state:
            st.session_state.messages = []
    
    def display_chat_history(self):
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
    
    def get_user_input(self):
        return st.chat_input("How are you feeling today?")
    
    def add_message(self, role, content, quote_data=None):
        st.session_state.messages.append({
            "role": role,
            "content": content,
            "quote_data": quote_data
        })
    
    def clear_chat(self):
        st.session_state.messages = []
        st.rerun()