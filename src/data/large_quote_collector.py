# src/data/large_quote_collector.py
"""
Large Scale Quote Collector - 500K+ quotes
"""

import pandas as pd
import requests
import zipfile
import io
import os

class LargeQuoteCollector:
    """
    Bade quote datasets collect karne ka class
    """
    
    def __init__(self):
        self.quotes_df = None
        
    def download_quotes_500k(self, save_path='data/raw/quotes_500k.csv'):
        """
        Quotes-500K dataset download karo (500,000 quotes)
        Source: https://github.com/lakpa-finju/Quotes-500K [citation:6]
        """
        print("🔄 Downloading Quotes-500K dataset...")
        
        # Dataset link - Google Drive se download
        url = "https://goo.gl/R3Sa34"  # Original link
        
        try:
            # Alternative: Kaggle se download
            # Ye manual download ho sakta hai
            print("📥 Please download manually from:")
            print("   https://www.kaggle.com/datasets/manann/quotes-500k")
            print("   and place in data/raw/ directory")
            
            # Agar file already exist kare
            if os.path.exists('data/raw/quotes_500k.csv'):
                df = pd.read_csv('data/raw/quotes_500k.csv')
                print(f"✅ Loaded {len(df)} quotes from local file")
                return df
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def download_kaggle_quote_dataset(self):
        """
        Kaggle quote dataset (multiple sources)
        """
        print("🔄 Kaggle datasets available:")
        datasets = [
            {
                'name': 'Quotes 500K',
                'url': 'https://www.kaggle.com/datasets/manann/quotes-500k',
                'size': '500,000 quotes'
            },
            {
                'name': 'English Quotes Dataset',
                'url': 'https://www.kaggle.com/datasets/mittalishu/english-quotes-dataset',
                'size': '50,000 quotes'
            },
            {
                'name': 'Quote Dataset',
                'url': 'https://www.kaggle.com/datasets/marufchowdhury/quote-dataset',
                'size': '200,000+ quotes'
            }
        ]
        
        for ds in datasets:
            print(f"\n📁 {ds['name']}:")
            print(f"   Size: {ds['size']}")
            print(f"   URL: {ds['url']}")
    
    def combine_multiple_datasets(self):
        """
        Multiple datasets ko combine karo
        """
        all_quotes = []
        
        # Dataset 1: Sample quotes (jo pehle banaya)
        if os.path.exists('data/raw/sample_quotes.csv'):
            df1 = pd.read_csv('data/raw/sample_quotes.csv')
            all_quotes.append(df1)
            print(f"✅ Sample quotes: {len(df1)}")
        
        # Dataset 2: Quotes-500K
        if os.path.exists('data/raw/quotes_500k.csv'):
            df2 = pd.read_csv('data/raw/quotes_500k.csv')
            all_quotes.append(df2)
            print(f"✅ Quotes-500K: {len(df2)}")
        
        # Sabko combine karo
        if all_quotes:
            combined_df = pd.concat(all_quotes, ignore_index=True)
            combined_df = combined_df.drop_duplicates(subset=['quote'])
            print(f"✅ Total unique quotes: {len(combined_df)}")
            return combined_df
        
        return None