"""
GoEmotions Dataset Preprocessor
"""

import pandas as pd
import numpy as np
import os

class GoEmotionsPreprocessor:
    def __init__(self, filepath='data/raw/quotes_500k.csv'):
        print("🔄 Loading GoEmotions dataset...")
        self.df = pd.read_csv(filepath)
        print(f"✅ Loaded {len(self.df)} records")
        
        # Emotion columns list
        self.emotion_columns = [
            'admiration', 'amusement', 'anger', 'annoyance', 'approval',
            'caring', 'confusion', 'curiosity', 'desire', 'disappointment',
            'disapproval', 'disgust', 'embarrassment', 'excitement', 'fear',
            'gratitude', 'grief', 'joy', 'love', 'nervousness',
            'optimism', 'pride', 'realization', 'relief', 'remorse',
            'sadness', 'surprise', 'neutral'
        ]
    
    def convert_to_quotes_format(self):
        """Convert GoEmotions format to our quotes format"""
        
        # Create new dataframe
        quotes_df = pd.DataFrame()
        
        # Copy text as quote
        quotes_df['quote'] = self.df['text']
        
        # Add author (unknown for this dataset)
        quotes_df['author'] = 'Unknown'
        
        # Determine main category based on emotions
        def get_main_category(row):
            emotions = []
            for col in self.emotion_columns:
                if row[col] == 1:
                    emotions.append(col)
            
            if not emotions:
                return 'General'
            
            # Map emotions to categories
            emotion_to_category = {
                'admiration': 'Inspirational',
                'amusement': 'Humor',
                'anger': 'Anger',
                'annoyance': 'Frustration',
                'approval': 'Wisdom',
                'caring': 'Love',
                'confusion': 'Confusion',
                'curiosity': 'Curiosity',
                'desire': 'Desire',
                'disappointment': 'Disappointment',
                'disapproval': 'Judgment',
                'disgust': 'Disgust',
                'embarrassment': 'Embarrassment',
                'excitement': 'Excitement',
                'fear': 'Fear',
                'gratitude': 'Gratitude',
                'grief': 'Grief',
                'joy': 'Joy',
                'love': 'Love',
                'nervousness': 'Anxiety',
                'optimism': 'Optimism',
                'pride': 'Pride',
                'realization': 'Realization',
                'relief': 'Relief',
                'remorse': 'Remorse',
                'sadness': 'Sadness',
                'surprise': 'Surprise',
                'neutral': 'Neutral'
            }
            
            # Return category for first emotion
            return emotion_to_category.get(emotions[0], 'General')
        
        quotes_df['category'] = self.df.apply(get_main_category, axis=1)
        
        # Add emotion labels as a list
        def get_emotion_list(row):
            emotions = []
            for col in self.emotion_columns:
                if row[col] == 1:
                    emotions.append(col)
            return ','.join(emotions)
        
        quotes_df['emotions'] = self.df.apply(get_emotion_list, axis=1)
        
        print(f"✅ Converted to quotes format: {len(quotes_df)} quotes")
        print(f"   Categories: {quotes_df['category'].nunique()}")
        
        return quotes_df
    
    def save_processed_data(self, output_path='data/processed/quotes_with_emotions.csv'):
        """Save processed data"""
        quotes_df = self.convert_to_quotes_format()
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        quotes_df.to_csv(output_path, index=False)
        print(f"💾 Saved to {output_path}")
        
        return quotes_df

if __name__ == "__main__":
    preprocessor = GoEmotionsPreprocessor()
    quotes_df = preprocessor.save_processed_data()
    
    # Show sample
    print("\n📝 Sample quotes:")
    print(quotes_df[['quote', 'category', 'emotions']].head())