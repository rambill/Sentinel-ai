"""
Analysis routes for text and image detection
"""
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, status
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta

from app.middleware.auth import get_current_user_id, get_current_user_optional
from app.database import get_db
from app.services.analysis_service import AnalysisService
from app.services.storage_service import StorageService
from app.config import settings

# Import AI models
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

# Use hybrid detectors for best accuracy
from app.ai.hybrid_detector import get_hybrid_text_detector, get_hybrid_image_detector

router = APIRouter(prefix="/api", tags=["analysis"])

# Initialize AI models (lazy loaded)
def get_text_detector():
    return get_hybrid_text_detector()

def get_image_detector():
    return get_hybrid_image_detector()


# Request/Response Models
class TextAnalysisRequest(BaseModel):
    text: str


class TextAnalysisResponse(BaseModel):
    isScam: bool
    confidence: float
    threatLevel: str
    explanation: str
    indicators: List[str]
    recommendation: str
    timestamp: str
    saved: bool = False


class ImageAnalysisResponse(BaseModel):
    isFake: bool
    confidence: float
    threatLevel: str
    explanation: str
    manipulationTypes: List[str]
    recommendation: str
    technicalDetails: dict
    timestamp: str
    saved: bool = False


class AnalysisHistoryResponse(BaseModel):
    id: str
    type: str
    content: str
    result: str
    confidence: float
    threat_level: str
    timestamp: str


# Text Analysis Endpoint
@router.post("/analyze-text", response_model=TextAnalysisResponse)
async def analyze_text(
    request: TextAnalysisRequest,
    user_id: Optional[str] = Depends(get_current_user_optional)
):
    """
    Analyze text for scam indicators using REAL AI
    
    Features:
    - Phishing detection
    - Scam pattern recognition
    - AI-generated text detection
    - URL analysis
    - Grammar and sentiment analysis
    - Threat level assessment
    """
    
    start_time = datetime.now()
    success = True
    error_msg = None
    
    try:
        # Use REAL AI detector (hybrid: rule-based + transformers)
        text_detector = get_text_detector()
        result = text_detector.analyze(request.text)
        
        # Calculate response time
        response_time_ms = int((datetime.now() - start_time).total_seconds() * 1000)
        
        # Save to database if user is authenticated
        saved = False
        if user_id:
            try:
                db = get_db()
                analysis_service = AnalysisService(db)
                
                # Save analysis
                await analysis_service.save_text_analysis(
                    user_id=user_id,
                    text_content=request.text,
                    is_scam=result["isScam"],
                    confidence=result["confidence"],
                    threat_level=result["threatLevel"],
                    explanation=result["explanation"],
                    indicators=result["indicators"],
                    recommendation=result["recommendation"]
                )
                
                # Track performance
                await analysis_service.track_performance(
                    user_id=user_id,
                    analysis_type="text",
                    response_time_ms=response_time_ms,
                    success=True
                )
                
                saved = True
            except Exception as e:
                logger.error(f"Error saving analysis: {e}")
        
        return TextAnalysisResponse(
            isScam=result["isScam"],
            confidence=result["confidence"],
            threatLevel=result["threatLevel"],
            explanation=result["explanation"],
            indicators=result["indicators"],
            recommendation=result["recommendation"],
            timestamp=datetime.now().isoformat(),
            saved=saved
        )
    except Exception as e:
        success = False
        error_msg = str(e)
        
        # Track failed performance
        if user_id:
            try:
                db = get_db()
                analysis_service = AnalysisService(db)
                response_time_ms = int((datetime.now() - start_time).total_seconds() * 1000)
                await analysis_service.track_performance(
                    user_id=user_id,
                    analysis_type="text",
                    response_time_ms=response_time_ms,
                    success=False,
                    error_message=error_msg
                )
            except:
                pass
        
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


# Image Analysis Endpoint
@router.post("/analyze-image", response_model=ImageAnalysisResponse)
async def analyze_image(
    file: UploadFile = File(...),
    user_id: Optional[str] = Depends(get_current_user_optional)
):
    """
    Analyze image for AI generation and manipulation using REAL AI
    
    Features:
    - Deepfake detection
    - AI-generated image detection
    - Photo manipulation detection
    - EXIF metadata analysis
    - Compression artifact analysis
    - Frequency domain analysis
    - Edge and noise pattern analysis
    """
    
    start_time = datetime.now()
    
    # Validate file type
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    # Validate file size
    file_bytes = await file.read()
    if len(file_bytes) > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(status_code=400, detail="File size exceeds 10MB limit")
    
    try:
        # Use REAL AI detector (hybrid: traditional CV + CNN)
        image_detector = get_image_detector()
        result = await image_detector.analyze(file_bytes, file.filename)
        
        # Calculate response time
        response_time_ms = int((datetime.now() - start_time).total_seconds() * 1000)
        
        # Save to database if user is authenticated
        saved = False
        image_url = ""
        
        if user_id:
            try:
                db = get_db()
                storage_service = StorageService(db)
                analysis_service = AnalysisService(db)
                
                # Upload image to storage
                storage_path, image_url = await storage_service.upload_image(
                    user_id=user_id,
                    file_bytes=file_bytes,
                    filename=file.filename,
                    content_type=file.content_type
                )
                
                # Save analysis to database
                await analysis_service.save_image_analysis(
                    user_id=user_id,
                    image_url=image_url,
                    image_filename=file.filename,
                    is_fake=result["isFake"],
                    confidence=result["confidence"],
                    threat_level=result["threatLevel"],
                    explanation=result["explanation"],
                    manipulation_types=result["manipulationTypes"],
                    recommendation=result["recommendation"],
                    technical_details=result["technicalDetails"]
                )
                
                # Track performance
                await analysis_service.track_performance(
                    user_id=user_id,
                    analysis_type="image",
                    response_time_ms=response_time_ms,
                    success=True
                )
                
                saved = True
            except Exception as e:
                logger.error(f"Error saving image analysis: {e}")
        
        return ImageAnalysisResponse(
            isFake=result["isFake"],
            confidence=result["confidence"],
            threatLevel=result["threatLevel"],
            explanation=result["explanation"],
            manipulationTypes=result["manipulationTypes"],
            recommendation=result["recommendation"],
            technicalDetails=result["technicalDetails"],
            timestamp=datetime.now().isoformat(),
            saved=saved
        )
    except Exception as e:
        # Track failed performance
        if user_id:
            try:
                db = get_db()
                analysis_service = AnalysisService(db)
                response_time_ms = int((datetime.now() - start_time).total_seconds() * 1000)
                await analysis_service.track_performance(
                    user_id=user_id,
                    analysis_type="image",
                    response_time_ms=response_time_ms,
                    success=False,
                    error_message=str(e)
                )
            except:
                pass
        
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


# Get Analysis History
@router.get("/history")
async def get_history(
    user_id: Optional[str] = Depends(get_current_user_optional),
    limit: int = 20,
    offset: int = 0
):
    """Get user's analysis history"""
    
    # If no user, return empty history
    if not user_id:
        return {"history": []}
    
    try:
        db = get_db()
        analysis_service = AnalysisService(db)
        
        # Get both text and image analyses
        text_analyses = await analysis_service.get_user_text_analyses(user_id, limit, offset)
        image_analyses = await analysis_service.get_user_image_analyses(user_id, limit, offset)
        
        # Combine and format
        history = []
        
        for analysis in text_analyses:
            history.append({
                "id": analysis["id"],
                "type": "text",
                "content": analysis["text_content"][:100] + "..." if len(analysis["text_content"]) > 100 else analysis["text_content"],
                "result": "Scam" if analysis["is_scam"] else "Legitimate",
                "confidence": analysis["confidence"],
                "threat_level": analysis["threat_level"],
                "timestamp": analysis["created_at"]
            })
        
        for analysis in image_analyses:
            history.append({
                "id": analysis["id"],
                "type": "image",
                "content": analysis["image_filename"],
                "result": "Fake" if analysis["is_fake"] else "Authentic",
                "confidence": analysis["confidence"],
                "threat_level": analysis["threat_level"],
                "timestamp": analysis["created_at"],
                "image_url": analysis["image_url"]
            })
        
        # Sort by timestamp
        history.sort(key=lambda x: x["timestamp"], reverse=True)
        
        return {"history": history[:limit]}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch history: {str(e)}")


# Get User Statistics
@router.get("/statistics")
async def get_statistics(user_id: Optional[str] = Depends(get_current_user_optional)):
    """Get user statistics"""
    
    # If no user, return default stats
    if not user_id:
        return {
            "totalScans": 0,
            "textScans": 0,
            "imageScans": 0,
            "threatsDetected": 0,
            "highRiskDetections": 0,
            "mediumRiskDetections": 0,
            "lowRiskDetections": 0,
            "avgConfidence": 0,
            "securityScore": 100,
            "lastScanAt": None
        }
    
    try:
        db = get_db()
        analysis_service = AnalysisService(db)
        
        stats = await analysis_service.get_user_statistics(user_id)
        
        return {
            "totalScans": stats.get("total_scans", 0),
            "textScans": stats.get("text_scans", 0),
            "imageScans": stats.get("image_scans", 0),
            "threatsDetected": stats.get("threats_detected", 0),
            "highRiskDetections": stats.get("high_risk_detections", 0),
            "mediumRiskDetections": stats.get("medium_risk_detections", 0),
            "lowRiskDetections": stats.get("low_risk_detections", 0),
            "avgConfidence": stats.get("avg_confidence", 0),
            "securityScore": stats.get("security_score", 100),
            "lastScanAt": stats.get("last_scan_at")
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch statistics: {str(e)}")


# Delete Analysis
@router.delete("/analysis/{analysis_id}")
async def delete_analysis(
    analysis_id: str,
    analysis_type: str,
    user_id: str = Depends(get_current_user_id)
):
    """Delete an analysis record"""
    try:
        db = get_db()
        analysis_service = AnalysisService(db)
        
        success = await analysis_service.delete_analysis(user_id, analysis_id, analysis_type)
        
        if not success:
            raise HTTPException(status_code=404, detail="Analysis not found")
        
        return {"message": "Analysis deleted successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete analysis: {str(e)}")


# Get Scan Frequency
@router.get("/scan-frequency")
async def get_scan_frequency(
    user_id: Optional[str] = Depends(get_current_user_optional),
    days: int = 7
):
    """Get scan frequency for last N days"""
    
    if not user_id:
        # Return empty data for non-logged in users
        return {"frequency": [
            {
                "scan_date": (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d"),
                "total_scans": 0,
                "text_scans": 0,
                "image_scans": 0,
                "threats_detected": 0
            }
            for i in range(days - 1, -1, -1)
        ]}
    
    try:
        db = get_db()
        analysis_service = AnalysisService(db)
        
        frequency = await analysis_service.get_scan_frequency(user_id, days)
        
        return {"frequency": frequency}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch scan frequency: {str(e)}")


# Get Performance Metrics
@router.get("/performance")
async def get_performance(
    user_id: Optional[str] = Depends(get_current_user_optional),
    hours: int = 24
):
    """Get performance metrics"""
    
    try:
        db = get_db()
        analysis_service = AnalysisService(db)
        
        metrics = await analysis_service.get_performance_metrics(user_id, hours)
        
        return {"metrics": metrics}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch performance metrics: {str(e)}")


# Get System Health
@router.get("/system-health")
async def get_system_health():
    """Get system health status"""
    
    try:
        db = get_db()
        analysis_service = AnalysisService(db)
        
        health = await analysis_service.get_system_health()
        
        return health
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch system health: {str(e)}")
