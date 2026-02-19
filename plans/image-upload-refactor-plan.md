# Image Upload Refactoring Plan

## Current Problem Analysis

### Current Implementation Issues:
1. **Base64 Blobs in Database**: Images are converted to base64 data URLs using `FileReader.readAsDataURL()` and stored as strings in database fields (`image_path`, `image_url`, `banner_path`)
2. **No Dedicated Upload Endpoint**: Missing proper file upload API endpoints
3. **Database Bloat**: Base64 encoding increases file size by ~33% and stores binary data in text fields
4. **Performance Issues**: Large base64 strings in API responses and database queries

### Affected Components:

#### Frontend:
1. `frontend3/app/pages/create.vue` - Project and hackathon creation with image upload
2. `frontend3/app/components/HackathonEditForm.vue` - Hackathon editing with image upload
3. `frontend3/app/pages/projects/[id]/edit.vue` - Project editing
4. Multiple display components that read `image_path`/`image_url` fields

#### Backend:
1. `backend/models.py` - Database models with `image_path`, `image_url`, `banner_path` fields
2. `backend/schemas.py` - Pydantic schemas
3. `backend/crud.py` - CRUD operations
4. `backend/main.py` - API endpoints

## Recommended Solution: Local Filesystem Storage

### Architecture Overview:
```
Frontend (Vue/Nuxt) → Backend (FastAPI) → Local Filesystem → Database (Paths only)
```

### Key Components:

1. **File Upload Endpoint** (`POST /api/upload`)
   - Accepts multipart/form-data with file
   - Validates file type, size
   - Generates unique filename
   - Saves to configured upload directory
   - Returns file URL/path

2. **File Serving** (Static files)
   - Configure FastAPI to serve static files from upload directory
   - Or use Nginx in production

3. **Database Schema** (No changes needed)
   - Continue using `image_path`, `image_url`, `banner_path` fields
   - Store relative paths (e.g., `/uploads/projects/abc123.jpg`) instead of base64

4. **File Management**
   - Delete old files when records are updated/deleted
   - Cleanup orphaned files

### Directory Structure:
```
/uploads/
├── projects/
│   ├── {project_id}/
│   │   └── {unique_filename}.{ext}
│   └── temp/
├── hackathons/
│   ├── {hackathon_id}/
│   │   └── {unique_filename}.{ext}
│   └── temp/
└── avatars/
    └── {user_id}/
        └── {unique_filename}.{ext}
```

## Implementation Plan

### Phase 1: Backend Infrastructure
1. Create upload directory configuration
2. Implement file upload endpoint with validation
3. Add static file serving
4. Create file utility functions (save, delete, generate paths)

### Phase 2: Frontend Integration
1. Replace `FileReader.readAsDataURL()` with `FormData` upload
2. Update all image upload components to use new endpoint
3. Modify form submissions to send file paths instead of base64

### Phase 3: Database Migration
1. Create migration to handle existing base64 data (convert or clear)
2. Update all CRUD operations to work with file paths

### Phase 4: Cleanup & Optimization
1. Implement file cleanup on delete/update
2. Add image optimization (resize, compress)
3. Add CDN integration option for future scaling

## Technical Specifications

### Backend Changes:

#### New Dependencies:
```python
# requirements.txt additions
python-multipart  # Already in FastAPI
Pillow  # For image processing (optional)
```

#### New File: `backend/file_upload.py`
```python
import os
import uuid
from pathlib import Path
from fastapi import UploadFile, HTTPException
import shutil

class FileUploadService:
    def __init__(self):
        self.upload_dir = Path(os.getenv("UPLOAD_DIR", "./uploads"))
        self.max_file_size = 10 * 1024 * 1024  # 10MB
        self.allowed_extensions = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
        
    async def save_upload_file(self, upload_file: UploadFile, subdirectory: str) -> str:
        # Validate file
        await self._validate_file(upload_file)
        
        # Generate unique filename
        file_ext = Path(upload_file.filename).suffix.lower()
        unique_filename = f"{uuid.uuid4()}{file_ext}"
        
        # Create directory if not exists
        save_dir = self.upload_dir / subdirectory
        save_dir.mkdir(parents=True, exist_ok=True)
        
        # Save file
        file_path = save_dir / unique_filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
        
        # Return relative path for database storage
        return f"/uploads/{subdirectory}/{unique_filename}"
    
    async def _validate_file(self, upload_file: UploadFile):
        # Check file size
        upload_file.file.seek(0, 2)  # Seek to end
        file_size = upload_file.file.tell()
        upload_file.file.seek(0)  # Reset to beginning
        
        if file_size > self.max_file_size:
            raise HTTPException(400, f"File too large. Max size: {self.max_file_size}")
        
        # Check file extension
        file_ext = Path(upload_file.filename).suffix.lower()
        if file_ext not in self.allowed_extensions:
            raise HTTPException(400, f"Invalid file type. Allowed: {self.allowed_extensions}")
```

#### New Endpoint in `backend/main.py`:
```python
@app.post("/api/upload")
async def upload_file(
    file: UploadFile = File(...),
    type: str = Query("project", enum=["project", "hackathon", "avatar"]),
    current_user: schemas.User = Depends(auth.get_current_user)
):
    """Upload a file and return its path"""
    upload_service = FileUploadService()
    file_path = await upload_service.save_upload_file(file, type)
    return {"file_path": file_path, "url": f"/static{file_path}"}
```

#### Static File Serving:
```python
from fastapi.staticfiles import StaticFiles

app.mount("/static", StaticFiles(directory="uploads"), name="static")
```

### Frontend Changes:

#### New Utility: `frontend3/utils/fileUpload.js`
```javascript
export async function uploadFile(file, type = 'project') {
  const formData = new FormData()
  formData.append('file', file)
  
  const response = await $fetch(`/api/upload?type=${type}`, {
    method: 'POST',
    body: formData,
    // Note: Don't set Content-Type header, browser will set it with boundary
  })
  
  return response.file_path
}
```

#### Component Updates:
1. Replace `FileReader.readAsDataURL()` with `uploadFile()`
2. Store returned file path in form data
3. Submit file path instead of base64 string

## Migration Strategy

### For Existing Data:
1. Option A: Clear existing base64 data and require re-upload
2. Option B: Convert base64 to files (more complex)
3. Recommended: Option A for simplicity

### Migration Script:
```python
# migration script to clear base64 data
def clear_base64_images(db: Session):
    # Clear image_path fields containing base64
    projects = db.query(models.Project).all()
    for project in projects:
        if project.image_path and project.image_path.startswith('data:image'):
            project.image_path = None
    
    hackathons = db.query(models.Hackathon).all()
    for hackathon in hackathons:
        if hackathon.image_url and hackathon.image_url.startswith('data:image'):
            hackathon.image_url = None
        if hackathon.banner_path and hackathon.banner_path.startswith('data:image'):
            hackathon.banner_path = None
    
    db.commit()
```

## Security Considerations

1. **File Validation**: Check MIME type, file signatures (not just extensions)
2. **File Size Limits**: Prevent DoS attacks
3. **Filename Sanitization**: Prevent path traversal attacks
4. **Authentication**: Require auth for uploads
5. **Rate Limiting**: Prevent abuse

## Future Enhancements

1. **Cloud Storage**: Easy to switch to S3/GCS by changing `FileUploadService`
2. **Image Processing**: Auto-resize, optimize, generate thumbnails
3. **CDN Integration**: For better performance at scale
4. **File Versioning**: Keep old versions when updating

## Success Metrics

1. **Database Size**: Reduce by removing base64 blobs
2. **API Performance**: Faster response times without base64 in JSON
3. **Upload Success Rate**: Maintain or improve
4. **User Experience**: Seamless transition with better performance