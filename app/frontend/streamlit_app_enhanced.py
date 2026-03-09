"""
QUOTES RECOMMENDATION CHATBOT - DARK MODE
Black Background, White Text, Purple Highlights
"""

import sys
import os
import random
import time

# Add project root to path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, project_root)

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="QUOTES RECOMMENDATION CHATBOT",
    page_icon="💫",
    layout="wide"
)

# ========== DARK MODE CSS - Black Background, White Text ==========
st.markdown("""
<style>
    /* Global Dark Mode */
    .stApp {
        background-color: #0A0A0A !important;
    }
    
    /* All text white by default */
    * {
        color: #FFFFFF !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }
    
    /* Headers with Purple */
    h1, h2, h3, h4, h5, h6 {
        color: #C084FC !important;
    }
    
    /* Main Header - Dark Purple Gradient */
    .main-header {
        background: linear-gradient(135deg, #2E1065 0%, #581C87 100%);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(139, 92, 246, 0.3);
        border: 1px solid #6B21A5;
    }
    
    .main-title {
        color: #FFFFFF !important;
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0;
        text-shadow: 0 0 10px rgba(192, 132, 252, 0.5);
    }
    
    .main-subtitle {
        color: #D8B4FE !important;
        font-size: 1.1rem;
        margin-top: 0.5rem;
    }
    
    /* Sidebar - Dark Background */
    section[data-testid="stSidebar"] {
        background-color: #111111 !important;
        border-right: 1px solid #2D2D2D;
    }
    
    /* Stats Cards - Dark Purple */
    .stat-card {
        background: linear-gradient(135deg, #1E1E1E 0%, #2A1E3A 100%) !important;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #A855F7;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        transition: all 0.3s ease;
    }
    
    .stat-card:hover {
        background: linear-gradient(135deg, #2A1E3A 0%, #3B2A5A 100%) !important;
        transform: translateX(5px);
        border-left: 4px solid #E879F9;
    }
    
    .stat-number {
        font-size: 1.5rem;
        font-weight: bold;
        color: #E879F9 !important;
        margin: 0;
    }
    
    .stat-label {
        color: #D1D5DB !important;
        font-size: 0.9rem;
        margin: 0;
    }
    
    /* Try These Section - Dark */
    .try-these-section {
        background-color: #111111 !important;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 1px solid #2D2D2D;
    }
    
    /* Buttons - Dark Purple */
    .stButton > button {
        background: linear-gradient(135deg, #2D1B40 0%, #1E1E1E 100%) !important;
        border: 1px solid #6B21A5 !important;
        border-radius: 25px !important;
        color: #FFFFFF !important;
        font-weight: 500 !important;
        padding: 0.5rem 1rem !important;
        transition: all 0.2s ease !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #6B21A5 0%, #8B5CF6 100%) !important;
        border-color: #C084FC !important;
        color: #FFFFFF !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4);
    }
    
    /* Category Titles - Purple */
    .category-title {
        color: #E879F9 !important;
        font-size: 1.3rem !important;
        font-weight: bold !important;
        margin: 1.5rem 0 0.5rem 0 !important;
        padding-bottom: 0.3rem !important;
        border-bottom: 3px solid #A855F7 !important;
        display: inline-block !important;
    }
    
    /* Word Chips - Dark Purple */
    .word-chip {
        display: inline-block !important;
        background: linear-gradient(135deg, #2A1E3A 0%, #1E1E1E 100%) !important;
        border: 1px solid #6B21A5 !important;
        border-radius: 30px !important;
        padding: 8px 18px !important;
        margin: 0 8px 8px 0 !important;
        color: #FFFFFF !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
        cursor: default !important;
    }
    
    .word-chip:hover {
        background: linear-gradient(135deg, #8B5CF6 0%, #6B21A5 100%) !important;
        border-color: #E879F9 !important;
        color: #FFFFFF !important;
        transform: scale(1.05);
        box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4);
    }
    
    /* Welcome Box - Dark */
    .welcome-box {
        background: linear-gradient(135deg, #111111 0%, #1A0B2E 100%) !important;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 2rem 0;
        border: 2px dashed #8B5CF6;
        box-shadow: 0 4px 20px rgba(139, 92, 246, 0.2);
    }
    
    .welcome-box h3 {
        color: #E879F9 !important;
        font-size: 1.8rem;
    }
    
    .welcome-box p {
        color: #D1D5DB !important;
    }
    
    /* Quote Cards - Dark Purple */
    .quote-card {
        background: linear-gradient(135deg, #1A0B2E 0%, #111111 100%) !important;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 6px solid #8B5CF6;
        box-shadow: 0 4px 15px rgba(139, 92, 246, 0.2);
        transition: all 0.3s ease;
    }
    
    .quote-card:hover {
        background: linear-gradient(135deg, #2A1E3A 0%, #1A0B2E 100%) !important;
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(139, 92, 246, 0.4);
        border-left: 6px solid #E879F9;
    }
    
    .quote-text {
        color: #FFFFFF !important;
        font-size: 1.2rem;
        font-style: italic;
        margin-bottom: 0.5rem;
    }
    
    .quote-author {
        color: #E879F9 !important;
        text-align: right;
        font-weight: bold;
    }
    
    /* Chat Messages - Dark */
    .user-msg {
        background: linear-gradient(135deg, #1A0B2E 0%, #111111 100%) !important;
        padding: 1rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        color: #FFFFFF !important;
        border-right: 4px solid #8B5CF6;
    }
    
    .bot-msg {
        background: linear-gradient(135deg, #111111 0%, #1A0B2E 100%) !important;
        padding: 1rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        color: #FFFFFF !important;
        border-left: 4px solid #8B5CF6;
    }
    
    /* Input field - Dark */
    .stTextInput > div > div > input {
        background-color: #1E1E1E !important;
        color: #FFFFFF !important;
        border: 1px solid #6B21A5 !important;
        border-radius: 25px !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #E879F9 !important;
        box-shadow: 0 0 10px rgba(139, 92, 246, 0.3);
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #9CA3AF !important;
        padding: 1rem;
        margin-top: 2rem;
        border-top: 1px solid #2D2D2D;
    }
    
    /* Tips Container - Dark */
    .tips-container {
        background-color: #111111 !important;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #2D2D2D;
    }
    
    /* Scrollbar - Dark */
    ::-webkit-scrollbar {
        width: 10px;
        background: #1E1E1E;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #6B21A5;
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #8B5CF6;
    }
</style>
""", unsafe_allow_html=True)

# ========== SAMPLE QUOTES ==========
QUOTES = [
    {"quote": "The only way to do great work is to love what you do.", "author": "Steve Jobs", "emotion": "motivated"},
    {"quote": "Life is what happens when you're busy making other plans.", "author": "John Lennon", "emotion": "reflective"},
    {"quote": "Happiness is not something ready made. It comes from your own actions.", "author": "Dalai Lama", "emotion": "happy"},
    {"quote": "The best thing to hold onto in life is each other.", "author": "Audrey Hepburn", "emotion": "love"},
    {"quote": "Everything you've ever wanted is on the other side of fear.", "author": "George Addair", "emotion": "scared"},
]

# ========== EMOTION KEYWORDS ==========
EMOTION_KEYWORDS = {
    "motivated": ["motivation", "motivated", "inspire", "dream"],
    "sad": ["sad", "depressed", "unhappy", "down"],
    "happy": ["happy", "joy", "excited", "glad"],
    "love": ["love", "romance", "heart", "care"],
    "scared": ["scared", "fear", "afraid", "anxious"],
    "grateful": ["grateful", "thankful", "appreciate"],
}

# ========== SESSION STATE ==========
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'user_input' not in st.session_state:
    st.session_state.user_input = None

# ========== HEADER ==========
st.markdown("""
<div class="main-header">
    <div class="main-title">💫 QUOTES RECOMMENDATION CHATBOT</div>
    <div class="main-subtitle">Find the perfect quote for your mood</div>
</div>
""", unsafe_allow_html=True)

# ========== SIDEBAR ==========
with st.sidebar:
    st.markdown("### 📊 Statistics")
    
    st.markdown("""
    <div class="stat-card">
        <p class="stat-number">500K+</p>
        <p class="stat-label">Quotes</p>
    </div>
    <div class="stat-card">
        <p class="stat-number">27+</p>
        <p class="stat-label">Emotions</p>
    </div>
    <div class="stat-card">
        <p class="stat-number">50+</p>
        <p class="stat-label">Authors</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Try These Section
    st.markdown('<div class="try-these-section">', unsafe_allow_html=True)
    st.markdown("### 🎯 Try These")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔥 Need Motivation", use_container_width=True):
            st.session_state.user_input = "I need motivation"
        if st.button("😢 Feeling Sad", use_container_width=True):
            st.session_state.user_input = "Feeling sad"
        if st.button("😊 I'm Happy", use_container_width=True):
            st.session_state.user_input = "I'm happy"
    with col2:
        if st.button("❤️ In Love", use_container_width=True):
            st.session_state.user_input = "I love someone"
        if st.button("😨 Feeling Scared", use_container_width=True):
            st.session_state.user_input = "Feeling scared"
        if st.button("🙏 Grateful", use_container_width=True):
            st.session_state.user_input = "I'm grateful"
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ========== MAIN CONTENT ==========
col_main, col_tips = st.columns([2, 1])

with col_main:
    # Welcome message
    if not st.session_state.messages:
        st.markdown("""
        <div class="welcome-box">
            <h3>🌟 Hello! How are you feeling today?</h3>
            <p>Tell me your emotions, and I'll find the perfect quote for you.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Chat history
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f'<div class="user-msg"><b>You:</b> {msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bot-msg">{msg["content"]}</div>', unsafe_allow_html=True)
    
    # User input
    if st.session_state.user_input:
        user_input = st.session_state.user_input
        st.session_state.user_input = None
    else:
        user_input = st.chat_input("How are you feeling today?")
    
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.markdown(f'<div class="user-msg"><b>You:</b> {user_input}</div>', unsafe_allow_html=True)
        
        with st.spinner("🔍 Finding quotes..."):
            time.sleep(0.5)
            
            detected = "motivated"
            user_lower = user_input.lower()
            for emotion, words in EMOTION_KEYWORDS.items():
                if any(word in user_lower for word in words):
                    detected = emotion
                    break
            
            matches = [q for q in QUOTES if q['emotion'] == detected]
            if not matches:
                matches = random.sample(QUOTES, 1)
            else:
                matches = matches[:1]
            
            for q in matches:
                st.markdown(f"""
                <div class="quote-card">
                    <div class="quote-text">"{q['quote']}"</div>
                    <div class="quote-author">— {q['author']}</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.session_state.messages.append({"role": "assistant", "content": "Here's a quote for you!"})

with col_tips:
    st.markdown('<div class="tips-container">', unsafe_allow_html=True)
    st.markdown("### 💫 Quick Tips")
    
    # POSITIVE
    st.markdown("""
    <div class="category-title">😊 POSITIVE</div>
    <div style="margin: 10px 0 20px 0;">
        <span class="word-chip">happy</span>
        <span class="word-chip">grateful</span>
        <span class="word-chip">excited</span>
        <span class="word-chip">proud</span>
        <span class="word-chip">hopeful</span>
    </div>
    """, unsafe_allow_html=True)
    
    # NEGATIVE
    st.markdown("""
    <div class="category-title">😔 NEGATIVE</div>
    <div style="margin: 10px 0 20px 0;">
        <span class="word-chip">sad</span>
        <span class="word-chip">lonely</span>
        <span class="word-chip">angry</span>
        <span class="word-chip">scared</span>
        <span class="word-chip">hurt</span>
    </div>
    """, unsafe_allow_html=True)
    
    # REFLECTIVE
    st.markdown("""
    <div class="category-title">💭 REFLECTIVE</div>
    <div style="margin: 10px 0 20px 0;">
        <span class="word-chip">thoughtful</span>
        <span class="word-chip">curious</span>
        <span class="word-chip">nostalgic</span>
        <span class="word-chip">confused</span>
    </div>
    """, unsafe_allow_html=True)
    
    # LOVE
    st.markdown("""
    <div class="category-title">❤️ LOVE</div>
    <div style="margin: 10px 0 20px 0;">
        <span class="word-chip">love</span>
        <span class="word-chip">care</span>
        <span class="word-chip">romance</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ========== FOOTER ==========
st.markdown("""
<div class="footer">
    💫 QUOTES RECOMMENDATION CHATBOT | Made with ❤️ | Dark Mode
</div>
""", unsafe_allow_html=True)