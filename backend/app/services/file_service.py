"""
File service layer for business logic operations related to files.
"""
from typing import Optional, Dict, Any
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session

from app.utils.file_upload import FileUploadService
from app.repositories.file_repository import FileRepository
from app.repositories.project_repository import ProjectRepository
from app.repositories.hackathon_repository import HackathonRepository
from app.repositories.user_repository import UserRepository


class FileService:
    """Service for file-related business logic."""

    def __init__(self):
        self.upload_service = FileUploadService()
        self.file_repo = FileRepository()
        self.project_repo = ProjectRepository()
        self.hackathon_repo = HackathonRepository()
        self.user_repo = UserRepository()

    async def upload_file(
        self, db: Session, file: UploadFile, file_type: str,
        entity_id: Optional[int] = None, user_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Upload a file with business logic validation."""
        # Business logic: validate entity exists and user has permission
        if entity_id:
            if file_type == "project":
                project = self.project_repo.get(db, entity_id)
                if not project:
                    raise HTTPException(
                        status_code=404, detail="Project not found"
                    )
                # Check if user has permission to upload to project
                if user_id and project.created_by != user_id:
                    # Could add more complex permission logic here
                    pass
            elif file_type == "hackathon":
                hackathon = self.hackathon_repo.get(db, entity_id)
                if not hackathon:
                    raise HTTPException(
                        status_code=404, detail="Hackathon not found"
                    )
            elif file_type == "avatar":
                user = self.user_repo.get(db, entity_id)
                if not user:
                    raise HTTPException(
                        status_code=404, detail="User not found"
                    )
                # Check if user is uploading their own avatar
                if user_id and user.id != user_id:
                    raise HTTPException(
                        status_code=403,
                        detail="Cannot upload avatar for another user"
                    )

        # Use the upload service to handle the actual upload
        upload_result = await self.upload_service.save_upload_file(
            file, file_type
        )

        # Create file record in database
        file_data = {
            "filename": upload_result["filename"],
            "original_filename": file.filename,
            "file_path": upload_result["file_path"],
            "file_type": file_type,
            "mime_type": file.content_type,
            "size": upload_result["size"],
            "entity_id": entity_id,
            "uploaded_by": user_id
        }

        file_record = self.file_repo.create(db, obj_in=file_data)

        # Return combined result
        return {
            "id": file_record.id,
            "filename": file_record.filename,
            "original_filename": file_record.original_filename,
            "file_path": file_record.file_path,
            "file_type": file_record.file_type,
            "mime_type": file_record.mime_type,
            "size": file_record.size,
            "entity_id": file_record.entity_id,
            "uploaded_by": file_record.uploaded_by,
            "created_at": file_record.created_at,
            "url": upload_result["url"]
        }

    def get_file(self, db: Session, file_id: int) -> Optional[Dict[str, Any]]:
        """Get file information by ID."""
        file_record = self.file_repo.get(db, file_id)
        if not file_record:
            return None

        # Build URL
        url = self.upload_service.get_file_url(file_record.file_path)

        return {
            "id": file_record.id,
            "filename": file_record.filename,
            "original_filename": file_record.original_filename,
            "file_path": file_record.file_path,
            "file_type": file_record.file_type,
            "mime_type": file_record.mime_type,
            "size": file_record.size,
            "entity_id": file_record.entity_id,
            "uploaded_by": file_record.uploaded_by,
            "created_at": file_record.created_at,
            "url": url
        }

    def delete_file(self, db: Session, file_id: int, user_id: int) -> bool:
        """Delete a file (with permission check)."""
        file_record = self.file_repo.get(db, file_id)
        if not file_record:
            return False

        # Business logic: check permissions
        # Allow deletion by uploader or admin
        user = self.user_repo.get(db, user_id)
        if not user:
            return False

        can_delete = False
        if file_record.uploaded_by == user_id:
            can_delete = True
        elif user.is_admin:
            can_delete = True

        if not can_delete:
            return False

        # Delete physical file
        try:
            self.upload_service.delete_file(file_record.file_path)
        except Exception:
            # Log error but continue with database deletion
            pass

        # Delete database record
        self.file_repo.delete(db, id=file_id)
        return True

    def get_entity_files(
        self, db: Session, file_type: str, entity_id: int
    ) -> list:
        """Get all files for an entity."""
        files = self.file_repo.get_by_entity(db, file_type, entity_id)
        result = []
        for file_record in files:
            url = self.upload_service.get_file_url(file_record.file_path)
            result.append({
                "id": file_record.id,
                "filename": file_record.filename,
                "original_filename": file_record.original_filename,
                "file_path": file_record.file_path,
                "file_type": file_record.file_type,
                "mime_type": file_record.mime_type,
                "size": file_record.size,
                "entity_id": file_record.entity_id,
                "uploaded_by": file_record.uploaded_by,
                "created_at": file_record.created_at,
                "url": url
            })
        return result


# Global instance for dependency injection
file_service = FileService()
