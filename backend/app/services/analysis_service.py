"""
Service layer for analysis operations
"""
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from supabase import Client
import logging

logger = logging.getLogger(__name__)


class AnalysisService:
    """Service for managing text and image analyses"""
    
    def __init__(self, db: Client):
        self.db = db
    
    async def save_text_analysis(
        self,
        user_id: str,
        text_content: str,
        is_scam: bool,
        confidence: float,
        threat_level: str,
        explanation: str,
        indicators: List[str],
        recommendation: str
    ) -> Dict:
        """
        Save text analysis to database
        
        Args:
            user_id: User ID
            text_content: Analyzed text
            is_scam: Whether text is a scam
            confidence: Confidence score (0-100)
            threat_level: Threat level (low/medium/high)
            explanation: AI explanation
            indicators: List of detected indicators
            recommendation: Recommendation text
            
        Returns:
            Saved analysis record
        """
        try:
            data = {
                "user_id": user_id,
                "text_content": text_content,
                "is_scam": is_scam,
                "confidence": confidence,
                "threat_level": threat_level,
                "explanation": explanation,
                "indicators": indicators,
                "recommendation": recommendation
            }
            
            result = self.db.table("text_analyses").insert(data).execute()
            
            # Update average confidence
            await self._update_avg_confidence(user_id)
            
            logger.info(f"Saved text analysis for user {user_id}")
            return result.data[0] if result.data else {}
            
        except Exception as e:
            logger.error(f"Error saving text analysis: {e}")
            raise
    
    async def save_image_analysis(
        self,
        user_id: str,
        image_url: str,
        image_filename: str,
        is_fake: bool,
        confidence: float,
        threat_level: str,
        explanation: str,
        manipulation_types: List[str],
        recommendation: str,
        technical_details: Dict
    ) -> Dict:
        """
        Save image analysis to database
        
        Args:
            user_id: User ID
            image_url: URL to stored image
            image_filename: Original filename
            is_fake: Whether image is fake/manipulated
            confidence: Confidence score (0-100)
            threat_level: Threat level (low/medium/high)
            explanation: AI explanation
            manipulation_types: List of detected manipulations
            recommendation: Recommendation text
            technical_details: Technical analysis details
            
        Returns:
            Saved analysis record
        """
        try:
            data = {
                "user_id": user_id,
                "image_url": image_url,
                "image_filename": image_filename,
                "is_fake": is_fake,
                "confidence": confidence,
                "threat_level": threat_level,
                "explanation": explanation,
                "manipulation_types": manipulation_types,
                "recommendation": recommendation,
                "technical_details": technical_details
            }
            
            result = self.db.table("image_analyses").insert(data).execute()
            
            # Update average confidence
            await self._update_avg_confidence(user_id)
            
            logger.info(f"Saved image analysis for user {user_id}")
            return result.data[0] if result.data else {}
            
        except Exception as e:
            logger.error(f"Error saving image analysis: {e}")
            raise
    
    async def get_user_text_analyses(
        self,
        user_id: str,
        limit: int = 10,
        offset: int = 0
    ) -> List[Dict]:
        """
        Get user's text analysis history
        
        Args:
            user_id: User ID
            limit: Number of records to return
            offset: Offset for pagination
            
        Returns:
            List of text analyses
        """
        try:
            result = self.db.table("text_analyses")\
                .select("*")\
                .eq("user_id", user_id)\
                .order("created_at", desc=True)\
                .range(offset, offset + limit - 1)\
                .execute()
            
            return result.data if result.data else []
            
        except Exception as e:
            logger.error(f"Error fetching text analyses: {e}")
            raise
    
    async def get_user_image_analyses(
        self,
        user_id: str,
        limit: int = 10,
        offset: int = 0
    ) -> List[Dict]:
        """
        Get user's image analysis history
        
        Args:
            user_id: User ID
            limit: Number of records to return
            offset: Offset for pagination
            
        Returns:
            List of image analyses
        """
        try:
            result = self.db.table("image_analyses")\
                .select("*")\
                .eq("user_id", user_id)\
                .order("created_at", desc=True)\
                .range(offset, offset + limit - 1)\
                .execute()
            
            return result.data if result.data else []
            
        except Exception as e:
            logger.error(f"Error fetching image analyses: {e}")
            raise
    
    async def get_user_statistics(self, user_id: str) -> Optional[Dict]:
        """
        Get user statistics
        
        Args:
            user_id: User ID
            
        Returns:
            User statistics or None
        """
        try:
            result = self.db.table("user_statistics")\
                .select("*")\
                .eq("user_id", user_id)\
                .single()\
                .execute()
            
            return result.data if result.data else None
            
        except Exception as e:
            logger.error(f"Error fetching user statistics: {e}")
            # Return default stats if not found
            return {
                "total_scans": 0,
                "text_scans": 0,
                "image_scans": 0,
                "threats_detected": 0,
                "high_risk_detections": 0,
                "medium_risk_detections": 0,
                "low_risk_detections": 0,
                "avg_confidence": 0,
                "security_score": 100
            }
    
    async def delete_analysis(
        self,
        user_id: str,
        analysis_id: str,
        analysis_type: str = "text"
    ) -> bool:
        """
        Delete an analysis record
        
        Args:
            user_id: User ID
            analysis_id: Analysis ID
            analysis_type: Type of analysis ('text' or 'image')
            
        Returns:
            True if deleted successfully
        """
        try:
            table = "text_analyses" if analysis_type == "text" else "image_analyses"
            
            self.db.table(table)\
                .delete()\
                .eq("id", analysis_id)\
                .eq("user_id", user_id)\
                .execute()
            
            logger.info(f"Deleted {analysis_type} analysis {analysis_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting analysis: {e}")
            return False

    async def track_performance(
        self,
        user_id: Optional[str],
        analysis_type: str,
        response_time_ms: int,
        success: bool = True,
        error_message: Optional[str] = None
    ):
        """Track performance metrics"""
        try:
            data = {
                "user_id": user_id,
                "analysis_type": analysis_type,
                "response_time_ms": response_time_ms,
                "success": success,
                "error_message": error_message
            }
            
            self.db.table("performance_metrics").insert(data).execute()
            
        except Exception as e:
            logger.error(f"Error tracking performance: {e}")
    
    async def get_scan_frequency(self, user_id: str, days: int = 7) -> List[Dict]:
        """Get scan frequency for last N days"""
        try:
            result = self.db.rpc('get_scan_frequency', {
                'p_user_id': user_id,
                'p_days': days
            }).execute()
            
            return result.data if result.data else []
            
        except Exception as e:
            logger.error(f"Error fetching scan frequency: {e}")
            return [
                {
                    "scan_date": (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d"),
                    "total_scans": 0,
                    "text_scans": 0,
                    "image_scans": 0,
                    "threats_detected": 0
                }
                for i in range(days - 1, -1, -1)
            ]
    
    async def get_performance_metrics(self, user_id: Optional[str] = None, hours: int = 24) -> Dict:
        """Get average response time and success rate"""
        try:
            result = self.db.rpc('get_avg_response_time', {
                'p_user_id': user_id,
                'p_hours': hours
            }).execute()
            
            metrics = {}
            if result.data:
                for row in result.data:
                    metrics[row['analysis_type']] = {
                        'avg_response_time_ms': float(row['avg_response_time_ms'] or 0),
                        'success_rate': float(row['success_rate'] or 100)
                    }
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error fetching performance metrics: {e}")
            return {
                'text': {'avg_response_time_ms': 0, 'success_rate': 100},
                'image': {'avg_response_time_ms': 0, 'success_rate': 100}
            }
    
    async def get_system_health(self) -> Dict:
        """Get system health status"""
        try:
            result = self.db.table("system_health")\
                .select("*")\
                .order("last_check", desc=True)\
                .execute()
            
            if result.data:
                total_uptime = sum(float(row['uptime_percentage']) for row in result.data)
                avg_uptime = total_uptime / len(result.data) if result.data else 100
                
                return {
                    'status': 'online' if all(row['status'] == 'online' for row in result.data) else 'degraded',
                    'uptime_percentage': round(avg_uptime, 2),
                    'services': result.data
                }
            
            return {
                'status': 'online',
                'uptime_percentage': 100.0,
                'services': []
            }
            
        except Exception as e:
            logger.error(f"Error fetching system health: {e}")
            return {
                'status': 'online',
                'uptime_percentage': 100.0,
                'services': []
            }
    
    async def _update_avg_confidence(self, user_id: str):
        """Update average confidence for user"""
        try:
            self.db.rpc('calculate_avg_confidence', {'p_user_id': user_id}).execute()
        except Exception as e:
            logger.error(f"Error updating avg confidence: {e}")
