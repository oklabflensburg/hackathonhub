"""
File upload utility for handling file uploads in the application.
"""
import os
import uuid
from pathlib import Path
from fastapi import UploadFile, status
import shutil

from app.i18n.helpers import raise_i18n_http_exception


class FileUploadService:
    def __init__(self):
        # Try to use UPLOAD_DIR from environment, fallback to ./uploads
        # If ./uploads is not writable, use /tmp/uploads
        default_dir = "./uploads"
        upload_dir = os.getenv("UPLOAD_DIR", default_dir)

        # Check if directory is writable
        upload_path = Path(upload_dir)
        if not upload_dir or not self._is_writable(upload_path):
            # Fallback to /tmp/uploads
            tmp_upload = Path("/tmp/uploads")
            tmp_upload.mkdir(parents=True, exist_ok=True)
            upload_dir = str(tmp_upload)
            print(f"WARNING: Using fallback upload directory: {upload_dir}")

        self.upload_dir = Path(upload_dir)
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

    def _is_writable(self, path: Path) -> bool:
        """Check if a directory is writable"""
        try:
            # Try to create a test file
            test_file = path / ".write_test"
            test_file.touch()
            test_file.unlink()
            return True
        except (OSError, IOError):
            return False

    def validate_file(self, file: UploadFile, locale: str = "en") -> None:
        """Validate file size and type"""
        # Check file size
        file.file.seek(0, 2)  # Seek to end
        file_size = file.file.tell()
        file.file.seek(0)  # Reset to beginning

        if file_size > self.max_file_size:
            raise_i18n_http_exception(
                locale=locale,
                status_code=status.HTTP_400_BAD_REQUEST,
                translation_key="errors.file_too_large",
                max_size=self.max_file_size // (1024 * 1024)
            )

        # Check file extension
        file_extension = Path(file.filename).suffix.lower()
        if file_extension not in self.allowed_extensions:
            raise_i18n_http_exception(
                locale=locale,
                status_code=status.HTTP_400_BAD_REQUEST,
                translation_key="errors.file_type_not_allowed",
                types=", ".join(self.allowed_extensions)
            )

    async def save_upload_file(
        self,
        file: UploadFile,
        file_type: str = "project",
        locale: str = "en"
    ) -> str:
        """Save uploaded file and return the file path"""
        # Validate file
        self.validate_file(file, locale)

        # Get directory for file type
        if file_type not in self.type_to_dir:
            raise_i18n_http_exception(
                locale=locale,
                status_code=status.HTTP_400_BAD_REQUEST,
                translation_key="errors.invalid_file_type",
                allowed_types=", ".join(self.type_to_dir.keys())
            )

        type_dir = self.type_to_dir[file_type]
        upload_path = self.upload_dir / type_dir
        upload_path.mkdir(parents=True, exist_ok=True)

        # Generate unique filename
        file_extension = Path(file.filename).suffix.lower()
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = upload_path / unique_filename

        # Save file
        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        except Exception as e:
            raise_i18n_http_exception(
                locale=locale,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                translation_key="errors.failed_to_save_file",
                error=str(e)
            )

        # Return relative path
        return str(file_path.relative_to(self.upload_dir))

    def get_file_url(self, file_path: str) -> str:
        """Get URL for a file"""
        if not file_path:
            return ""
        
        # Check if file exists
        full_path = self.upload_dir / file_path
        if not full_path.exists():
            return ""
        
        # Return relative URL
        return f"/static/uploads/{file_path}"


# Singleton instance
file_upload_service = FileUploadService()

# Alias for backward compatibility with legacy code
file_upload = file_upload_service