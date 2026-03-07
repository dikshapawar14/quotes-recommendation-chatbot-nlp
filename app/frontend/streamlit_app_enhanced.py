"""
QUOTES RECOMMENDATION CHATBOT - Main Application
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

# ========== CSS STYLES ==========
st.markdown("""
<style>
    /* Main Header */
    .main-header {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .main-title {
        color: white;
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0;
    }
    
    .main-subtitle {
        color: #e0e7ff;
        font-size: 1.1rem;
        margin-top: 0.5rem;
    }
    
    /* Quote Cards */
    .quote-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        border-left: 6px solid #6366f1;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .quote-text {
        font-size: 1.2rem;
        font-style: italic;
        color: #1f2937;
        margin-bottom: 0.5rem;
    }
    
    .quote-author {
        text-align: right;
        font-size: 1rem;
        font-weight: 600;
        color: #6366f1;
    }
    
    .quote-category {
        display: inline-block;
        background: #6366f1;
        color: white;
        padding: 0.2rem 1rem;
        border-radius: 15px;
        font-size: 0.8rem;
        margin-right: 0.5rem;
    }
    
    /* Emotion Badges */
    .badge {
        display: inline-block;
        padding: 0.2rem 1rem;
        border-radius: 15px;
        font-size: 0.8rem;
        margin: 0.2rem;
    }
    
    .badge-positive {
        background: #d1fae5;
        color: #065f46;
        border: 1px solid #a7f3d0;
    }
    
    .badge-negative {
        background: #fee2e2;
        color: #991b1b;
        border: 1px solid #fecaca;
    }
    
    .badge-neutral {
        background: #f3f4f6;
        color: #374151;
        border: 1px solid #e5e7eb;
    }
    
    /* Sidebar Stats */
    .stat-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #6366f1;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .stat-number {
        font-size: 1.5rem;
        font-weight: bold;
        color: #6366f1;
        margin: 0;
    }
    
    .stat-label {
        color: #6b7280;
        font-size: 0.9rem;
        margin: 0;
    }
    
    /* Welcome Box */
    .welcome-box {
        background: #f5f3ff;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 2rem 0;
        border: 2px dashed #6366f1;
    }
    
    .welcome-box h3 {
        color: #1f2937;
        font-size: 1.8rem;
        margin-bottom: 0.5rem;
    }
    
    .welcome-box p {
        color: #4b5563;
        font-size: 1.1rem;
    }
    
    /* Chat Messages */
    .user-msg {
        background: #f3f4f6;
        padding: 1rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        color: #1f2937;
        border-left: 4px solid #6366f1;
    }
    
    .bot-msg {
        background: #eef2ff;
        padding: 1rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        color: #1f2937;
        border-right: 4px solid #6366f1;
    }
    
    /* Tip Section */
    .tip-container {
        background: white;
        padding: 1rem;
        border-radius: 12px;
        margin: 1rem 0;
        border: 1px solid #e5e7eb;
    }
    
    .tip-category {
        font-weight: bold;
        color: #1f2937;
        margin: 1rem 0 0.5rem 0;
        font-size: 1.1rem;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #6b7280;
        padding: 1rem;
        margin-top: 2rem;
        border-top: 1px solid #e5e7eb;
    }
</style>
""", unsafe_allow_html=True)

# ========== SAMPLE QUOTES ==========
QUOTES = [
    {"quote": "The only way to do great work is to love what you do.", "author": "Steve Jobs", "category": "Motivation", "emotion": "motivated"},
    {"quote": "Life is what happens when you're busy making other plans.", "author": "John Lennon", "category": "Life", "emotion": "reflective"},
    {"quote": "The future belongs to those who believe in the beauty of their dreams.", "author": "Eleanor Roosevelt", "category": "Dreams", "emotion": "hopeful"},
    {"quote": "Happiness is not something ready made. It comes from your own actions.", "author": "Dalai Lama", "category": "Happiness", "emotion": "happy"},
    {"quote": "The best thing to hold onto in life is each other.", "author": "Audrey Hepburn", "category": "Love", "emotion": "love"},
    {"quote": "Everything you've ever wanted is on the other side of fear.", "author": "George Addair", "category": "Courage", "emotion": "scared"},
]

# ========== EMOTION KEYWORDS ==========
EMOTION_KEYWORDS = {
    "motivated": ["motivation", "motivated", "inspire", "dream", "goal"],
    "sad": ["sad", "depressed", "unhappy", "down", "cry", "lonely"],
    "happy": ["happy", "joy", "excited", "glad", "great"],
    "love": ["love", "romance", "heart", "care"],
    "confused": ["confused", "confusing", "puzzled"],
    "grateful": ["grateful", "thankful", "appreciate"],
    "scared": ["scared", "fear", "afraid", "anxious"],
    "angry": ["angry", "mad", "frustrated", "annoyed"],
    "hopeful": ["hope", "hopeful", "optimistic"],
    "thoughtful": ["think", "thought", "wonder", "curious", "nostalgic"]
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
    <div class="main-subtitle">Find the perfect quote for every emotion</div>
</div>
""", unsafe_allow_html=True)

# ========== SIDEBAR ==========
with st.sidebar:
    st.markdown("### 📊 Statistics")
    
    st.markdown("""
    <div class="stat-card">
        <p class="stat-number">1,000+</p>
        <p class="stat-label">Quotes</p>
    </div>
    <div class="stat-card">
        <p class="stat-number">10+</p>
        <p class="stat-label">Emotions</p>
    </div>
    <div class="stat-card">
        <p class="stat-number">50+</p>
        <p class="stat-label">Authors</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🎯 Try These")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💭 I need motivation", use_container_width=True):
            st.session_state.user_input = "I need motivation"
        if st.button("💭 Feeling sad", use_container_width=True):
            st.session_state.user_input = "Feeling sad"
        if st.button("💭 I'm happy", use_container_width=True):
            st.session_state.user_input = "I'm happy"
    with col2:
        if st.button("💭 I love someone", use_container_width=True):
            st.session_state.user_input = "I love someone"
        if st.button("💭 Feeling confused", use_container_width=True):
            st.session_state.user_input = "Feeling confused"
        if st.button("💭 I'm grateful", use_container_width=True):
            st.session_state.user_input = "I'm grateful"
    
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
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.markdown(f'<div class="user-msg"><b>You:</b> {user_input}</div>', unsafe_allow_html=True)
        
        # Find matching quotes
        with st.spinner("🔍 Finding quotes..."):
            time.sleep(0.5)
            
            # Detect emotion
            detected = "general"
            user_lower = user_input.lower()
            for emotion, words in EMOTION_KEYWORDS.items():
                if any(word in user_lower for word in words):
                    detected = emotion
                    break
            
            # Get matching quotes
            matches = [q for q in QUOTES if q['emotion'] == detected]
            if not matches:
                matches = random.sample(QUOTES, 2)
            else:
                matches = matches[:2]
            
            # Display quotes
            for q in matches:
                if q['emotion'] in ['happy', 'motivated', 'hopeful', 'grateful', 'love']:
                    badge = "badge-positive"
                elif q['emotion'] in ['sad', 'scared', 'angry']:
                    badge = "badge-negative"
                else:
                    badge = "badge-neutral"
                
                st.markdown(f"""
                <div class="quote-card">
                    <div class="quote-text">"{q['quote']}"</div>
                    <div class="quote-author">— {q['author']}</div>
                    <div style="margin-top:0.8rem">
                        <span class="quote-category">{q['category']}</span>
                        <span class="badge {badge}">🎭 {q['emotion']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.session_state.messages.append({"role": "assistant", "content": f"Found {len(matches)} quotes for you"})

with col_tips:
    st.markdown("### 💫 Quick Tips")
    
    # POSITIVE SECTION - Working Buttons
    st.markdown("**😊 Positive**")
    pos_cols = st.columns(5)
    pos_words = ["happy", "grateful", "excited", "proud", "hopeful"]
    for i, word in enumerate(pos_words):
        with pos_cols[i]:
            if st.button(word, key=f"pos_{word}", use_container_width=True):
                st.session_state.user_input = f"I'm {word}"
    
    # NEGATIVE SECTION - Working Buttons
    st.markdown("**😔 Negative**")
    neg_cols = st.columns(5)
    neg_words = ["sad", "lonely", "angry", "scared", "hurt"]
    for i, word in enumerate(neg_words):
        with neg_cols[i]:
            if st.button(word, key=f"neg_{word}", use_container_width=True):
                st.session_state.user_input = f"Feeling {word}"
    
    # REFLECTIVE SECTION - Working Buttons
    st.markdown("**💭 Reflective**")
    ref_cols = st.columns(4)
    ref_words = ["thoughtful", "curious", "nostalgic", "confused"]
    for i, word in enumerate(ref_words):
        with ref_cols[i]:
            if st.button(word, key=f"ref_{word}", use_container_width=True):
                st.session_state.user_input = f"Feeling {word}"
    
    # LOVE SECTION - Working Buttons
    st.markdown("**❤️ Love**")
    love_cols = st.columns(3)
    love_words = ["love", "care", "romance"]
    for i, word in enumerate(love_words):
        with love_cols[i]:
            if st.button(word, key=f"love_{word}", use_container_width=True):
                st.session_state.user_input = f"I need {word}"
    
    st.markdown("---")
    st.markdown("**✨ Quick Actions:**")
    
    # QUICK ACTIONS - Working Buttons
    act_col1, act_col2 = st.columns(2)
    with act_col1:
        if st.button("😊 Happy", key="act_happy", use_container_width=True):
            st.session_state.user_input = "I'm happy"
        if st.button("😔 Sad", key="act_sad", use_container_width=True):
            st.session_state.user_input = "Feeling sad"
        if st.button("💭 Curious", key="act_curious", use_container_width=True):
            st.session_state.user_input = "I'm curious"
    with act_col2:
        if st.button("❤️ Love", key="act_love", use_container_width=True):
            st.session_state.user_input = "I need love"
        if st.button("😤 Angry", key="act_angry", use_container_width=True):
            st.session_state.user_input = "Feeling angry"
        if st.button("🙏 Grateful", key="act_grateful", use_container_width=True):
            st.session_state.user_input = "I'm grateful"

# ========== FOOTER ==========
st.markdown("""
<div class="footer">
    💫 QUOTES RECOMMENDATION CHATBOT | Made with ❤️ using NLP
</div>
""", unsafe_allow_html=True)