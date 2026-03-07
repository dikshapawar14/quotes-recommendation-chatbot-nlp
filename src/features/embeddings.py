"""
Embeddings Module - Quotes ko vector mein convert karne ke liye
"""

from sentence_transformers import SentenceTransformer
import numpy as np
import pandas as pd
import pickle
import os
from tqdm import tqdm
import time

class QuoteEmbeddings:
    """Quotes ke embeddings banane ka class"""
    
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        print(f"Loading model: {model_name}")
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)
        self.embeddings = None
        self.quotes_df = None
    
    def create_embeddings(self, quotes_df, text_column='text_for_embedding'):
        print("Creating embeddings for quotes...")
        
        texts = quotes_df[text_column].tolist()
        batch_size = 32
        all_embeddings = []
        
        for i in tqdm(range(0, len(texts), batch_size)):
            batch = texts[i:i+batch_size]
            batch_embeddings = self.model.encode(batch, show_progress_bar=False)
            all_embeddings.append(batch_embeddings)
        
        self.embeddings = np.vstack(all_embeddings)
        self.quotes_df = quotes_df
        
        print(f"Created {len(self.embeddings)} embeddings")
        return self.embeddings
    
    def save_embeddings(self, save_dir='data/embeddings/'):
        os.makedirs(save_dir, exist_ok=True)
        
        np.save(os.path.join(save_dir, 'quote_embeddings.npy'), self.embeddings)
        self.quotes_df.to_csv(os.path.join(save_dir, 'quotes_with_embeddings.csv'), index=False)
        
        info = {
            'model_name': self.model_name,
            'embedding_dim': self.embeddings.shape[1],
            'num_quotes': len(self.embeddings)
        }
        
        with open(os.path.join(save_dir, 'embedding_info.pkl'), 'wb') as f:
            pickle.dump(info, f)
        
        print(f"Embeddings saved")
        return save_dir
    
    def load_embeddings(self, load_dir='data/embeddings/'):
        emb_path = os.path.join(load_dir, 'quote_embeddings.npy')
        df_path = os.path.join(load_dir, 'quotes_with_embeddings.csv')
        
        if os.path.exists(emb_path) and os.path.exists(df_path):
            self.embeddings = np.load(emb_path)
            self.quotes_df = pd.read_csv(df_path)
            print(f"Loaded {len(self.embeddings)} embeddings")
            return True
        return False
    
    def get_embedding(self, text):
        return self.model.encode([text])[0]

if __name__ == "__main__":
    print("Embeddings module ready")