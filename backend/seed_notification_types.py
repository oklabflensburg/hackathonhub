#!/usr/bin/env python3
"""
Seed script to populate notification_types table with canonical definitions.

This script should be run after the migration
`20260314_191906_add_notification_type_metadata.py` has been applied.
"""
import sys
import os

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


# Canonical notification definitions - same as original hardcoded definitions
NOTIFICATION_DEFINITIONS = [
    # (type_key, category, default_channels, description,
    #  help_text, help_text_key, email_template)
    ("team_invitation", "team", "email,push,in_app",
     "When you're invited to join a team",
     "Alerts you when another participant invites you to a team.",
     "notifications.help_text.team_invitation", "team/invitation_sent"),
    ("team_invitation_accepted", "team", "email,in_app",
     "When someone accepts your team invitation",
     "Lets you know that an invited member has joined your team.",
     "notifications.help_text.team_invitation_accepted",
     "team/invitation_accepted"),
    ("team_invitation_declined", "team", "email,in_app",
     "When someone declines your team invitation",
     "Informs you when an invitation is declined.",
     "notifications.help_text.team_invitation_declined", None),
    ("team_member_added", "team", "email,push,in_app",
     "When you're added to a team",
     "Notifies you that you were added to a team.",
     "notifications.help_text.team_member_added", "team/member_added"),
    ("team_created", "team", "email,in_app",
     "When a team is created",
     "Confirms team creation and keeps new collaboration spaces visible.",
     "notifications.help_text.team_created", "team/created"),
    ("project_created", "project", "email,push,in_app",
     "When a project is created in your team",
     "Tells you when a new project appears in your team.",
     "notifications.help_text.project_created", "project/created"),
    ("project_commented", "project", "email,push,in_app",
     "When someone comments on your project",
     "Highlights new project discussion and feedback.",
     "notifications.help_text.project_commented", "project/commented"),
    ("hackathon_registered", "hackathon", "email,in_app",
     "When you register for a hackathon",
     "Confirms successful registration for a hackathon.",
     "notifications.help_text.hackathon_registered", "hackathon/registered"),
    ("hackathon_started", "hackathon", "email,push,in_app",
     "When a hackathon starts",
     "Signals the official start of a hackathon.",
     "notifications.help_text.hackathon_started", "hackathon/started"),
    ("hackathon_start_reminder", "hackathon", "email,push",
     "When a hackathon starts soon",
     "Sends a reminder shortly before hackathon kickoff.",
     "notifications.help_text.hackathon_start_reminder", None),
    ("comment_reply", "system", "email,push,in_app",
     "When someone replies to your comment",
     "Keeps threaded conversations visible when someone replies.",
     "notifications.help_text.comment_reply", None),
    ("vote_received", "system", "in_app",
     "When your project receives a vote",
     "Shows engagement with your project inside the app.",
     "notifications.help_text.vote_received", None),
    ("system_announcement", "system", "email,in_app",
     "System announcements and updates",
     "Covers platform-wide announcements and operational updates.",
     "notifications.help_text.system_announcement", None),
    ("security_alert", "system", "email,push",
     "Security alerts and account notifications",
     "Reserved for security-sensitive events that may need action.",
     "notifications.help_text.security_alert", None),
    ("verification_confirmed", "system", "email,in_app",
     "When email verification succeeds",
     "Confirms that your email address was verified.",
     "notifications.help_text.verification_confirmed",
     "verification_confirmed"),
    ("password_reset_confirmed", "system", "email",
     "When a password reset is confirmed",
     "Confirms that a password reset request was completed.",
     "notifications.help_text.password_reset_confirmed",
     "password_reset_confirmed"),
    ("password_changed", "system", "email",
     "When a password changes",
     "Warns you whenever the account password changes.",
     "notifications.help_text.password_changed", "password_changed"),
    ("newsletter_unsubscribed", "system", "email",
     "When newsletter preferences change",
     "Records changes to newsletter communication preferences.",
     "notifications.help_text.newsletter_unsubscribed",
     "newsletter_unsubscribed"),
    ("security_login_new_device", "system", "email,push",
     "When a new device logs in",
     "Notifies you about sign-ins from new devices.",
     "notifications.help_text.security_login_new_device",
     "security_login_new_device"),
    ("settings_changed", "system", "email",
     "When account settings change",
     "Confirms sensitive account setting changes.",
     "notifications.help_text.settings_changed", "settings_changed"),
]


def seed_notification_types():
    """Seed notification_types table with canonical definitions."""
    # Create database engine
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False,
                                bind=engine)

    with SessionLocal() as session:
        # Check if table exists and has any data
        result = session.execute(
            text("SELECT COUNT(*) FROM notification_types")
        )
        count = result.scalar()

        print(f"Found {count} existing notification types in database")

        # Process each definition
        for i, definition in enumerate(NOTIFICATION_DEFINITIONS):
            (type_key, category, channels_str, description,
             help_text, help_text_key, email_template) = definition

            # Check if this type already exists
            result = session.execute(
                text("""SELECT id FROM notification_types
                       WHERE type_key = :key"""),
                {"key": type_key}
            )
            existing = result.fetchone()

            if existing:
                # Update existing record
                session.execute(
                    text("""
                        UPDATE notification_types
                        SET category = :category,
                            default_channels = :channels,
                            description = :description,
                            help_text = :help_text,
                            help_text_key = :help_text_key,
                            email_template = :email_template
                        WHERE type_key = :key
                    """),
                    {
                        "key": type_key,
                        "category": category,
                        "channels": channels_str,
                        "description": description,
                        "help_text": help_text,
                        "help_text_key": help_text_key,
                        "email_template": email_template
                    }
                )
                print(f"✓ Updated: {type_key}")
            else:
                # Insert new record
                session.execute(
                    text("""
                        INSERT INTO notification_types
                        (type_key, category, default_channels, description,
                         help_text, help_text_key, email_template, sort_order)
                        VALUES
                        (:key, :category, :channels, :description,
                         :help_text, :help_text_key, :email_template,
                         :sort_order)
                    """),
                    {
                        "key": type_key,
                        "category": category,
                        "channels": channels_str,
                        "description": description,
                        "help_text": help_text,
                        "help_text_key": help_text_key,
                        "email_template": email_template,
                        "sort_order": i + 1
                    }
                )
                print(f"✓ Inserted: {type_key}")

        session.commit()
        total = len(NOTIFICATION_DEFINITIONS)
        print(f"\nSuccessfully seeded {total} notification types")


if __name__ == "__main__":
    seed_notification_types()