-- Add user_agent column to push_subscriptions table
ALTER TABLE push_subscriptions ADD COLUMN user_agent TEXT;

-- If you need to rollback:
-- ALTER TABLE push_subscriptions DROP COLUMN user_agent;