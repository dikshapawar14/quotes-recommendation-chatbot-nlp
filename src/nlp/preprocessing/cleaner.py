"""
Text Cleaner Module
"""

import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')

class TextCleaner:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
    
    def basic_clean(self, text):
        if not isinstance(text, str):
            return ""
        
        text = text.lower()
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text
    
    def remove_stopwords(self, text):
        words = text.split()
        filtered = [w for w in words if w not in self.stop_words]
        return ' '.join(filtered)
    
    def lemmatize_text(self, text):
        words = text.split()
        lemmatized = [self.lemmatizer.lemmatize(w) for w in words]
        return ' '.join(lemmatized)
    
    def clean_pipeline(self, text, remove_stops=True, lemmatize=True):
        cleaned = self.basic_clean(text)
        
        if remove_stops:
            cleaned = self.remove_stopwords(cleaned)
        
        if lemmatize:
            cleaned = self.lemmatize_text(cleaned)
        
        return cleaned
    
    def process_quotes_dataframe(self, df, text_column='quote'):
        print("🔄 Processing quotes...")
        
        df['cleaned_quote'] = df[text_column].apply(self.clean_pipeline)
        
        if 'author' in df.columns:
            df['cleaned_author'] = df['author'].apply(self.basic_clean)
        
        if 'category' in df.columns:
            df['cleaned_category'] = df['category'].apply(self.basic_clean)
        
        df['text_for_embedding'] = df['cleaned_quote']
        
        if 'cleaned_author' in df.columns:
            df['text_for_embedding'] += " by " + df['cleaned_author']
        
        if 'cleaned_category' in df.columns:
            df['text_for_embedding'] += " category " + df['cleaned_category']
        
        print(f"✅ Processed {len(df)} quotes")
        return df