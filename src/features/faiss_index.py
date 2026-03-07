"""
FAISS Index Module
"""

import faiss
import numpy as np
import pickle
import os

class FaissIndex:
    def __init__(self, dimension=None):
        self.index = None
        self.dimension = dimension
        self.quotes_df = None
    
    def create_index(self, embeddings, quotes_df):
        print("🔄 Creating FAISS index...")
        
        self.dimension = embeddings.shape[1]
        self.quotes_df = quotes_df
        self.index = faiss.IndexFlatL2(self.dimension)
        self.index.add(embeddings)
        
        print(f"✅ FAISS index created with {self.index.ntotal} vectors")
        return self.index
    
    def search(self, query_embedding, k=5):
        if self.index is None:
            return None
        
        distances, indices = self.index.search(query_embedding.reshape(1, -1), k)
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx != -1:
                quote_data = self.quotes_df.iloc[idx].to_dict()
                quote_data['distance'] = float(distances[0][i])
                quote_data['similarity'] = 1 / (1 + float(distances[0][i]))
                results.append(quote_data)
        
        return results
    
    def save_index(self, save_dir='data/embeddings/'):
        os.makedirs(save_dir, exist_ok=True)
        faiss.write_index(self.index, os.path.join(save_dir, 'faiss_index.bin'))
        print(f"💾 FAISS index saved")
    
    def load_index(self, load_dir='data/embeddings/'):
        index_path = os.path.join(load_dir, 'faiss_index.bin')
        
        if os.path.exists(index_path):
            self.index = faiss.read_index(index_path)
            print(f"✅ FAISS index loaded with {self.index.ntotal} vectors")
            return True
        return False

if __name__ == "__main__":
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    
    from src.features.embeddings import QuoteEmbeddings
    
    embedder = QuoteEmbeddings()
    if embedder.load_embeddings():
        faiss_index = FaissIndex()
        faiss_index.create_index(embedder.embeddings, embedder.quotes_df)
        faiss_index.save_index()