"""
Quote Display Component
"""

import streamlit as st

class QuoteDisplay:
    def __init__(self):
        self.setup_css()
    
    def setup_css(self):
        """CSS styles setup karo"""
        st.markdown("""
        <style>
        .quote-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1.5rem;
            border-radius: 10px;
            margin: 1rem 0;
            color: white;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .quote-text {
            font-size: 1.2rem;
            font-style: italic;
            margin-bottom: 0.5rem;
            line-height: 1.6;
        }
        .quote-author {
            text-align: right;
            font-weight: bold;
            font-size: 1rem;
        }
        .quote-category {
            display: inline-block;
            background: rgba(255, 255, 255, 0.2);
            padding: 0.2rem 1rem;
            border-radius: 15px;
            font-size: 0.8rem;
            margin-top: 0.5rem;
        }
        .quote-match {
            font-size: 0.8rem;
            opacity: 0.9;
        }
        </style>
        """, unsafe_allow_html=True)
    
    def display_single_quote(self, quote_data):
        """Ek quote display karo"""
        quote = quote_data.get('quote', 'No quote available')
        author = quote_data.get('author', 'Unknown')
        category = quote_data.get('category', 'General')
        similarity = quote_data.get('similarity', 0)
        
        # Similarity ko percentage mein convert karo
        match_percent = int(similarity * 100) if similarity else 0
        
        html = f"""
        <div class="quote-card">
            <div class="quote-text">"{quote}"</div>
            <div class="quote-author">— {author}</div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 0.5rem;">
                <span class="quote-category">#{category}</span>
                <span class="quote-match">Match: {match_percent}%</span>
            </div>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)
    
    def display_multiple_quotes(self, quotes_list):
        """Multiple quotes display karo"""
        if not quotes_list:
            st.warning("😔 No quotes found. Try a different message!")
            return
        
        st.markdown(f"### Found {len(quotes_list)} quotes for you:")
        for quote in quotes_list:
            self.display_single_quote(quote)
    
    def display_quote_of_the_day(self, quote_data):
        """Quote of the day display karo"""
        if not quote_data:
            st.info("No quote of the day available")
            return
        
        st.markdown("### 🌟 Quote of the Day")
        self.display_single_quote(quote_data)
    
    def display_error(self, message):
        """Error message display karo"""
        st.error(f"❌ {message}")
    
    def display_success(self, message):
        """Success message display karo"""
        st.success(f"✅ {message}")
    
    def display_info(self, message):
        """Info message display karo"""
        st.info(f"ℹ️ {message}")