# Notification System

## Overview

The notification system provides automated email notifications for important user actions in the Hackathon Dashboard. It's designed to keep users informed about team invitations, project updates, and other important events.

## Architecture

The notification system consists of four main components:

1. **Notification Service** (`notification_service.py`) - Core service for sending notifications
2. **Email Templates** (`templates/emails/`) - HTML templates for different notification types
3. **Template Engine** (`template_engine.py`) - Renders templates with i18n support
4. **Push Notification Service** (`push_notification_service.py`) - Handles web push notifications
5. **Integration** - Integrated into existing API endpoints

## Supported Notification Types

### Team Notifications
- **Team Invitation Sent**: Sent to users when they're invited to join a team
- **Team Invitation Accepted**: Sent to inviter when invitation is accepted
- **Team Member Added**: Sent to users when they're added to a team

### Project Notifications
- **Project Created**: Sent to team members when a project is created

### Future Notifications (Planned)
- Project commented
- Hackathon registration
- Hackathon started
- Team created

## Implementation Details

### Notification Service API

The `NotificationService` class provides the following methods:

```python
# Send any notification
send_notification(
    notification_type: str,
    recipient_email: str,
    recipient_name: str,
    language: str = "en",
    variables: Dict[str, Any] = None
) -> bool

# Team-specific notifications
send_team_invitation_notification(
    db: Session,
    invitation_id: int,
    language: str = "en"
) -> bool

send_team_invitation_accepted_notification(
    db: Session,
    invitation_id: int,
    language: str = "en"
) -> bool

send_team_member_added_notification(
    db: Session,
    team_id: int,
    user_id: int,
    added_by_id: int,
    language: str = "en"
) -> bool

# Project notifications
send_project_created_notification(
    db: Session,
    project_id: int,
    language: str = "en",
    recipient_ids: Optional[List[int]] = None
) -> bool
```

### Template Structure

Email templates are organized in the `templates/emails/` directory:

```
templates/emails/
├── base.html                    # Base template with layout
├── team/
│   ├── invitation_sent/
│   │   ├── en.html             # English template
│   │   └── de.html             # German template
│   ├── invitation_accepted/
│   │   └── en.html
│   └── member_added/
│       └── en.html
└── project/
    └── created/
        └── en.html
```

### Template Variables

Each template type accepts specific variables:

**Team Invitation Sent:**
- `team_name`: Name of the team
- `team_description`: Team description
- `hackathon_name`: Name of the hackathon
- `actor_name`: Name of the inviter
- `invitation_url`: URL to view invitation
- `expiration_date`: When invitation expires

**Team Invitation Accepted:**
- `team_name`: Name of the team
- `team_description`: Team description
- `hackathon_name`: Name of the hackathon
- `actor_name`: Name of user who accepted
- `member_role`: Role of new member
- `member_count`: Total team members
- `team_url`: URL to team page

**Team Member Added:**
- `team_name`: Name of the team
- `team_description`: Team description
- `hackathon_name`: Name of the hackathon
- `actor_name`: Name of user who added member
- `member_role`: Role of new member
- `member_count`: Total team members
- `team_url`: URL to team page

**Project Created:**
- `project_title`: Title of the project
- `project_description`: Project description
- `project_technologies`: Technologies used
- `actor_name`: Name of project creator
- `project_url`: URL to project page
- `hackathon_name`: (Optional) Name of hackathon
- `team_name`: (Optional) Name of team

## Integration with Existing Endpoints

The notification system is integrated into the following API endpoints:

### Team Endpoints
1. **Create Team Invitation** (`POST /api/teams/{team_id}/invitations`)
   - Sends notification to invited user
   - Integrated in `main.py` line ~1356

2. **Accept Invitation** (`POST /api/invitations/{invitation_id}/accept`)
   - Sends notification to inviter
   - Integrated in `main.py` line ~1439

3. **Add Team Member** (`POST /api/teams/{team_id}/members`)
   - Sends notification to added user (if not self-joining)
   - Integrated in `main.py` line ~1112

### Project Endpoints
1. **Create Project** (`POST /api/projects`)
   - Sends notification to team members (if project has a team)
   - Integrated in `main.py` line ~120

## Internationalization (i18n)

The notification system supports multiple languages:

1. **English** (default)
2. **German**

Translations are stored in `i18n/translations.py` under the `email` section:

```python
"email": {
    "team_invitation_subject": "You've been invited to join a team...",
    "team_invitation_accepted_subject": "Your team invitation has been accepted...",
    "team_member_added_subject": "You've been added to a team...",
    "project_created_subject": "New project created...",
    "team_invitation_title": "Team Invitation",
    "team_invitation_accepted_title": "Invitation Accepted",
    "team_member_added_title": "Team Member Added",
    "project_created_title": "New Project"
}
```

## Testing

A test script is available at `test_notification_system.py`:

```bash
cd backend
python test_notification_system.py
```

The test script:
1. Creates an in-memory SQLite database
2. Creates test users, hackathon, and team
3. Tests all notification types
4. Tests both English and German notifications

## Configuration

### Email Service
The notification system uses the existing `EmailService` from `email_service.py`. Ensure email configuration is set in environment variables:

```bash
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FROM_EMAIL=noreply@hackathonhub.oklabflensburg.de
```

### Frontend URL
Notifications include links to the frontend. Set the frontend URL:

```bash
FRONTEND_URL=http://localhost:3001
```

### Push Notifications (VAPID Keys)
For web push notifications to work, you need to configure VAPID (Voluntary Application Server Identification) keys. These keys are used to authenticate your server with push services.

Add the following to your `.env` file:

```bash
# Push Notifications (VAPID keys for web push)
# Generate using: python3 generate_vapid_keys.py
VAPID_PRIVATE_KEY=your-vapid-private-key-here
VAPID_PUBLIC_KEY=your-vapid-public-key-here
```

To generate VAPID keys:

1. Run the key generation script:
   ```bash
   cd backend
   python3 generate_vapid_keys.py
   ```

2. Copy the generated keys to your `.env` file

3. Restart your application

The push notification service will automatically load these keys from the environment. If keys are not configured, you'll see the warning: "VAPID keys not configured. Push notifications will not work."

## Error Handling

Notifications are sent asynchronously and errors are logged but don't fail the main request:

```python
try:
    notification_service.send_team_invitation_notification(...)
except Exception as e:
    logger.error(f"Failed to send invitation notification: {e}")
    # Don't fail the request
```

## Adding New Notification Types

To add a new notification type:

1. **Create Template:**
   ```bash
   mkdir -p templates/emails/new_type/
   touch templates/emails/new_type/en.html
   touch templates/emails/new_type/de.html
   ```

2. **Add Translations:**
   Add to `i18n/translations.py`:
   ```python
   "new_type_subject": "Subject for new type...",
   "new_type_title": "Title for new type"
   ```

3. **Update Template Engine:**
   Add to `subject_key_map` and `title_key_map` in `template_engine.py`

4. **Add Notification Method:**
   Add method to `NotificationService` class

5. **Integrate with Endpoint:**
   Call the notification method from relevant API endpoints

## Best Practices

1. **Always include recipient name** in notification variables
2. **Use language from request headers** when available
3. **Don't fail requests** if notifications fail
4. **Log all notification attempts** (success and failure)
5. **Test templates** in both languages
6. **Keep templates responsive** for mobile devices

## Performance Considerations

1. Notifications are sent synchronously but errors don't block requests
2. Consider implementing a queue system for high-volume notifications
3. Template rendering is lightweight and cached
4. Database queries are optimized to fetch only needed data

## Monitoring

Check application logs for notification activity:

```bash
# Successful notifications
Notification sent: team_invitation_sent to user@example.com

# Failed notifications
Failed to send notification: team_invitation_sent to user@example.com
Error sending notification team_invitation_sent: [error details]