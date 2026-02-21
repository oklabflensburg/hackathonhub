-- Create notification_types table
CREATE TABLE IF NOT EXISTS notification_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL UNIQUE,
    description VARCHAR,
    default_email BOOLEAN NOT NULL DEFAULT true,
    default_push BOOLEAN NOT NULL DEFAULT true,
    default_in_app BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);

-- Create user_notification_preferences table
CREATE TABLE IF NOT EXISTS user_notification_preferences (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    notification_type_id INTEGER NOT NULL REFERENCES notification_types(id),
    email_enabled BOOLEAN NOT NULL DEFAULT true,
    push_enabled BOOLEAN NOT NULL DEFAULT true,
    in_app_enabled BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    UNIQUE(user_id, notification_type_id)
);

-- Create user_notifications table
CREATE TABLE IF NOT EXISTS user_notifications (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    notification_type VARCHAR NOT NULL,
    title VARCHAR NOT NULL,
    message VARCHAR NOT NULL,
    data JSONB,
    channels_sent JSONB,
    read_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);

-- Create push_subscriptions table
CREATE TABLE IF NOT EXISTS push_subscriptions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    endpoint VARCHAR NOT NULL UNIQUE,
    p256dh VARCHAR NOT NULL,
    auth VARCHAR NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);

-- Create indexes for faster queries
CREATE INDEX IF NOT EXISTS ix_user_notifications_user_id ON user_notifications(user_id);
CREATE INDEX IF NOT EXISTS ix_user_notifications_created_at ON user_notifications(created_at);
CREATE INDEX IF NOT EXISTS ix_user_notifications_read_at ON user_notifications(read_at);
CREATE INDEX IF NOT EXISTS ix_user_notification_preferences_user_id ON user_notification_preferences(user_id);
CREATE INDEX IF NOT EXISTS ix_push_subscriptions_user_id ON push_subscriptions(user_id);

-- Insert default notification types
INSERT INTO notification_types (name, description, default_email, default_push, default_in_app) VALUES
('project_created', 'When a project is created', true, true, true),
('project_commented', 'When someone comments on your project', true, true, true),
('team_invitation', 'When you are invited to a team', true, true, true),
('team_invitation_accepted', 'When someone accepts your team invitation', true, true, true),
('team_member_added', 'When a member is added to your team', true, true, true),
('hackathon_registered', 'When you register for a hackathon', true, true, true),
('hackathon_started', 'When a hackathon you registered for starts', true, true, true),
('password_reset', 'Password reset requests', true, false, false),
('email_verification', 'Email verification requests', true, false, false),
('newsletter_welcome', 'Welcome to newsletter', true, false, false)
ON CONFLICT (name) DO NOTHING;