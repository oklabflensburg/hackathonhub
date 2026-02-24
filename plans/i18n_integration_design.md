# i18n Integration Design for Error Messages

## Current i18n Architecture

### 1. Translation System
- **File**: `backend/app/i18n/translations.py`
- **Structure**: Nested dictionary with `locale` → `category` → `key` → `translation`
- **Access function**: `get_translation(key: str, locale: str = "en", **kwargs)`

### 2. Middleware
- **File**: `backend/app/i18n/middleware.py`
- **Function**: `get_locale(request)` extracts locale from `Accept-Language` header
- **Middleware**: `LocaleMiddleware` adds locale to request state
- **Accessor**: `get_locale_from_request(request)` retrieves locale from state

## Design Approaches

### Approach 1: Direct Translation in Each HTTPException

**Pros**:
- Simple and explicit
- Easy to understand
- No additional abstraction

**Cons**:
- Repetitive code
- Hard to maintain consistency
- Requires request object in every function

**Example**:
```python
from app.i18n.translations import get_translation
from app.i18n.middleware import get_locale_from_request

@router.get("/{project_id}")
async def get_project(project_id: int, request: Request, db: Session = Depends(get_db)):
    project = project_service.get_project(db, project_id)
    if not project:
        locale = get_locale_from_request(request)
        detail = get_translation("errors.project_not_found", locale)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
    return project
```

### Approach 2: Dependency Injection Pattern

**Pros**:
- Cleaner function signatures
- Centralized locale handling
- Follows FastAPI patterns

**Cons**:
- Requires modifying all route functions
- More complex setup

**Example**:
```python
from fastapi import Depends
from app.i18n.middleware import get_locale_from_request

async def get_current_locale(request: Request) -> str:
    return get_locale_from_request(request)

@router.get("/{project_id}")
async def get_project(
    project_id: int, 
    db: Session = Depends(get_db),
    locale: str = Depends(get_current_locale)
):
    project = project_service.get_project(db, project_id)
    if not project:
        detail = get_translation("errors.project_not_found", locale)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
    return project
```

### Approach 3: Helper Function Library

**Pros**:
- DRY (Don't Repeat Yourself)
- Consistent error handling
- Easy to test and maintain

**Cons**:
- Additional abstraction layer
- Learning curve for new developers

**Example**:
```python
# i18n_helpers.py
from app.i18n.translations import get_translation

def raise_not_found(locale: str, entity: str, **kwargs):
    detail = get_translation(f"errors.{entity}_not_found", locale, **kwargs)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

def raise_forbidden(locale: str, action: str, **kwargs):
    detail = get_translation(f"errors.forbidden_{action}", locale, **kwargs)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=detail)

# Usage
@router.get("/{project_id}")
async def get_project(
    project_id: int, 
    db: Session = Depends(get_db),
    locale: str = Depends(get_current_locale)
):
    project = project_service.get_project(db, project_id)
    if not project:
        raise_not_found(locale, "project")
    return project
```

### Approach 4: Custom HTTPException Class

**Pros**:
- Most elegant solution
- Full control over exception behavior
- Can integrate with FastAPI error handlers

**Cons**:
- Most complex to implement
- Requires understanding of FastAPI exception handling

**Example**:
```python
# i18n_exceptions.py
from fastapi import HTTPException, status
from app.i18n.translations import get_translation

class I18nHTTPException(HTTPException):
    def __init__(self, locale: str, status_code: int, translation_key: str, **kwargs):
        detail = get_translation(translation_key, locale, **kwargs)
        super().__init__(status_code=status_code, detail=detail)

# Usage
@router.get("/{project_id}")
async def get_project(
    project_id: int, 
    db: Session = Depends(get_db),
    locale: str = Depends(get_current_locale)
):
    project = project_service.get_project(db, project_id)
    if not project:
        raise I18nHTTPException(
            locale=locale,
            status_code=status.HTTP_404_NOT_FOUND,
            translation_key="errors.project_not_found"
        )
    return project
```

## Recommended Approach: Hybrid Solution

Given the existing codebase and the need for gradual migration, I recommend:

### Phase 1: Basic Helper Functions
Create simple helper functions that can be used immediately:
```python
# app/i18n/helpers.py
from fastapi import HTTPException, status
from .translations import get_translation

def raise_i18n_http_exception(
    locale: str, 
    status_code: int, 
    translation_key: str,
    **kwargs
) -> None:
    """Raise an HTTPException with i18n support."""
    detail = get_translation(translation_key, locale, **kwargs)
    raise HTTPException(status_code=status_code, detail=detail)

# Common shortcuts
def raise_not_found(locale: str, entity: str, **kwargs):
    return raise_i18n_http_exception(
        locale, status.HTTP_404_NOT_FOUND, f"errors.{entity}_not_found", **kwargs
    )

def raise_forbidden(locale: str, action: str = "default", **kwargs):
    key = f"errors.forbidden_{action}" if action != "default" else "errors.forbidden"
    return raise_i18n_http_exception(
        locale, status.HTTP_403_FORBIDDEN, key, **kwargs
    )
```

### Phase 2: Locale Dependency
Add locale dependency to route functions:
```python
# app/i18n/dependencies.py
from fastapi import Request, Depends
from .middleware import get_locale_from_request

async def get_locale(request: Request) -> str:
    """Dependency to get locale from request."""
    return get_locale_from_request(request)
```

### Phase 3: Update Route Functions
Update route functions to include locale dependency and use helpers:
```python
from app.i18n.dependencies import get_locale
from app.i18n.helpers import raise_not_found

@router.get("/{project_id}")
async def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    locale: str = Depends(get_locale)
):
    project = project_service.get_project(db, project_id)
    if not project:
        raise_not_found(locale, "project")
    return project
```

### Phase 4: Service Layer Integration
For services that raise HTTPExceptions, pass locale as parameter:
```python
# In service layer
def get_project_service(db: Session, project_id: int, locale: str = "en"):
    project = project_repository.get(db, project_id)
    if not project:
        from app.i18n.helpers import raise_not_found
        raise_not_found(locale, "project")
    return project
```

## Translation Key Naming Convention

### Error Categories
- `errors.{entity}_not_found` - Entity not found (project, user, team, etc.)
- `errors.forbidden_{action}` - Permission denied for specific action
- `errors.unauthorized_{reason}` - Authentication failure reasons
- `errors.validation_{field}` - Field validation errors
- `errors.server_{component}` - Server-side errors by component

### Parameterized Translations
For dynamic content:
```python
# Translation dictionary
"file_too_large": "File too large. Max size is {max_size}MB"

# Usage
detail = get_translation("errors.file_too_large", locale, max_size=10)
```

## Migration Strategy

1. **Add missing translations** to `translations.py` for all existing error messages
2. **Create helper module** with basic i18n support functions
3. **Update one route file at a time** starting with high-impact files
4. **Add locale dependency** to updated routes
5. **Test each updated route** with different Accept-Language headers
6. **Update service layer** functions that raise HTTPExceptions
7. **Add i18n middleware** to main app if not already present

## Testing Considerations
- Test with `Accept-Language: en` header
- Test with `Accept-Language: de` header
- Test with no header (should default to English)
- Test with unsupported language (should fallback to English)
- Test parameterized translations with different values