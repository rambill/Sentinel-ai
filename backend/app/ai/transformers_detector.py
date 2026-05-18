"""
Transformer-based text classification for scam detection
Uses Hugging Face Transformers with DistilBERT
"""
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch
from typing import Dict, List, Tuple
import logging
from functools import lru_cache

logger = logging.getLogger(__name__)


class TransformerScamDetector:
    """
    Advanced scam detection using transformer models
    Combines multiple pre-trained models for better accuracy
    """
    
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Using device: {self.device}")
        
        # Initialize models
        self._init_models()
    
    def _init_models(self):
        """Initialize transformer models"""
        try:
            # Sentiment analysis model (for detecting manipulation)
            logger.info("Loading sentiment analysis model...")
            self.sentiment_analyzer = pipeline(
                "sentiment-analysis",
                model="distilbert-base-uncased-finetuned-sst-2-english",
                device=0 if self.device == "cuda" else -1
            )
            
            # Text classification model (for spam/phishing)
            logger.info("Loading text classification model...")
            self.spam_classifier = pipeline(
                "text-classification",
                model="mrm8488/bert-tiny-finetuned-sms-spam-detection",
                device=0 if self.device == "cuda" else -1
            )
            
            # Zero-shot classification for flexible detection
            logger.info("Loading zero-shot classifier...")
            self.zero_shot = pipeline(
                "zero-shot-classification",
                model="facebook/bart-large-mnli",
                device=0 if self.device == "cuda" else -1
            )
            
            logger.info("All transformer models loaded successfully!")
            
        except Exception as e:
            logger.error(f"Error loading models: {e}")
            # Fallback to CPU if CUDA fails
            if self.device == "cuda":
                logger.warning("Falling back to CPU...")
                self.device = "cpu"
                self._init_models()
            else:
                raise
    
    def analyze(self, text: str) -> Dict:
        """
        Analyze text using transformer models
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary with analysis results
        """
        if not text or len(text.strip()) < 10:
            return {
                "is_scam": False,
                "confidence": 50.0,
                "threat_level": "low",
                "model_scores": {},
                "explanation": "Text too short for reliable analysis"
            }
        
        try:
            # Run all models
            sentiment_result = self._analyze_sentiment(text)
            spam_result = self._analyze_spam(text)
            zero_shot_result = self._analyze_zero_shot(text)
            
            # Combine results
            combined_score = self._combine_scores(
                sentiment_result,
                spam_result,
                zero_shot_result
            )
            
            # Determine final classification
            is_scam = combined_score["confidence"] >= 50.0
            threat_level = self._determine_threat_level(combined_score["confidence"])
            
            return {
                "is_scam": is_scam,
                "confidence": combined_score["confidence"],
                "threat_level": threat_level,
                "model_scores": {
                    "sentiment": sentiment_result,
                    "spam": spam_result,
                    "zero_shot": zero_shot_result
                },
                "explanation": self._generate_explanation(
                    is_scam,
                    combined_score,
                    sentiment_result,
                    spam_result,
                    zero_shot_result
                )
            }
            
        except Exception as e:
            logger.error(f"Error in transformer analysis: {e}")
            return {
                "is_scam": False,
                "confidence": 50.0,
                "threat_level": "low",
                "model_scores": {},
                "explanation": f"Analysis error: {str(e)}"
            }
    
    def _analyze_sentiment(self, text: str) -> Dict:
        """Analyze sentiment for manipulation detection"""
        try:
            # Truncate text if too long
            text = text[:512]
            
            result = self.sentiment_analyzer(text)[0]
            
            # Negative sentiment often indicates threats/urgency
            score = result["score"] if result["label"] == "NEGATIVE" else 1 - result["score"]
            
            return {
                "label": result["label"],
                "score": score,
                "confidence": result["score"]
            }
        except Exception as e:
            logger.error(f"Sentiment analysis error: {e}")
            return {"label": "UNKNOWN", "score": 0.5, "confidence": 0.5}
    
    def _analyze_spam(self, text: str) -> Dict:
        """Analyze for spam/phishing patterns"""
        try:
            # Truncate text if too long
            text = text[:512]
            
            result = self.spam_classifier(text)[0]
            
            # Check if classified as spam
            is_spam = result["label"].upper() in ["SPAM", "1", "POSITIVE"]
            score = result["score"] if is_spam else 1 - result["score"]
            
            return {
                "label": result["label"],
                "score": score,
                "confidence": result["score"],
                "is_spam": is_spam
            }
        except Exception as e:
            logger.error(f"Spam analysis error: {e}")
            return {"label": "UNKNOWN", "score": 0.5, "confidence": 0.5, "is_spam": False}
    
    def _analyze_zero_shot(self, text: str) -> Dict:
        """Zero-shot classification for flexible scam detection"""
        try:
            # Truncate text if too long
            text = text[:512]
            
            # Define scam-related labels
            candidate_labels = [
                "phishing attempt",
                "scam message",
                "legitimate communication",
                "urgent threat",
                "financial fraud",
                "normal message"
            ]
            
            result = self.zero_shot(text, candidate_labels)
            
            # Get top prediction
            top_label = result["labels"][0]
            top_score = result["scores"][0]
            
            # Check if top label indicates scam
            scam_labels = ["phishing attempt", "scam message", "urgent threat", "financial fraud"]
            is_scam = top_label in scam_labels
            
            return {
                "top_label": top_label,
                "top_score": top_score,
                "all_scores": dict(zip(result["labels"], result["scores"])),
                "is_scam": is_scam
            }
        except Exception as e:
            logger.error(f"Zero-shot analysis error: {e}")
            return {
                "top_label": "unknown",
                "top_score": 0.5,
                "all_scores": {},
                "is_scam": False
            }
    
    def _combine_scores(
        self,
        sentiment: Dict,
        spam: Dict,
        zero_shot: Dict
    ) -> Dict:
        """
        Combine scores from multiple models
        Uses weighted average with confidence weighting
        """
        # Weights for each model
        weights = {
            "sentiment": 0.2,
            "spam": 0.4,
            "zero_shot": 0.4
        }
        
        # Calculate weighted score
        sentiment_score = sentiment["score"] * weights["sentiment"]
        spam_score = spam["score"] * weights["spam"]
        zero_shot_score = (zero_shot["top_score"] if zero_shot["is_scam"] else (1 - zero_shot["top_score"])) * weights["zero_shot"]
        
        combined = sentiment_score + spam_score + zero_shot_score
        
        # Convert to percentage
        confidence = min(combined * 100, 99.0)
        
        return {
            "confidence": confidence,
            "sentiment_contribution": sentiment_score * 100,
            "spam_contribution": spam_score * 100,
            "zero_shot_contribution": zero_shot_score * 100
        }
    
    def _determine_threat_level(self, confidence: float) -> str:
        """Determine threat level based on confidence"""
        if confidence >= 70:
            return "high"
        elif confidence >= 40:
            return "medium"
        else:
            return "low"
    
    def _generate_explanation(
        self,
        is_scam: bool,
        combined: Dict,
        sentiment: Dict,
        spam: Dict,
        zero_shot: Dict
    ) -> str:
        """Generate human-readable explanation"""
        if is_scam:
            reasons = []
            
            if spam["is_spam"]:
                reasons.append(f"spam classifier detected suspicious patterns ({spam['confidence']*100:.1f}% confidence)")
            
            if zero_shot["is_scam"]:
                reasons.append(f"classified as '{zero_shot['top_label']}' ({zero_shot['top_score']*100:.1f}% confidence)")
            
            if sentiment["label"] == "NEGATIVE":
                reasons.append(f"negative sentiment detected (manipulation tactics)")
            
            reason_text = ", ".join(reasons) if reasons else "multiple suspicious indicators"
            
            return (
                f"Deep learning models detected this as a potential scam with "
                f"{combined['confidence']:.1f}% confidence. Analysis found: {reason_text}. "
                f"The message exhibits patterns commonly found in fraudulent communications."
            )
        else:
            return (
                f"Deep learning analysis indicates this message is likely legitimate with "
                f"{100 - combined['confidence']:.1f}% confidence. No significant scam patterns detected. "
                f"The content follows normal communication patterns."
            )


# Global instance (lazy loaded)
_transformer_detector = None


def get_transformer_detector() -> TransformerScamDetector:
    """Get or create transformer detector instance"""
    global _transformer_detector
    if _transformer_detector is None:
        _transformer_detector = TransformerScamDetector()
    return _transformer_detector
