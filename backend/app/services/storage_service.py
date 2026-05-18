"""
Service layer for file storage operations
"""
from supabase import Client
from app.config import settings
import logging
import uuid
from typing import Tuple
import os

logger = logging.getLogger(__name__)


class StorageService:
    """Service for managing file uploads to Supabase Storage"""
    
    def __init__(self, db: Client):
        self.db = db
        self.bucket = settings.SUPABASE_STORAGE_BUCKET
    
    async def upload_image(
        self,
        user_id: str,
        file_bytes: bytes,
        filename: str,
        content_type: str
    ) -> Tuple[str, str]:
        """
        Upload image to Supabase Storage
        
        Args:
            user_id: User ID
            file_bytes: Image file bytes
            filename: Original filename
            content_type: MIME type
            
        Returns:
            Tuple of (storage_path, public_url)
        """
        try:
            # Generate unique filename
            file_ext = os.path.splitext(filename)[1]
            unique_filename = f"{uuid.uuid4()}{file_ext}"
            
            # Create user-specific path
            storage_path = f"{user_id}/{unique_filename}"
            
            # Upload to Supabase Storage
            result = self.db.storage.from_(self.bucket).upload(
                path=storage_path,
                file=file_bytes,
                file_options={"content-type": content_type}
            )
            
            # Get public URL
            public_url = self.db.storage.from_(self.bucket).get_public_url(storage_path)
            
            logger.info(f"Uploaded image {filename} for user {user_id}")
            return storage_path, public_url
            
        except Exception as e:
            logger.error(f"Error uploading image: {e}")
            raise
    
    async def delete_image(self, storage_path: str) -> bool:
        """
        Delete image from Supabase Storage
        
        Args:
            storage_path: Path to file in storage
            
        Returns:
            True if deleted successfully
        """
        try:
            self.db.storage.from_(self.bucket).remove([storage_path])
            logger.info(f"Deleted image {storage_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting image: {e}")
            return False
    
    async def get_image_url(self, storage_path: str) -> str:
        """
        Get public URL for stored image
        
        Args:
            storage_path: Path to file in storage
            
        Returns:
            Public URL
        """
        try:
            return self.db.storage.from_(self.bucket).get_public_url(storage_path)
        except Exception as e:
            logger.error(f"Error getting image URL: {e}")
            raise
