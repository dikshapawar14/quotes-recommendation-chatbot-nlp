"""
Streamlit Chatbot App
"""

import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.recommender import QuoteRecommender
import random

# Page config
st.set_page_config(
    page_title="Quote Recommendation Chatbot",
    page_icon="💭",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .quote-box {
        background: #f3f4f6;
        padding: 2rem;
        border-radius: 10px;
        border-left: 5px solid #667eea;
        margin: 1rem 0;
        font-size: 1.2rem;
        font-style: italic;
    }
    .author {
        text-align: right;
        color: #666;
        font-weight: bold;
    }
    .emotion-tag {
        display: inline-block;
        padding: 0.2rem 1rem;
        background: #e0e7ff;
        color: #4338ca;
        border-radius: 15px;
        font-size: 0.8rem;
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize recommender (cached)
@st.cache_resource
def load_recommender():
    return QuoteRecommender()

# Session state initialization
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'recommender' not in st.session_state:
    st.session_state.recommender = load_recommender()

# Header
st.markdown("<div class='main-header'><h1>💭 Quote Recommendation Chatbot</h1><p>Tell me how you feel, I'll find the perfect quote for you!</p></div>", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## 🌟 About")
    st.markdown("This chatbot uses NLP to understand your emotions and recommend matching quotes.")
    
    st.markdown("## 🎯 How to use")
    st.markdown("1. Type how you're feeling")
    st.markdown("2. Get personalized quotes")
    st.markdown("3. Find inspiration!")
    
    st.markdown("## 📊 Stats")
    if st.session_state.recommender.embedder.quotes_df is not None:
        total_quotes = len(st.session_state.recommender.embedder.quotes_df)
        categories = st.session_state.recommender.embedder.quotes_df['category'].nunique()
        st.metric("Total Quotes", total_quotes)
        st.metric("Categories", categories)
    
    if st.button("🔄 Reset Chat"):
        st.session_state.messages = []
        st.rerun()
    
    if st.button("💫 Quote of the Day"):
        quote = st.session_state.recommender.get_quote_of_the_day()
        if quote:
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"**Quote of the Day**\n\n> {quote['quote']}\n\n— *{quote['author']}*",
                "quote_data": quote
            })
            st.rerun()

# Main chat area
col1, col2 = st.columns([2, 1])

with col1:
    # Chat messages
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                if "quote_data" in message:
                    st.markdown(f"<div class='emotion-tag'>#{message['quote_data'].get('category', 'General')}</div>", unsafe_allow_html=True)
    
    # User input
    if prompt := st.chat_input("How are you feeling today?"):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get recommendations
        with st.chat_message("assistant"):
            with st.spinner("Finding the perfect quote for you..."):
                results = st.session_state.recommender.recommend_by_emotion(prompt, k=3)
                
                if results:
                    response = "Here are some quotes for you:\n\n"
                    for i, r in enumerate(results):
                        response += f"**Quote {i+1}**\n"
                        response += f"> {r['quote']}\n"
                        response += f"\n— *{r['author']}*\n"
                        response += f"<div class='emotion-tag'>#{r['category']}</div>\n\n"
                    
                    st.markdown(response, unsafe_allow_html=True)
                    
                    # Store in session
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response,
                        "quote_data": results[0]
                    })
                else:
                    st.markdown("Sorry, I couldn't find any quotes matching your mood. Try rephrasing!")
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": "Sorry, I couldn't find any quotes matching your mood. Try rephrasing!"
                    })

with col2:
    st.markdown("### 💡 Tips")
    st.info(
        """
        **Try saying:**
        - "I'm feeling sad today"
        - "I need motivation"
        - "I'm so happy!"
        - "Feeling lonely"
        - "I love someone"
        - "Need success tips"
        """
    )
    
    st.markdown("### 🎨 Categories")
    if st.session_state.recommender.embedder.quotes_df is not None:
        categories = st.session_state.recommender.embedder.quotes_df['category'].value_counts()
        for cat, count in categories.head(5).items():
            st.markdown(f"- **{cat}**: {count} quotes")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #666;'>Made with ❤️ using NLP and Sentence Transformers</p>", unsafe_allow_html=True)