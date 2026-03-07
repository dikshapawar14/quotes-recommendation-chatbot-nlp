"""
Advanced Emotion Detection - 27 emotions cover karne ke liye
Using GoEmotions dataset approach [citation:2][citation:7]
"""

import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F

class AdvancedEmotionDetector:
    """
    27 emotions detect karne wala advanced model
    """
    
    def __init__(self):
        # GoEmotions pre-trained model [citation:7]
        self.model_name = 'monologg/bert-base-cased-goemotions'
        
        print(f"🔄 Loading GoEmotions model...")
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
        
        # 27 emotions + neutral [citation:2]
        self.emotion_labels = [
            'admiration', 'amusement', 'anger', 'annoyance', 'approval',
            'caring', 'confusion', 'curiosity', 'desire', 'disappointment',
            'disapproval', 'disgust', 'embarrassment', 'excitement', 'fear',
            'gratitude', 'grief', 'joy', 'love', 'nervousness',
            'optimism', 'pride', 'realization', 'relief', 'remorse',
            'sadness', 'surprise', 'neutral'
        ]
        
        # Emotion groups for better understanding
        self.emotion_groups = {
            'positive': ['admiration', 'amusement', 'approval', 'caring', 'excitement',
                        'gratitude', 'joy', 'love', 'optimism', 'pride', 'relief', 'surprise'],
            'negative': ['anger', 'annoyance', 'disappointment', 'disapproval', 'disgust',
                        'embarrassment', 'fear', 'grief', 'nervousness', 'remorse', 'sadness'],
            'confusion': ['confusion', 'curiosity', 'realization'],
            'desire': ['desire'],
            'neutral': ['neutral']
        }
    
    def detect_emotions(self, text, threshold=0.3):
        """
        Saare 27 emotions ki probabilities detect karo
        """
        inputs = self.tokenizer(text, return_tensors='pt', truncation=True, max_length=128)
        
        with torch.no_grad():
            outputs = self.model(**inputs)
            probabilities = F.softmax(outputs.logits, dim=-1)
        
        # Results dictionary banao
        results = {}
        for i, label in enumerate(self.emotion_labels):
            prob = probabilities[0][i].item()
            if prob > threshold:  # Sirf significant emotions
                results[label] = prob
        
        # Sort by probability
        results = dict(sorted(results.items(), key=lambda x: x[1], reverse=True))
        
        return results
    
    def get_primary_emotion(self, text):
        """
        Sabse dominant emotion do
        """
        emotions = self.detect_emotions(text, threshold=0.1)
        if emotions:
            primary = list(emotions.keys())[0]
            return primary, emotions[primary]
        return 'neutral', 0.0
    
    def get_emotion_group(self, emotion):
        """
        Emotion kis group mein aata hai
        """
        for group, emotions in self.emotion_groups.items():
            if emotion in emotions:
                return group
        return 'other'
    
    def analyze_user_message(self, message):
        """
        Complete emotion analysis
        """
        # Detect all emotions
        emotions = self.detect_emotions(message)
        
        # Primary emotion
        primary, confidence = self.get_primary_emotion(message)
        
        # Emotion group
        group = self.get_emotion_group(primary)
        
        # Multi-label emotions (top 3)
        top_emotions = list(emotions.keys())[:3]
        
        return {
            'primary_emotion': primary,
            'confidence': confidence,
            'emotion_group': group,
            'all_emotions': emotions,
            'top_emotions': top_emotions,
            'text': message
        }

# Example usage
if __name__ == "__main__":
    detector = AdvancedEmotionDetector()
    
    test_messages = [
        "I'm so excited about my new job! I can't wait to start.",
        "I feel really sad and lonely today. Nothing seems to work.",
        "I love you so much, you mean everything to me.",
        "This is so confusing, I don't understand what's happening.",
        "I'm grateful for all the support from my friends.",
        "That makes me angry! How could they do that?"
    ]
    
    for msg in test_messages:
        result = detector.analyze_user_message(msg)
        print(f"\n📝 Message: {msg}")
        print(f"🎯 Primary: {result['primary_emotion']} ({result['confidence']:.2f})")
        print(f"📌 Group: {result['emotion_group']}")
        print(f"🔍 Top emotions: {result['top_emotions']}")