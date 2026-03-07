"""
User Features Module - User interaction patterns se features nikalne ke liye
"""

import numpy as np
from collections import defaultdict, Counter
import time

class UserFeatureExtractor:
    """User behavior aur preferences track karne ka class"""
    
    def __init__(self):
        # User session data store karne ke liye
        self.user_sessions = defaultdict(lambda: {
            'queries': [],
            'selected_quotes': [],
            'categories_viewed': [],
            'session_start': time.time(),
            'total_interactions': 0
        })
    
    def update_user_session(self, user_id, query=None, selected_quote=None):
        """User session update karo"""
        session = self.user_sessions[user_id]
        
        if query:
            session['queries'].append({
                'text': query,
                'timestamp': time.time()
            })
        
        if selected_quote:
            session['selected_quotes'].append({
                'quote': selected_quote.get('quote', ''),
                'category': selected_quote.get('category', ''),
                'author': selected_quote.get('author', ''),
                'timestamp': time.time()
            })
            
            if 'category' in selected_quote:
                session['categories_viewed'].append(selected_quote['category'])
        
        session['total_interactions'] += 1
    
    def extract_session_features(self, user_id):
        """Current session se features"""
        session = self.user_sessions.get(user_id, {})
        
        if not session:
            return {}
        
        session_duration = time.time() - session.get('session_start', time.time())
        queries = session.get('queries', [])
        selected = session.get('selected_quotes', [])
        categories = session.get('categories_viewed', [])
        
        features = {
            'session_duration': session_duration,
            'total_queries': len(queries),
            'total_selections': len(selected),
            'interaction_rate': len(selected) / max(len(queries), 1),
            'unique_categories': len(set(categories)),
            'avg_time_between_queries': self._avg_time_between(queries)
        }
        
        # Category preferences
        if categories:
            category_counts = Counter(categories)
            most_common = category_counts.most_common(1)
            if most_common:
                features['preferred_category'] = most_common[0][0]
                features['category_preference_score'] = most_common[0][1] / len(categories)
        
        return features
    
    def _avg_time_between(self, items):
        """Average time between interactions"""
        if len(items) < 2:
            return 0
        
        timestamps = [item['timestamp'] for item in items]
        diffs = [timestamps[i+1] - timestamps[i] for i in range(len(timestamps)-1)]
        return np.mean(diffs) if diffs else 0
    
    def extract_query_features(self, query):
        """User query se features"""
        if not query:
            return {}
        
        words = query.lower().split()
        
        features = {
            'query_length': len(query),
            'query_word_count': len(words),
            'query_has_question': '?' in query,
            'query_has_exclamation': '!' in query,
            'query_is_short': len(words) < 5,
            'query_is_long': len(words) > 15
        }
        
        # Detect query type
        question_words = ['what', 'why', 'how', 'when', 'where', 'who']
        features['query_is_question'] = any(
            query.lower().startswith(qw) for qw in question_words
        )
        
        # Emotion indicators in query
        emotion_words = {
            'sad': ['sad', 'depressed', 'unhappy', 'down'],
            'happy': ['happy', 'glad', 'joy', 'excited'],
            'angry': ['angry', 'mad', 'frustrated'],
            'love': ['love', 'romance', 'heart']
        }
        
        for emotion, words_list in emotion_words.items():
            features[f'query_emotion_{emotion}'] = any(
                w in words_list for w in words
            )
        
        return features
    
    def extract_preference_features(self, user_id):
        """User preferences based on history"""
        session = self.user_sessions.get(user_id, {})
        selected = session.get('selected_quotes', [])
        
        if not selected:
            return {}
        
        # Author preferences
        authors = [q['author'] for q in selected if q.get('author')]
        if authors:
            author_counts = Counter(authors)
            top_author = author_counts.most_common(1)[0]
            features = {
                'preferred_author': top_author[0],
                'author_preference_score': top_author[1] / len(selected)
            }
        else:
            features = {}
        
        # Category consistency
        categories = [q['category'] for q in selected if q.get('category')]
        if categories:
            category_counts = Counter(categories)
            features['category_consistency'] = max(category_counts.values()) / len(categories)
        
        return features
    
    def extract_all_features(self, user_id, query=None, selected_quote=None):
        """Sabhi user features ek saath"""
        # Update session first
        if query or selected_quote:
            self.update_user_session(user_id, query, selected_quote)
        
        features = {}
        
        # Session features
        features.update(self.extract_session_features(user_id))
        
        # Query features
        if query:
            features.update(self.extract_query_features(query))
        
        # Preference features
        features.update(self.extract_preference_features(user_id))
        
        # Add prefix
        features = {f'user_{k}': v for k, v in features.items()}
        
        return features
    
    def clear_session(self, user_id):
        """User session clear karo"""
        if user_id in self.user_sessions:
            del self.user_sessions[user_id]

if __name__ == "__main__":
    extractor = UserFeatureExtractor()
    
    # Simulate user interaction
    user_id = "test_user_1"
    
    # Query 1
    features1 = extractor.extract_all_features(
        user_id, 
        query="I need motivation today"
    )
    print("After query 1:", features1)
    
    # Select a quote
    quote = {
        'quote': 'Stay hungry, stay foolish',
        'author': 'Steve Jobs',
        'category': 'Motivation'
    }
    features2 = extractor.extract_all_features(
        user_id,
        selected_quote=quote
    )
    print("\nAfter selection:", features2)
    
    # Query 2
    features3 = extractor.extract_all_features(
        user_id,
        query="Any love quotes?"
    )
    print("\nAfter query 2:", features3)