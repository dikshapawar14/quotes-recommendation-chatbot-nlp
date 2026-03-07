"""
Data Loader Module
"""

import pandas as pd
import os
from src.nlp.preprocessing.cleaner import TextCleaner

class DataLoader:
    def __init__(self, data_path='data/'):
        self.data_path = data_path
        self.cleaner = TextCleaner()
    
    def load_raw_data(self, filename='raw/sample_quotes.csv'):
        filepath = os.path.join(self.data_path, filename)
        
        if not os.path.exists(filepath):
            print(f"❌ File not found: {filepath}")
            return None
        
        if filename.endswith('.csv'):
            df = pd.read_csv(filepath)
        else:
            print(f"❌ Unsupported format: {filename}")
            return None
        
        print(f"✅ Loaded {len(df)} records")
        return df
    
    def load_and_preprocess(self, filename='raw/sample_quotes.csv', save_processed=True):
        df = self.load_raw_data(filename)
        
        if df is None:
            return None
        
        df = self.cleaner.process_quotes_dataframe(df)
        
        if save_processed:
            processed_path = os.path.join(self.data_path, 'processed/cleaned_quotes.csv')
            os.makedirs(os.path.dirname(processed_path), exist_ok=True)
            df.to_csv(processed_path, index=False)
            print(f"💾 Saved processed data")
        
        return df