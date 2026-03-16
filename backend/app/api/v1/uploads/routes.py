"""
File upload API routes.
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Request, Depends
from typing import Optional

from app.core.auth import get_current_user
from app.core.database import get_db
from app.core.permissions import PERMISSION_CODES, user_has_permission
from app.utils.file_upload import file_upload_service
from sqlalchemy.orm import Session
from app.api.openapi_responses import UNAUTHORIZED_RESPONSE

router = APIRouter(responses=UNAUTHORIZED_RESPONSE)


@router.post("/upload")
async def upload_file(
    request: Request,
    file: UploadFile = File(...),
    type: Optional[str] = "project",
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Upload a file (image) for projects, hackathons, or users."""
    if not user_has_permission(db, current_user, PERMISSION_CODES["uploads_create"]):
        raise HTTPException(status_code=403, detail="Not authorized to upload files")

    try:
        file_path = await file_upload_service.save_upload_file(file, type)
        relative_url = file_upload_service.get_file_url(file_path)

        # If relative_url is empty (file doesn't exist), construct default
        if not relative_url:
            relative_url = f"/static/uploads/{type}s/{file.filename}"

        # Convert to absolute URL
        base_url = str(request.base_url).rstrip('/')
        absolute_url = f"{base_url}{relative_url}"

        return {
            "url": absolute_url,
            "filename": file.filename,
            "message": "File uploaded successfully"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"File upload failed: {str(e)}"
        )
