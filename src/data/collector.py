"""
Data Collector Module
"""

import pandas as pd
import os
import random

class QuoteCollector:
    def __init__(self):
        self.quotes = []
    
    def create_sample_data(self):
        sample_quotes = [
            {"quote": "The only way to do great work is to love what you do.", "author": "Steve Jobs", "category": "Inspirational"},
            {"quote": "Life is what happens when you're busy making other plans.", "author": "John Lennon", "category": "Life"},
            {"quote": "The future belongs to those who believe in the beauty of their dreams.", "author": "Eleanor Roosevelt", "category": "Dreams"},
            {"quote": "It does not matter how slowly you go as long as you do not stop.", "author": "Confucius", "category": "Perseverance"},
            {"quote": "Everything you've ever wanted is on the other side of fear.", "author": "George Addair", "category": "Courage"},
            {"quote": "Love all, trust a few, do wrong to none.", "author": "William Shakespeare", "category": "Love"},
            {"quote": "The best thing to hold onto in life is each other.", "author": "Audrey Hepburn", "category": "Love"},
            {"quote": "Love is composed of a single soul inhabiting two bodies.", "author": "Aristotle", "category": "Love"},
            {"quote": "Success is not final, failure is not fatal: it is the courage to continue that counts.", "author": "Winston Churchill", "category": "Success"},
            {"quote": "The only place where success comes before work is in the dictionary.", "author": "Vidal Sassoon", "category": "Success"},
            {"quote": "Happiness is not something ready made. It comes from your own actions.", "author": "Dalai Lama", "category": "Happiness"},
            {"quote": "The most important thing is to enjoy your life - to be happy - it's all that matters.", "author": "Audrey Hepburn", "category": "Happiness"},
            {"quote": "The pain you feel today is the strength you feel tomorrow.", "author": "Unknown", "category": "Emotional"},
            {"quote": "It's okay to not be okay, as long as you don't stay that way.", "author": "Unknown", "category": "Emotional"},
            {"quote": "A friend is someone who knows all about you and still loves you.", "author": "Elbert Hubbard", "category": "Friendship"},
            {"quote": "Friendship is born at that moment when one person says to another, 'What! You too?'", "author": "C.S. Lewis", "category": "Friendship"},
            {"quote": "Don't watch the clock; do what it does. Keep going.", "author": "Sam Levenson", "category": "Motivation"},
            {"quote": "The harder you work for something, the greater you'll feel when you achieve it.", "author": "Unknown", "category": "Motivation"},
            {"quote": "The only true wisdom is in knowing you know nothing.", "author": "Socrates", "category": "Wisdom"},
            {"quote": "The journey of a thousand miles begins with one step.", "author": "Lao Tzu", "category": "Wisdom"},
        ]
        
        # Add more quotes
        categories = ['Inspirational', 'Life', 'Love', 'Success', 'Happiness', 'Emotional', 'Friendship', 'Motivation', 'Wisdom']
        authors = ['Unknown', 'Anonymous', 'Albert Einstein', 'Mark Twain', 'Oscar Wilde', 'Rumi', 'Buddha']
        
        for i in range(80):
            quote = {
                'quote': f"Sample quote number {i+1} about {random.choice(categories)}",
                'author': random.choice(authors),
                'category': random.choice(categories)
            }
            sample_quotes.append(quote)
        
        df = pd.DataFrame(sample_quotes)
        print(f"✅ Created {len(df)} sample quotes")
        return df
    
    def save_to_csv(self, df, filename='data/raw/quotes_dataset.csv'):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        df.to_csv(filename, index=False)
        print(f"💾 Data saved to {filename}")
        return filename

if __name__ == "__main__":
    collector = QuoteCollector()
    df = collector.create_sample_data()
    collector.save_to_csv(df, 'data/raw/sample_quotes.csv')