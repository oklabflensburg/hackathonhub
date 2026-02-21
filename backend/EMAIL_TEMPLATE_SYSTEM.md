# Email Template System

## Overview

The email template system replaces inline HTML email content in Python code with external template files, providing:
- **Professional separation** of content from code
- **Internationalization (i18n)** support for multiple languages
- **Easy maintenance** through dedicated template files
- **Consistent styling** with a base template

## Architecture

### Directory Structure
```
backend/
├── templates/
│   ├── emails/
│   │   ├── base.html              # Base email template with common structure
│   │   ├── verification/          # Email verification templates
│   │   │   ├── en.html           # English content
│   │   │   ├── de.html           # German content
│   │   │   └── subject.txt       # Subject line (now handled by translations)
│   │   ├── password_reset/       # Password reset templates
│   │   │   ├── en.html
│   │   │   ├── de.html
│   │   │   └── subject.txt
│   │   └── newsletter_welcome/   # Newsletter welcome templates
│   │       ├── en.html
│   │       ├── de.html
│   │       └── subject.txt
└── template_engine.py            # Template rendering engine
```

### Template Engine

The `TemplateEngine` class (`backend/template_engine.py`) provides:
- **Template loading** from filesystem
- **Variable substitution** using `{{ variable_name }}` syntax
- **Language fallback** (e.g., French → English)
- **HTML to text conversion** for plain text emails
- **Integration with i18n system** for subject lines and titles

### Supported Email Types

1. **Email Verification** - Sent during user registration
2. **Password Reset** - Sent when user requests password reset
3. **Newsletter Welcome** - Sent when user subscribes to newsletter

## Usage

### Rendering Emails

```python
from template_engine import template_engine

# Prepare template variables
variables = {
    "user_name": "John Doe",
    "verification_url": "http://example.com/verify?token=abc123",
    "expiration_hours": 24
}

# Render email
email_content = template_engine.render_email(
    template_name="verification",  # or "password_reset", "newsletter_welcome"
    language="en",                 # or "de" for German
    variables=variables
)

# email_content contains:
# {
#     "subject": "Verify Your Email Address - Hackathon Dashboard",
#     "html": "<!DOCTYPE html>...",
#     "text": "Verify Your Email Address..."
# }
```

### Sending Emails

The refactored email functions now accept a `language` parameter:

```python
# Email verification
send_verification_email(
    user_email="user@example.com",
    user_name="John Doe",
    token="abc123",
    language="en"  # Optional, defaults to "en"
)

# Password reset
forgot_password(
    db=session,
    email="user@example.com",
    language="de"  # Optional, defaults to "en"
)

# Newsletter welcome
email_service.send_newsletter_welcome(
    to_email="user@example.com",
    language="en"  # Optional, defaults to "en"
)
```

## Template Variables

Each template type supports specific variables:

### Verification Email
- `{{ user_name }}` - User's name or username
- `{{ verification_url }}` - Full verification URL
- `{{ expiration_hours }}` - Expiration time in hours (default: 24)

### Password Reset Email
- `{{ user_name }}` - User's name or username
- `{{ reset_url }}` - Full password reset URL
- `{{ expiration_hours }}` - Expiration time in hours (default: 1)

### Newsletter Welcome Email
- `{{ unsubscribe_url }}` - Unsubscribe URL (placeholder)

## Internationalization

### Translation Files
Email subject lines and titles are managed in `backend/i18n/translations.py`:

```python
TRANSLATIONS = {
    "en": {
        "email": {
            "verification_subject": "Verify Your Email Address - Hackathon Dashboard",
            "password_reset_subject": "Reset Your Password - Hackathon Dashboard",
            "newsletter_welcome_subject": "Welcome to Hackathon Hub Newsletter!",
            # ... titles
        }
    },
    "de": {
        "email": {
            "verification_subject": "Bestätigen Sie Ihre E-Mail-Adresse - Hackathon Dashboard",
            # ... German translations
        }
    }
}
```

### Language Detection
Currently, language must be passed explicitly to email functions. Future improvements could:
- Detect language from user preferences
- Use Accept-Language header from HTTP requests
- Store user language preference in database

## Template Syntax

### HTML Templates
Templates use simple variable substitution:
```html
<p>Hello {{ user_name }},</p>
<p>Click <a href="{{ verification_url }}">here</a> to verify.</p>
```

### Base Template
All emails use `base.html` which provides:
- Consistent header/footer
- Responsive design
- Brand styling
- Language attribute (`lang="{{ lang }}"`)

## Migration from Inline HTML

### Before (Old way - inline HTML in Python):
```python
html_content = f"""
<!DOCTYPE html>
<html>
<body>
    <p>Hello {user_name},</p>
    <p>Click <a href="{verification_url}">here</a> to verify.</p>
</body>
</html>
"""
```

### After (New way - using templates):
```python
# Template file: templates/emails/verification/en.html
<p>Hello {{ user_name }},</p>
<p>Click <a href="{{ verification_url }}">here</a> to verify.</p>

# Python code
variables = {"user_name": user_name, "verification_url": verification_url}
email_content = template_engine.render_email("verification", "en", variables)
```

## Benefits

1. **Separation of Concerns**: HTML/CSS separated from Python logic
2. **Easier Maintenance**: Update email content without touching code
3. **Internationalization**: Support multiple languages easily
4. **Consistency**: All emails use same base template
5. **Testing**: Templates can be tested independently
6. **Collaboration**: Designers can work on templates without Python knowledge

## Future Improvements

1. **Template Caching**: Cache loaded templates for performance
2. **More Template Variables**: Add support for more dynamic content
3. **Template Inheritance**: Support nested template inheritance
4. **Template Validation**: Validate template syntax on load
5. **Email Preview**: Web interface to preview templates
6. **Template Variables Documentation**: Auto-generated docs for available variables

## Files Modified

1. `backend/template_engine.py` - New template engine
2. `backend/email_verification.py` - Updated to use templates
3. `backend/email_auth.py` - Updated to use templates
4. `backend/email_service.py` - Updated to use templates
5. `backend/i18n/translations.py` - Added email translations
6. `backend/templates/emails/` - All template files
7. `backend/test_template_engine.py` - Test script for templates

## Testing

Run the test script to verify template rendering:
```bash
cd backend
python test_template_engine.py
```

The test will verify:
- All template types render correctly
- Language support (English and German)
- Fallback to English for unsupported languages
- Variable substitution works properly