-- Create notification_types table
CREATE TABLE IF NOT EXISTS notification_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    default_email BOOLEAN NOT NULL DEFAULT 1,
    default_push BOOLEAN NOT NULL DEFAULT 1,
    default_in_app BOOLEAN NOT NULL DEFAULT 1,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create user_notification_preferences table
CREATE TABLE IF NOT EXISTS user_notification_preferences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    notification_type_id INTEGER NOT NULL,
    email_enabled BOOLEAN NOT NULL DEFAULT 1,
    push_enabled BOOLEAN NOT NULL DEFAULT 1,
    in_app_enabled BOOLEAN NOT NULL DEFAULT 1,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (notification_type_id) REFERENCES notification_types(id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    UNIQUE(user_id, notification_type_id)
);

-- Create user_notifications table
CREATE TABLE IF NOT EXISTS user_notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    notification_type TEXT NOT NULL,
    title TEXT NOT NULL,
    message TEXT NOT NULL,
    data TEXT, -- JSON stored as TEXT in SQLite
    channels_sent TEXT, -- JSON stored as TEXT in SQLite
    read_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Create push_subscriptions table
CREATE TABLE IF NOT EXISTS push_subscriptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    endpoint TEXT NOT NULL UNIQUE,
    p256dh TEXT NOT NULL,
    auth TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Create indexes for faster queries
CREATE INDEX IF NOT EXISTS ix_user_notifications_user_id ON user_notifications(user_id);
CREATE INDEX IF NOT EXISTS ix_user_notifications_created_at ON user_notifications(created_at);
CREATE INDEX IF NOT EXISTS ix_user_notifications_read_at ON user_notifications(read_at);
CREATE INDEX IF NOT EXISTS ix_user_notification_preferences_user_id ON user_notification_preferences(user_id);
CREATE INDEX IF NOT EXISTS ix_push_subscriptions_user_id ON push_subscriptions(user_id);

-- Insert default notification types
INSERT OR IGNORE INTO notification_types (name, description, default_email, default_push, default_in_app) VALUES
('project_created', 'When a project is created', 1, 1, 1),
('project_commented', 'When someone comments on your project', 1, 1, 1),
('team_invitation', 'When you are invited to a team', 1, 1, 1),
('team_invitation_accepted', 'When someone accepts your team invitation', 1, 1, 1),
('team_member_added', 'When a member is added to your team', 1, 1, 1),
('hackathon_registered', 'When you register for a hackathon', 1, 1, 1),
('hackathon_started', 'When a hackathon you registered for starts', 1, 1, 1),
('password_reset', 'Password reset requests', 1, 0, 0),
('email_verification', 'Email verification requests', 1, 0, 0),
('newsletter_welcome', 'Welcome to newsletter', 1, 0, 0);