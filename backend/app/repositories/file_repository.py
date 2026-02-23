"""
File Repository.

This repository handles all database operations for File entities.
"""
from typing import List, Optional
from sqlalchemy.orm import Session

from app.domain.models.shared import File
from app.repositories.base import BaseRepository


class FileRepository(BaseRepository[File]):
    """
    Repository for File operations.
    """
    
    def __init__(self):
        super().__init__(File)
    
    def get_by_user(self, db: Session,
                    user_id: int,
                    skip: int = 0,
                    limit: int = 100) -> List[File]:
        """
        Get files uploaded by a user.
        
        Args:
            db: Database session
            user_id: User ID
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of files uploaded by the user
        """
        return db.query(self.model).filter(
            self.model.uploader_id == user_id
        ).offset(skip).limit(limit).all()
    
    def create_file(self, db: Session,
                    user_id: int,
                    filename: str,
                    filepath: str,
                    file_type: Optional[str] = None,
                    file_size: Optional[int] = None) -> File:
        """
        Create a new file record.
        
        Args:
            db: Database session
            user_id: User ID
            filename: Original filename
            filepath: Path where file is stored
            file_type: File type (optional)
            file_size: File size in bytes (optional)
            
        Returns:
            Created File
        """
        file = File(
            uploader_id=user_id,
            filename=filename,
            filepath=filepath,
            file_type=file_type,
            file_size=file_size
        )
        
        db.add(file)
        db.commit()
        db.refresh(file)
        return file