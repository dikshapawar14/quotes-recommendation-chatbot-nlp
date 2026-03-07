"""
Text Features Module - Text se linguistic features nikalne ke liye
"""

import re
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from collections import Counter
import string

class TextFeatureExtractor:
    """Text se linguistic features extract karne ka class"""
    
    def __init__(self):
        # Download NLTK data if needed
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
            nltk.download('stopwords')
        
        self.stop_words = set(stopwords.words('english'))
    
    def extract_basic_features(self, text):
        """Basic text features - length, word count, etc."""
        if not isinstance(text, str):
            text = str(text)
        
        words = word_tokenize(text)
        sentences = sent_tokenize(text)
        
        features = {
            'char_count': len(text),
            'word_count': len(words),
            'sentence_count': len(sentences),
            'avg_word_length': sum(len(w) for w in words) / max(len(words), 1),
            'avg_sentence_length': len(words) / max(len(sentences), 1),
        }
        
        return features
    
    def extract_lexical_features(self, text):
        """Lexical features - unique words, vocabulary richness"""
        words = word_tokenize(text.lower())
        words = [w for w in words if w.isalpha()]  # Only alphabetic
        
        unique_words = set(words)
        
        features = {
            'unique_word_count': len(unique_words),
            'lexical_diversity': len(unique_words) / max(len(words), 1),
            'stopword_count': sum(1 for w in words if w in self.stop_words),
            'stopword_ratio': sum(1 for w in words if w in self.stop_words) / max(len(words), 1),
        }
        
        return features
    
    def extract_pos_features(self, text):
        """Part-of-speech features (simplified)"""
        words = word_tokenize(text)
        
        # Simple POS detection based on suffixes
        pos_counts = {
            'noun': 0,
            'verb': 0,
            'adjective': 0,
            'adverb': 0,
            'other': 0
        }
        
        noun_suffixes = ['tion', 'ness', 'ity', 'ment', 'ance', 'ence', 'ship']
        verb_suffixes = ['ate', 'ize', 'ify', 'en', 'ing', 'ed']
        adj_suffixes = ['ous', 'ive', 'ful', 'less', 'able', 'ic', 'al']
        adv_suffixes = ['ly']
        
        for word in words:
            word_lower = word.lower()
            if any(word_lower.endswith(suf) for suf in noun_suffixes):
                pos_counts['noun'] += 1
            elif any(word_lower.endswith(suf) for suf in verb_suffixes):
                pos_counts['verb'] += 1
            elif any(word_lower.endswith(suf) for suf in adj_suffixes):
                pos_counts['adjective'] += 1
            elif any(word_lower.endswith(suf) for suf in adv_suffixes):
                pos_counts['adverb'] += 1
            else:
                pos_counts['other'] += 1
        
        # Normalize
        total = sum(pos_counts.values())
        if total > 0:
            for key in pos_counts:
                pos_counts[key] /= total
        
        return pos_counts
    
    def extract_sentiment_features(self, text):
        """Basic sentiment features"""
        words = word_tokenize(text.lower())
        
        # Simple positive/negative word lists
        positive_words = {'good', 'great', 'excellent', 'amazing', 'wonderful', 
                         'beautiful', 'happy', 'love', 'best', 'awesome'}
        negative_words = {'bad', 'terrible', 'awful', 'horrible', 'sad', 
                         'hate', 'worst', 'poor', 'ugly', 'angry'}
        
        pos_count = sum(1 for w in words if w in positive_words)
        neg_count = sum(1 for w in words if w in negative_words)
        
        features = {
            'positive_word_count': pos_count,
            'negative_word_count': neg_count,
            'sentiment_score': (pos_count - neg_count) / max(len(words), 1)
        }
        
        return features
    
    def extract_all_features(self, text):
        """Sabhi features ek saath extract karo"""
        features = {}
        
        # Combine all features
        features.update(self.extract_basic_features(text))
        features.update(self.extract_lexical_features(text))
        features.update(self.extract_pos_features(text))
        features.update(self.extract_sentiment_features(text))
        
        return features
    
    def process_quotes_dataframe(self, df, text_column='quote'):
        """Dataframe ke saare quotes ke features extract karo"""
        print("🔄 Extracting text features from quotes...")
        
        all_features = []
        for idx, row in df.iterrows():
            text = row.get(text_column, '')
            features = self.extract_all_features(str(text))
            all_features.append(features)
        
        # Convert to dataframe
        features_df = pd.DataFrame(all_features)
        
        # Add prefix to column names
        features_df = features_df.add_prefix('text_')
        
        print(f"✅ Extracted {len(features_df.columns)} text features")
        return features_df

if __name__ == "__main__":
    import pandas as pd
    
    extractor = TextFeatureExtractor()
    
    # Test
    test_text = "This is a great and amazing quote about love and happiness!"
    features = extractor.extract_all_features(test_text)
    
    print("Text Features:", features)