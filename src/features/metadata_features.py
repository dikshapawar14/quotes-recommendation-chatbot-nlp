"""
Metadata Features Module - Quote metadata se features nikalne ke liye
"""

import pandas as pd
import numpy as np
from datetime import datetime
import re

class MetadataFeatureExtractor:
    """Metadata se features extract karne ka class"""
    
    def __init__(self):
        self.category_keywords = {
            'love': ['love', 'heart', 'romance', 'relationship'],
            'life': ['life', 'live', 'living', 'alive'],
            'success': ['success', 'win', 'achieve', 'goal'],
            'happiness': ['happy', 'joy', 'smile', 'laugh'],
            'wisdom': ['wise', 'knowledge', 'learn', 'understand'],
            'motivation': ['motivate', 'inspire', 'dream', 'believe'],
            'friendship': ['friend', 'together', 'companion'],
            'family': ['family', 'mother', 'father', 'child'],
            'nature': ['nature', 'earth', 'sky', 'ocean']
        }
    
    def extract_author_features(self, author_name):
        """Author name se features"""
        if not isinstance(author_name, str):
            return {}
        
        features = {
            'author_length': len(author_name),
            'author_word_count': len(author_name.split()),
            'author_has_initial': bool(re.search(r'[A-Z]\.', author_name)),
            'author_is_unknown': author_name.lower() in ['unknown', 'anonymous', '']
        }
        
        return features
    
    def extract_category_features(self, category):
        """Category se features"""
        if not isinstance(category, str):
            category = 'General'
        
        features = {
            'category_length': len(category),
            'category': category  # Will be one-hot encoded later
        }
        
        # Add keyword matching
        for cat, keywords in self.category_keywords.items():
            features[f'category_matches_{cat}'] = any(
                kw in category.lower() for kw in keywords
            )
        
        return features
    
    def extract_temporal_features(self, timestamp=None):
        """Time-based features (if available)"""
        if timestamp is None:
            # Default values if no timestamp
            return {
                'hour': 0,
                'day': 0,
                'month': 0,
                'year': 0,
                'is_weekend': False
            }
        
        if isinstance(timestamp, str):
            try:
                dt = pd.to_datetime(timestamp)
            except:
                return self.extract_temporal_features(None)
        else:
            dt = timestamp
        
        features = {
            'hour': dt.hour,
            'day': dt.day,
            'month': dt.month,
            'year': dt.year,
            'day_of_week': dt.dayofweek,
            'is_weekend': dt.dayofweek >= 5
        }
        
        return features
    
    def extract_popularity_features(self, quote_data):
        """Popularity metrics (if available)"""
        features = {}
        
        # Check for like/favorite counts
        if 'likes' in quote_data:
            features['likes'] = quote_data['likes']
        else:
            features['likes'] = 0
        
        if 'favorites' in quote_data:
            features['favorites'] = quote_data['favorites']
        else:
            features['favorites'] = 0
        
        if 'views' in quote_data:
            features['views'] = quote_data['views']
            features['like_ratio'] = features['likes'] / max(quote_data['views'], 1)
        else:
            features['views'] = 0
            features['like_ratio'] = 0
        
        return features
    
    def extract_all_features(self, row):
        """Sabhi metadata features ek saath extract karo"""
        features = {}
        
        # Author features
        if 'author' in row:
            features.update(self.extract_author_features(row['author']))
        
        # Category features
        if 'category' in row:
            features.update(self.extract_category_features(row['category']))
        
        # Popularity features
        features.update(self.extract_popularity_features(row))
        
        return features
    
    def process_quotes_dataframe(self, df):
        """Dataframe ke saare quotes ke metadata features extract karo"""
        print("🔄 Extracting metadata features...")
        
        all_features = []
        for idx, row in df.iterrows():
            features = self.extract_all_features(row)
            all_features.append(features)
        
        # Convert to dataframe
        features_df = pd.DataFrame(all_features)
        
        # One-hot encode category
        if 'category' in features_df.columns:
            category_dummies = pd.get_dummies(
                features_df['category'], 
                prefix='cat', 
                dummy_na=False
            )
            features_df = pd.concat([features_df.drop('category', axis=1), category_dummies], axis=1)
        
        # Add prefix
        features_df = features_df.add_prefix('meta_')
        
        print(f"✅ Extracted {len(features_df.columns)} metadata features")
        return features_df

if __name__ == "__main__":
    extractor = MetadataFeatureExtractor()
    
    # Test
    test_row = {
        'author': 'Albert Einstein',
        'category': 'Inspirational',
        'likes': 1000,
        'views': 5000
    }
    
    features = extractor.extract_all_features(test_row)
    print("Metadata Features:", features)