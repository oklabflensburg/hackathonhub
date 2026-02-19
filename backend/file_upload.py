import os
import uuid
from pathlib import Path
from fastapi import UploadFile, HTTPException
import shutil
from typing import Optional


class FileUploadService:
    def __init__(self):
        self.upload_dir = Path(os.getenv("UPLOAD_DIR", "./uploads"))
        self.max_file_size = 10 * 1024 * 1024  # 10MB
        self.allowed_extensions = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
        self.allowed_mime_types = {
            "image/jpeg",
            "image/png",
            "image/gif",
            "image/webp"
        }
        # Map API type to directory name
        self.type_to_dir = {
            "project": "projects",
            "hackathon": "hackathons",
            "avatar": "avatars"
        }
        
    async def save_upload_file(
        self, 
        upload_file: UploadFile, 
        subdirectory: str,
        entity_id: Optional[int] = None
    ) -> str:
        """
        Save an uploaded file and return its relative path
        
        Args:
            upload_file: The uploaded file
            subdirectory: Type of upload (project, hackathon, avatar)
            entity_id: Optional ID for organizing files by entity
            
        Returns:
            Relative file path for database storage
        """
        # Validate file
        await self._validate_file(upload_file)
        
        # Generate unique filename
        file_ext = Path(upload_file.filename).suffix.lower()
        if file_ext not in self.allowed_extensions:
            file_ext = self._get_extension_from_mime(upload_file.content_type)
        
        unique_filename = f"{uuid.uuid4()}{file_ext}"
        
        # Create directory structure
        # Map API type to directory name (e.g., "hackathon" -> "hackathons")
        dir_name = self.type_to_dir.get(subdirectory, subdirectory)
        
        if entity_id:
            save_dir = self.upload_dir / dir_name / str(entity_id)
        else:
            save_dir = self.upload_dir / dir_name / "temp"
        
        try:
            save_dir.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Cannot create directory {save_dir}: {str(e)}. "
                       "Please check permissions or set UPLOAD_DIR env var."
            )
        
        # Save file
        file_path = save_dir / unique_filename
        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(upload_file.file, buffer)
        except OSError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Cannot write file {file_path}: {str(e)}. "
                       f"Please check disk space and permissions."
            )
        
        # Return relative path for database storage
        if entity_id:
            return f"/uploads/{dir_name}/{entity_id}/{unique_filename}"
        else:
            return f"/uploads/{dir_name}/temp/{unique_filename}"
    
    async def _validate_file(self, upload_file: UploadFile):
        """Validate file size, type, and content"""
        # Check file size
        upload_file.file.seek(0, 2)  # Seek to end
        file_size = upload_file.file.tell()
        upload_file.file.seek(0)  # Reset to beginning
        
        if file_size > self.max_file_size:
            max_size_mb = self.max_file_size // (1024 * 1024)
            raise HTTPException(
                status_code=400, 
                detail=f"File too large. Max size: {max_size_mb}MB"
            )
        
        if file_size == 0:
            raise HTTPException(status_code=400, detail="File is empty")
        
        # Check file extension
        file_ext = Path(upload_file.filename).suffix.lower()
        if file_ext and file_ext not in self.allowed_extensions:
            allowed_exts = ', '.join(self.allowed_extensions)
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid file extension. Allowed: {allowed_exts}"
            )
        
        # Check MIME type
        if upload_file.content_type not in self.allowed_mime_types:
            allowed_mimes = ', '.join(self.allowed_mime_types)
            detail_msg = f"Invalid file type. Allowed: {allowed_mimes}"
            raise HTTPException(status_code=400, detail=detail_msg)
    
    def _get_extension_from_mime(self, mime_type: str) -> str:
        """Get file extension from MIME type"""
        mime_to_ext = {
            "image/jpeg": ".jpg",
            "image/png": ".png",
            "image/gif": ".gif",
            "image/webp": ".webp"
        }
        return mime_to_ext.get(mime_type, ".jpg")
    
    def delete_file(self, file_path: str) -> bool:
        """
        Delete a file by its relative path
        
        Args:
            file_path: Relative file path
                (e.g., /uploads/projects/1/abc123.jpg)
            
        Returns:
            True if file was deleted, False otherwise
        """
        if not file_path or not file_path.startswith("/uploads/"):
            return False
        
        # Convert relative path to absolute path
        absolute_path = self.upload_dir / file_path.lstrip("/uploads/")
        
        try:
            if absolute_path.exists():
                absolute_path.unlink()
                return True
        except Exception:
            pass
        
        return False
    
    def get_file_url(self, file_path: str) -> str:
        """
        Get the full URL for a file path
        
        Args:
            file_path: Relative file path
            
        Returns:
            Full URL for accessing the file
        """
        if not file_path:
            return ""
        
        # If it's already a full URL (from external sources), return as-is
        if file_path.startswith(("http://", "https://")):
            return file_path
        
        # For local files, return path that will be served by static files
        return f"/static{file_path}"
    
    def cleanup_temp_files(self, subdirectory: str, max_age_hours: int = 24):
        """
        Clean up temporary files older than max_age_hours
        
        Args:
            subdirectory: Type of upload (project, hackathon, avatar)
            max_age_hours: Maximum age in hours before deletion
        """
        import time
        temp_dir = self.upload_dir / subdirectory / "temp"
        
        if not temp_dir.exists():
            return
        
        current_time = time.time()
        max_age_seconds = max_age_hours * 3600
        
        for file_path in temp_dir.glob("*"):
            if file_path.is_file():
                file_age = current_time - file_path.stat().st_mtime
                if file_age > max_age_seconds:
                    try:
                        file_path.unlink()
                    except Exception:
                        pass


# Create a singleton instance
file_upload_service = FileUploadService()