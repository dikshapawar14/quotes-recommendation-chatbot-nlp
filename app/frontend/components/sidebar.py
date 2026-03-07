"""
Sidebar Component - App sidebar ke liye
"""

import streamlit as st

class Sidebar:
    """Sidebar manage karne ka class"""
    
    def __init__(self, recommender=None):
        self.recommender = recommender
    
    def render(self):
        """Sidebar render karo"""
        with st.sidebar:
            self.render_header()
            self.render_about()
            self.render_how_to_use()
            self.render_stats()
            self.render_buttons()
            self.render_categories()
    
    def render_header(self):
        """Header section"""
        st.markdown("## 🌟 Quote Bot")
        st.markdown("---")
    
    def render_about(self):
        """About section"""
        st.markdown("### 📖 About")
        st.markdown("""
        This chatbot uses **NLP** to understand your emotions 
        and recommend the perfect quotes.
        """)
    
    def render_how_to_use(self):
        """How to use section"""
        st.markdown("### 🎯 How to Use")
        st.markdown("""
        1. Type how you're feeling
        2. Get personalized quotes
        3. Find inspiration!
        """)
    
    def render_stats(self):
        """Statistics section"""
        st.markdown("### 📊 Statistics")
        
        if self.recommender and self.recommender.embedder.quotes_df is not None:
            df = self.recommender.embedder.quotes_df
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Quotes", len(df))
            with col2:
                if 'category' in df.columns:
                    st.metric("Categories", df['category'].nunique())
            
            if 'author' in df.columns:
                st.metric("Unique Authors", df['author'].nunique())
        else:
            st.info("Load data to see stats")
    
    def render_buttons(self):
        """Action buttons"""
        st.markdown("### 🎮 Actions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔄 Reset Chat", use_container_width=True):
                st.session_state.messages = []
                st.rerun()
        
        with col2:
            if st.button("💫 Quote of Day", use_container_width=True):
                st.session_state.show_qotd = True
                st.rerun()
    
    def render_categories(self):
        """Categories list"""
        st.markdown("### 🏷️ Categories")
        
        if self.recommender and self.recommender.embedder.quotes_df is not None:
            df = self.recommender.embedder.quotes_df
            
            if 'category' in df.columns:
                categories = df['category'].value_counts().head(8)
                
                for cat, count in categories.items():
                    st.markdown(f"- **{cat}**: {count}")
            else:
                st.info("No categories found")
        else:
            st.info("Load data to see categories")