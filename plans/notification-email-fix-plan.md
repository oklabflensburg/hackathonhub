# Notification Email Fix Plan

## Problem Analysis
After investigating why notifications are not sending emails, I've identified several critical issues:

### 1. Database Schema Mismatch (CRITICAL)
**Issue**: The database migration (`add_notification_tables.py`) creates tables with an old schema, but the Python code (`models.py`, `notification_service.py`) expects a new schema.

**Migration Schema (OLD)**:
- `notification_types` table with `name` column
- `user_notification_preferences` table with `notification_type_id` foreign key and separate boolean columns (`email_enabled`, `push_enabled`, `in_app_enabled`)

**Python Model Schema (NEW)**:
- `notification_types` table with `type_key` column
- `user_notification_preferences` table with `notification_type` string column and `channel` column

**Impact**: The notification preference service fails when querying preferences, causing notifications to not be sent.

### 2. SMTP Configuration Issues
**Issue**: The `.env` file contains placeholder SMTP credentials. The `email_service.py` returns `True` (success) when SMTP is not configured, masking failures.

**Code Issue** (lines 77-83 in `email_service.py`):
```python
if not self.smtp_user or not self.smtp_password:
    logger.warning("SMTP not configured. Email would be sent to: %s", to_email)
    return True  # Return success in development
```

**Impact**: Emails appear to be sent successfully but are actually just logged.

### 3. Notification Preference System Failure
**Issue**: Due to schema mismatch, `notification_preference_service.should_send_notification()` likely returns `False` or throws exceptions.

**Impact**: Even if SMTP works, notifications are blocked at the preference check level.

### 4. Template Mapping Issues
**Issue**: The notification service has hardcoded template mappings that may not match actual template paths.

## Solution Plan

### Phase 1: Immediate Diagnostic Tests
1. **Run Diagnostic Script**: Create and run a comprehensive test to identify exactly which component is failing.
2. **Check Database Schema**: Verify which schema is actually in the production database.
3. **Test SMTP Connectivity**: Test email service with real credentials.

### Phase 2: Database Schema Fix
**Option A (Recommended)**: Create a new migration to update tables to match Python models:
```sql
-- Update notification_types table
ALTER TABLE notification_types RENAME COLUMN name TO type_key;
ALTER TABLE notification_types ADD COLUMN category VARCHAR(50);
ALTER TABLE notification_types ADD COLUMN default_channels VARCHAR(100);

-- Recreate user_notification_preferences table with new schema
DROP TABLE user_notification_preferences;
CREATE TABLE user_notification_preferences (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    notification_type VARCHAR(50) NOT NULL,
    channel VARCHAR(20) NOT NULL,
    enabled BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, notification_type, channel)
);
```

**Option B**: Update Python code to match existing database schema (less ideal but faster).

### Phase 3: SMTP Configuration Fix
1. **Update Email Service**: Change `email_service.py` to return `False` when SMTP is not configured in production.
2. **Validate Credentials**: Ensure production `.env` file has real SMTP credentials.
3. **Add Configuration Validation**: Add startup check for SMTP configuration.

### Phase 4: Notification Service Fix
1. **Fix Preference Service**: Ensure `notification_preference_service.py` works with correct schema.
2. **Add Error Handling**: Improve error logging and recovery.
3. **Test All Notification Types**: Verify each notification type works end-to-end.

### Phase 5: Monitoring and Validation
1. **Add Notification Logging**: Log all notification attempts with success/failure status.
2. **Create Health Check Endpoint**: Add `/api/health/notifications` endpoint to test notification system.
3. **Add Alerting**: Set up alerts for notification failures.

## Implementation Steps

### Step 1: Create Diagnostic Script
Create `backend/diagnose_notifications.py` to:
1. Test database connectivity and schema
2. Test SMTP configuration and connectivity
3. Test template loading
4. Test notification preference system
5. Send test notification

### Step 2: Fix Database Schema
Based on diagnostic results:
- If database has old schema: Create migration to update to new schema
- If code expects wrong schema: Update Python models to match database

### Step 3: Update Email Service
```python
# In email_service.py, change:
def send_email(...) -> bool:
    # Check if SMTP is configured
    if not self.smtp_user or not self.smtp_password:
        if os.getenv("ENVIRONMENT") == "production":
            logger.error("SMTP not configured in production!")
            return False
        else:
            logger.warning("SMTP not configured in development")
            return True  # Still return True in development
```

### Step 4: Test and Deploy
1. Run comprehensive tests
2. Deploy changes to staging
3. Verify notifications work
4. Deploy to production

## Files to Modify

### Critical Files:
1. `backend/migrations/versions/add_notification_tables.py` - Update migration
2. `backend/email_service.py` - Fix SMTP handling
3. `backend/notification_preference_service.py` - Ensure compatibility
4. `backend/models.py` - Verify model definitions

### New Files to Create:
1. `backend/diagnose_notifications.py` - Diagnostic script
2. `backend/test_notification_integration.py` - Integration tests
3. `backend/notification_monitor.py` - Monitoring utility

## Success Criteria
1. All notification types send emails successfully
2. Database schema matches Python models
3. SMTP configuration validated and working
4. Comprehensive logging of notification attempts
5. Health check endpoint returns "healthy"

## Rollback Plan
1. Keep backup of current database schema
2. Create rollback migration
3. Monitor error rates after deployment
4. Have feature flag to disable new notification system if needed

## Timeline
- **Day 1**: Diagnostic and planning
- **Day 2**: Database schema fixes
- **Day 3**: Code updates and testing
- **Day 4**: Deployment and validation

## Risk Assessment
- **High Risk**: Database schema changes could break existing functionality
- **Medium Risk**: SMTP configuration changes could affect email delivery
- **Low Risk**: Template and logging changes

## Testing Strategy
1. **Unit Tests**: Test individual components
2. **Integration Tests**: Test notification flow end-to-end
3. **Load Tests**: Ensure system handles notification volume
4. **User Acceptance Tests**: Verify notifications work for real users

## Documentation Updates Needed
1. Update `NOTIFICATION_SYSTEM.md` with troubleshooting guide
2. Add SMTP configuration guide
3. Update deployment checklist
4. Add monitoring guide

This plan addresses the root causes of why notifications are not sending emails and provides a clear path to resolution.