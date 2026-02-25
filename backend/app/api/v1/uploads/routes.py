"""
File upload API routes.
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Request
from typing import Optional

from app.utils.file_upload import file_upload_service

router = APIRouter()


@router.post("/upload")
async def upload_file(
    request: Request,
    file: UploadFile = File(...),
    type: Optional[str] = "project"
):
    """Upload a file (image) for projects, hackathons, or users."""
    try:
        file_path = await file_upload_service.save_upload_file(file, type)
        relative_url = file_upload_service.get_file_url(file_path)

        # If relative_url is empty (file doesn't exist), construct default
        if not relative_url:
            relative_url = f"/static/uploads/{type}s/{file.filename}"

        return {
            "url": relative_url,
            "filename": file.filename,
            "message": "File uploaded successfully"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"File upload failed: {str(e)}"
        )
