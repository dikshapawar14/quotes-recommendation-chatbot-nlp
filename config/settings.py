"""
Configuration Settings
"""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

class Config:
    # Paths
    PROJECT_ROOT = BASE_DIR
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw')
    PROCESSED_DATA_DIR = os.path.join(DATA_DIR, 'processed')
    EMBEDDINGS_DIR = os.path.join(DATA_DIR, 'embeddings')
    
    # Models
    SENTENCE_TRANSFORMER_MODEL = 'all-MiniLM-L6-v2'
    EMBEDDING_DIMENSION = 384
    
    # Recommendations
    DEFAULT_TOP_K = 5
    MAX_TOP_K = 10
    
    # App
    APP_NAME = "Quote Recommendation Chatbot"
    APP_ICON = "💭"
    APP_LAYOUT = "wide"
    
    # Files
    QUOTES_FILE = 'sample_quotes.csv'
    PROCESSED_QUOTES_FILE = 'cleaned_quotes.csv'
    EMBEDDINGS_FILE = 'quote_embeddings.npy'
    FAISS_INDEX_FILE = 'faiss_index.bin'

# Create config object
config = Config()