"""
Enhanced Quote Recommender Module
"""

import numpy as np
import random
from src.features.embeddings import QuoteEmbeddings
from src.features.faiss_index import FaissIndex
from src.nlp.preprocessing.cleaner import TextCleaner

class EnhancedQuoteRecommender:
    def __init__(self, embeddings_dir='data/embeddings/'):
        print("Initializing Enhanced Quote Recommender...")
        
        self.cleaner = TextCleaner()
        self.embedder = QuoteEmbeddings()
        self.faiss_index = FaissIndex()
        
        if self.embedder.load_embeddings(embeddings_dir):
            self.faiss_index.load_index(embeddings_dir)
            self.faiss_index.quotes_df = self.embedder.quotes_df
            print("Enhanced Recommender ready!")
        else:
            print("No embeddings found. Please run embeddings.py first")
    
    def recommend(self, user_message, k=5):
        cleaned = self.cleaner.clean_pipeline(user_message)
        embedding = self.embedder.get_embedding(cleaned)
        results = self.faiss_index.search(embedding, k=k)
        return results if results else []
    
    def recommend_by_emotion(self, user_message, k=5):
        emotion_keywords = {
            'sad': ['sad', 'depressed', 'unhappy', 'down', 'grief'],
            'happy': ['happy', 'joy', 'excited', 'glad', 'cheerful'],
            'angry': ['angry', 'mad', 'frustrated', 'annoyed'],
            'love': ['love', 'romance', 'heart', 'adore'],
            'motivated': ['motivation', 'inspire', 'dream', 'goal'],
            'scared': ['scared', 'fear', 'afraid', 'anxious'],
            'lonely': ['lonely', 'alone', 'isolated'],
            'grateful': ['grateful', 'thankful', 'appreciate'],
            'confused': ['confused', 'confusing', 'puzzled'],
            'proud': ['proud', 'accomplished', 'achievement']
        }
        
        detected = 'general'
        msg_lower = user_message.lower()
        
        for emotion, keywords in emotion_keywords.items():
            if any(k in msg_lower for k in keywords):
                detected = emotion
                break
        
        results = self.recommend(user_message, k=k*2)
        
        for r in results[:k]:
            r['detected_emotion'] = detected
        
        return results[:k]
    
    def get_quote_of_the_day(self):
        if self.embedder.quotes_df is not None and len(self.embedder.quotes_df) > 0:
            idx = random.randint(0, len(self.embedder.quotes_df)-1)
            return self.embedder.quotes_df.iloc[idx].to_dict()
        return None
    
    def get_emotion_stats(self):
        return {
            'total_emotions': 10,
            'quotes_available': len(self.embedder.quotes_df) if self.embedder.quotes_df is not None else 0
        }