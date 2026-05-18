"""
Hybrid detector combining rule-based and deep learning approaches
Provides best of both worlds for maximum accuracy
"""
from typing import Dict, List
import logging
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from ai_models.text_detector import TextScamDetector
from ai_models.image_detector import ImageDeepfakeDetector
from app.ai.transformers_detector import get_transformer_detector
from app.ai.cnn_detector import get_cnn_detector

logger = logging.getLogger(__name__)


class HybridTextDetector:
    """
    Hybrid text detector combining rule-based and transformer models
    """
    
    def __init__(self):
        self.rule_based = TextScamDetector()
        # Temporarily disable transformers for immediate functionality
        # They can be enabled later after models download
        self.use_transformers = False
        logger.info("Hybrid text detector initialized (rule-based only for fast startup)")
        
        # Uncomment below to enable transformers after models are downloaded
        # try:
        #     self.transformer = get_transformer_detector()
        #     self.use_transformers = True
        #     logger.info("Hybrid text detector initialized with transformers")
        # except Exception as e:
        #     logger.warning(f"Transformers not available, using rule-based only: {e}")
        #     self.use_transformers = False
    
    def analyze(self, text: str) -> Dict:
        """
        Analyze text using hybrid approach
        
        Args:
            text: Input text
            
        Returns:
            Combined analysis results
        """
        # Get rule-based analysis
        rule_result = self.rule_based.analyze(text)
        
        if not self.use_transformers:
            return rule_result
        
        try:
            # Get transformer analysis
            transformer_result = self.transformer.analyze(text)
            
            # Combine results
            combined = self._combine_results(rule_result, transformer_result)
            
            return combined
            
        except Exception as e:
            logger.error(f"Error in transformer analysis, falling back to rule-based: {e}")
            return rule_result
    
    def _combine_results(self, rule_result: Dict, transformer_result: Dict) -> Dict:
        """
        Combine rule-based and transformer results
        
        Strategy:
        - Use weighted average of confidences
        - Combine indicators from both
        - Generate comprehensive explanation
        """
        # Weights (transformers are generally more accurate)
        rule_weight = 0.4
        transformer_weight = 0.6
        
        # Combine confidences
        rule_conf = rule_result["confidence"]
        trans_conf = transformer_result["confidence"]
        
        combined_confidence = (rule_conf * rule_weight) + (trans_conf * transformer_weight)
        
        # Determine if scam (either model says yes with high confidence)
        is_scam = (
            (rule_result["isScam"] and rule_conf > 60) or
            (transformer_result["is_scam"] and trans_conf > 60) or
            combined_confidence > 50
        )
        
        # Determine threat level
        if combined_confidence >= 70:
            threat_level = "high"
        elif combined_confidence >= 40:
            threat_level = "medium"
        else:
            threat_level = "low"
        
        # Combine indicators
        indicators = list(set(rule_result["indicators"]))
        
        # Add transformer insights
        if transformer_result.get("model_scores"):
            model_scores = transformer_result["model_scores"]
            
            if model_scores.get("spam", {}).get("is_spam"):
                indicators.append("🤖 Deep learning: Spam patterns detected")
            
            if model_scores.get("zero_shot", {}).get("is_scam"):
                top_label = model_scores["zero_shot"].get("top_label", "")
                indicators.append(f"🤖 Deep learning: Classified as '{top_label}'")
            
            if model_scores.get("sentiment", {}).get("label") == "NEGATIVE":
                indicators.append("🤖 Deep learning: Negative sentiment (manipulation tactics)")
        
        # Generate combined explanation
        explanation = self._generate_combined_explanation(
            is_scam,
            combined_confidence,
            rule_result,
            transformer_result
        )
        
        # Use rule-based recommendation (it's more detailed)
        recommendation = rule_result["recommendation"]
        
        return {
            "isScam": is_scam,
            "confidence": round(combined_confidence, 1),
            "threatLevel": threat_level,
            "explanation": explanation,
            "indicators": indicators[:10],  # Limit to top 10
            "recommendation": recommendation,
            "analysis_details": {
                "rule_based_confidence": rule_conf,
                "transformer_confidence": trans_conf,
                "model_scores": transformer_result.get("model_scores", {})
            }
        }
    
    def _generate_combined_explanation(
        self,
        is_scam: bool,
        confidence: float,
        rule_result: Dict,
        transformer_result: Dict
    ) -> str:
        """Generate comprehensive explanation"""
        if is_scam:
            return (
                f"Our hybrid AI system (combining rule-based analysis and deep learning transformers) "
                f"detected this as a potential scam with {confidence:.1f}% confidence. "
                f"Both traditional pattern matching and advanced neural networks identified suspicious characteristics. "
                f"{transformer_result.get('explanation', '')}"
            )
        else:
            return (
                f"Our hybrid AI system analyzed this message and found it likely legitimate. "
                f"Only {confidence:.1f}% scam indicators detected, which is below the threshold for concern. "
                f"Both rule-based and deep learning models found no significant red flags. "
                f"The content follows standard communication patterns."
            )


class HybridImageDetector:
    """
    Hybrid image detector combining traditional CV and CNN models
    """
    
    def __init__(self):
        self.traditional = ImageDeepfakeDetector()
        # Temporarily disable CNN for immediate functionality
        self.use_cnn = False
        logger.info("Hybrid image detector initialized (traditional CV only for fast startup)")
        
        # Uncomment below to enable CNN after models are downloaded
        # try:
        #     self.cnn = get_cnn_detector()
        #     self.use_cnn = True
        #     logger.info("Hybrid image detector initialized with CNN")
        # except Exception as e:
        #     logger.warning(f"CNN not available, using traditional CV only: {e}")
        #     self.use_cnn = False
    
    async def analyze(self, image_bytes: bytes, filename: str) -> Dict:
        """
        Analyze image using hybrid approach
        
        Args:
            image_bytes: Image file bytes
            filename: Original filename
            
        Returns:
            Combined analysis results
        """
        # Get traditional CV analysis
        traditional_result = await self.traditional.analyze(image_bytes, filename)
        
        if not self.use_cnn:
            return traditional_result
        
        try:
            # Get CNN analysis
            cnn_result = await self.cnn.analyze(image_bytes, filename)
            
            # Combine results
            combined = self._combine_results(traditional_result, cnn_result)
            
            return combined
            
        except Exception as e:
            logger.error(f"Error in CNN analysis, falling back to traditional: {e}")
            return traditional_result
    
    def _combine_results(self, traditional_result: Dict, cnn_result: Dict) -> Dict:
        """
        Combine traditional CV and CNN results
        
        Strategy:
        - CNN gets higher weight (more accurate)
        - Combine manipulation indicators
        - Merge technical details
        """
        # Weights (CNN is generally more accurate, but traditional is more conservative)
        traditional_weight = 0.4  # Increased from 0.3
        cnn_weight = 0.6  # Decreased from 0.7
        
        # Combine confidences
        trad_conf = traditional_result["confidence"]
        cnn_conf = cnn_result["confidence"]
        
        combined_confidence = (trad_conf * traditional_weight) + (cnn_conf * cnn_weight)
        
        # Determine if fake - require BOTH to agree for high confidence
        is_fake = (
            (traditional_result["isFake"] and cnn_result["is_fake"]) or  # Both agree
            (traditional_result["isFake"] and trad_conf > 70) or  # Traditional very confident
            (cnn_result["is_fake"] and cnn_conf > 75) or  # CNN very confident
            combined_confidence > 65  # Increased from 50
        )
        
        # Determine threat level with higher thresholds
        if combined_confidence >= 75:  # Increased from 70
            threat_level = "high"
        elif combined_confidence >= 55:  # Increased from 40
            threat_level = "medium"
        else:
            threat_level = "low"
        
        # Combine manipulation types
        manipulation_types = list(set(traditional_result["manipulationTypes"]))
        
        # Add CNN insights
        if cnn_result.get("features"):
            features = cnn_result["features"]
            
            if features.get("edge_density", 0) > 50:
                manipulation_types.append("🤖 CNN: Unusual edge artifacts detected")
            elif features.get("edge_density", 0) < 10:
                manipulation_types.append("🤖 CNN: Suspiciously smooth (possible AI generation)")
            
            if cnn_result.get("quality_score", 50) > 90:
                manipulation_types.append("🤖 CNN: Suspiciously perfect quality")
        
        # Generate combined explanation
        explanation = self._generate_combined_explanation(
            is_fake,
            combined_confidence,
            traditional_result,
            cnn_result
        )
        
        # Merge technical details
        technical_details = {
            **traditional_result.get("technicalDetails", {}),
            **cnn_result.get("technical_details", {}),
            "cnn_score": cnn_result.get("cnn_score", 50),
            "traditional_score": trad_conf,
            "combined_confidence": combined_confidence
        }
        
        return {
            "isFake": is_fake,
            "confidence": round(combined_confidence, 1),
            "threatLevel": threat_level,
            "explanation": explanation,
            "manipulationTypes": manipulation_types[:10],
            "recommendation": traditional_result["recommendation"],
            "technicalDetails": technical_details
        }
    
    def _generate_combined_explanation(
        self,
        is_fake: bool,
        confidence: float,
        traditional_result: Dict,
        cnn_result: Dict
    ) -> str:
        """Generate comprehensive explanation"""
        if is_fake:
            return (
                f"Our hybrid AI system (combining traditional computer vision and deep learning CNN) "
                f"detected this image as potentially fake/manipulated with {confidence:.1f}% confidence. "
                f"Both classical image analysis and neural network models identified suspicious patterns. "
                f"{cnn_result.get('explanation', '')}"
            )
        else:
            return (
                f"Our hybrid AI system analyzed this image and found it likely authentic. "
                f"Only {confidence:.1f}% manipulation indicators detected, which is below the threshold for concern. "
                f"Both traditional CV and deep learning models found no significant manipulation patterns. "
                f"The image characteristics are consistent with genuine photography."
            )


# Global instances
_hybrid_text_detector = None
_hybrid_image_detector = None


def get_hybrid_text_detector() -> HybridTextDetector:
    """Get or create hybrid text detector"""
    global _hybrid_text_detector
    if _hybrid_text_detector is None:
        _hybrid_text_detector = HybridTextDetector()
    return _hybrid_text_detector


def get_hybrid_image_detector() -> HybridImageDetector:
    """Get or create hybrid image detector"""
    global _hybrid_image_detector
    if _hybrid_image_detector is None:
        _hybrid_image_detector = HybridImageDetector()
    return _hybrid_image_detector
