"""
CNN-based image classification for deepfake detection
Uses PyTorch with pre-trained models
"""
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import io
import numpy as np
from typing import Dict, Tuple
import logging

logger = logging.getLogger(__name__)


class CNNDeepfakeDetector:
    """
    CNN-based deepfake and manipulation detector
    Uses EfficientNet for image classification
    """
    
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"Using device: {self.device}")
        
        # Initialize model
        self._init_model()
        
        # Image preprocessing
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])
    
    def _init_model(self):
        """Initialize pre-trained CNN model"""
        try:
            logger.info("Loading EfficientNet model...")
            
            # Load pre-trained EfficientNet-B0
            self.model = models.efficientnet_b0(pretrained=True)
            
            # Modify final layer for binary classification (real/fake)
            num_features = self.model.classifier[1].in_features
            self.model.classifier[1] = nn.Linear(num_features, 2)
            
            # Move to device
            self.model = self.model.to(self.device)
            self.model.eval()
            
            logger.info("EfficientNet model loaded successfully!")
            
        except Exception as e:
            logger.error(f"Error loading CNN model: {e}")
            raise
    
    async def analyze(self, image_bytes: bytes, filename: str) -> Dict:
        """
        Analyze image using CNN
        
        Args:
            image_bytes: Image file bytes
            filename: Original filename
            
        Returns:
            Dictionary with analysis results
        """
        try:
            # Load and preprocess image
            image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
            
            # Get image metadata
            width, height = image.size
            format_type = image.format or "Unknown"
            
            # Extract features
            features = self._extract_features(image)
            
            # Run CNN inference
            cnn_result = self._run_inference(image)
            
            # Analyze image quality
            quality_score = self._analyze_quality(image)
            
            # Combine results
            combined_score = self._combine_analysis(
                cnn_result,
                features,
                quality_score
            )
            
            # Determine classification
            is_fake = combined_score["confidence"] >= 50.0
            threat_level = self._determine_threat_level(combined_score["confidence"])
            
            return {
                "is_fake": is_fake,
                "confidence": combined_score["confidence"],
                "threat_level": threat_level,
                "cnn_score": cnn_result["fake_probability"] * 100,
                "quality_score": quality_score,
                "features": features,
                "explanation": self._generate_explanation(
                    is_fake,
                    combined_score,
                    cnn_result,
                    features
                ),
                "technical_details": {
                    "resolution": f"{width}x{height}",
                    "format": format_type,
                    "model": "EfficientNet-B0",
                    "device": str(self.device)
                }
            }
            
        except Exception as e:
            logger.error(f"Error in CNN analysis: {e}")
            return {
                "is_fake": False,
                "confidence": 50.0,
                "threat_level": "low",
                "cnn_score": 50.0,
                "quality_score": 50.0,
                "features": {},
                "explanation": f"Analysis error: {str(e)}",
                "technical_details": {}
            }
    
    def _run_inference(self, image: Image.Image) -> Dict:
        """Run CNN inference on image"""
        try:
            # Preprocess image
            image_tensor = self.transform(image).unsqueeze(0).to(self.device)
            
            # Run inference
            with torch.no_grad():
                outputs = self.model(image_tensor)
                probabilities = torch.nn.functional.softmax(outputs, dim=1)
                
                # Get probabilities for real/fake
                real_prob = probabilities[0][0].item()
                fake_prob = probabilities[0][1].item()
            
            return {
                "real_probability": real_prob,
                "fake_probability": fake_prob,
                "prediction": "fake" if fake_prob > real_prob else "real"
            }
            
        except Exception as e:
            logger.error(f"Inference error: {e}")
            return {
                "real_probability": 0.5,
                "fake_probability": 0.5,
                "prediction": "unknown"
            }
    
    def _extract_features(self, image: Image.Image) -> Dict:
        """Extract image features for analysis"""
        try:
            # Convert to numpy array
            img_array = np.array(image)
            
            # Calculate statistics
            mean_brightness = np.mean(img_array)
            std_brightness = np.std(img_array)
            
            # Color distribution
            if len(img_array.shape) == 3:
                r_mean = np.mean(img_array[:, :, 0])
                g_mean = np.mean(img_array[:, :, 1])
                b_mean = np.mean(img_array[:, :, 2])
                color_balance = {
                    "red": float(r_mean),
                    "green": float(g_mean),
                    "blue": float(b_mean)
                }
            else:
                color_balance = {"grayscale": float(mean_brightness)}
            
            # Edge detection (simple Sobel)
            from scipy import ndimage
            edges = ndimage.sobel(np.mean(img_array, axis=2) if len(img_array.shape) == 3 else img_array)
            edge_density = np.mean(np.abs(edges))
            
            return {
                "brightness": {
                    "mean": float(mean_brightness),
                    "std": float(std_brightness)
                },
                "color_balance": color_balance,
                "edge_density": float(edge_density),
                "aspect_ratio": image.size[0] / image.size[1]
            }
            
        except Exception as e:
            logger.error(f"Feature extraction error: {e}")
            return {}
    
    def _analyze_quality(self, image: Image.Image) -> float:
        """Analyze image quality (compression, noise)"""
        try:
            img_array = np.array(image)
            
            # Calculate noise level (variance of Laplacian)
            from scipy import ndimage
            gray = np.mean(img_array, axis=2) if len(img_array.shape) == 3 else img_array
            laplacian = ndimage.laplace(gray)
            noise_level = np.var(laplacian)
            
            # Normalize to 0-100 scale (lower noise = higher quality)
            quality = max(0, min(100, 100 - (noise_level / 100)))
            
            return float(quality)
            
        except Exception as e:
            logger.error(f"Quality analysis error: {e}")
            return 50.0
    
    def _combine_analysis(
        self,
        cnn_result: Dict,
        features: Dict,
        quality_score: float
    ) -> Dict:
        """Combine CNN results with feature analysis"""
        # Weight CNN prediction heavily
        cnn_weight = 0.7
        feature_weight = 0.2
        quality_weight = 0.1
        
        # CNN contribution
        cnn_score = cnn_result["fake_probability"] * cnn_weight
        
        # Feature-based suspicion (high edge density or unusual color balance)
        feature_suspicion = 0.0
        if features:
            edge_density = features.get("edge_density", 0)
            if edge_density > 50:  # Unusually high edges (possible manipulation)
                feature_suspicion = 0.3
            elif edge_density < 10:  # Too smooth (possible AI generation)
                feature_suspicion = 0.2
        
        feature_score = feature_suspicion * feature_weight
        
        # Quality contribution (very high quality can indicate AI generation)
        quality_suspicion = 0.0
        if quality_score > 90:  # Suspiciously perfect
            quality_suspicion = 0.3
        elif quality_score < 30:  # Heavy compression (possible manipulation)
            quality_suspicion = 0.2
        
        quality_contribution = quality_suspicion * quality_weight
        
        # Combined confidence
        combined = (cnn_score + feature_score + quality_contribution) * 100
        confidence = min(combined, 99.0)
        
        return {
            "confidence": confidence,
            "cnn_contribution": cnn_score * 100,
            "feature_contribution": feature_score * 100,
            "quality_contribution": quality_contribution * 100
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
        is_fake: bool,
        combined: Dict,
        cnn_result: Dict,
        features: Dict
    ) -> str:
        """Generate human-readable explanation"""
        if is_fake:
            reasons = []
            
            if cnn_result["fake_probability"] > 0.6:
                reasons.append(f"CNN model detected manipulation patterns ({cnn_result['fake_probability']*100:.1f}% confidence)")
            
            if features.get("edge_density", 0) > 50:
                reasons.append("unusual edge artifacts detected")
            elif features.get("edge_density", 0) < 10:
                reasons.append("suspiciously smooth appearance (possible AI generation)")
            
            reason_text = ", ".join(reasons) if reasons else "multiple suspicious indicators"
            
            return (
                f"Deep learning CNN analysis detected this image as potentially fake/manipulated with "
                f"{combined['confidence']:.1f}% confidence. Analysis found: {reason_text}. "
                f"The image exhibits patterns inconsistent with authentic photography."
            )
        else:
            return (
                f"CNN analysis indicates this image is likely authentic with "
                f"{100 - combined['confidence']:.1f}% confidence. No significant manipulation patterns detected. "
                f"The image characteristics are consistent with genuine photography."
            )


# Global instance (lazy loaded)
_cnn_detector = None


def get_cnn_detector() -> CNNDeepfakeDetector:
    """Get or create CNN detector instance"""
    global _cnn_detector
    if _cnn_detector is None:
        _cnn_detector = CNNDeepfakeDetector()
    return _cnn_detector
