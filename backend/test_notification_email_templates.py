from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.utils.jinja2_engine import Jinja2TemplateEngine


ENGINE = Jinja2TemplateEngine()
SNAPSHOT_DIR = Path(__file__).with_name("test_snapshots") / "notification_email_templates"


@pytest.mark.parametrize(
    ("snapshot_name", "template_name", "language", "variables", "expected_subject"),
    [
        (
            "team_invitation_sent_en",
            "team/invitation_sent",
            "en",
            {
                "team_name": "Alpha Team",
                "inviter_name": "Alice",
                "accept_url": "https://example.com/invitations/1",
                "user_name": "Bob",
            },
            "You've been invited to join a team - Hackathon Dashboard",
        ),
        (
            "project_created_de",
            "project/created",
            "de",
            {
                "project_name": "Dashboard",
                "creator_name": "Clara",
                "project_url": "https://example.com/projects/1",
                "user_name": "Dieter",
            },
            "Neues Projekt erstellt - Hackathon Dashboard",
        ),
        (
            "hackathon_registered_en",
            "hackathon/registered",
            "en",
            {
                "hackathon_name": "Hack 2026",
                "user_name": "Erin",
                "hackathon_date": "2026-04-15",
                "hackathon_url": "https://example.com/hackathons/1",
            },
            "You're registered for Hack 2026 - Hackathon Dashboard",
        ),
        (
            "hackathon_start_reminder_de",
            "hackathon/start_reminder",
            "de",
            {
                "hackathon_name": "Hack 2026",
                "user_name": "Franz",
                "start_time": "2026-04-15 09:00",
                "days_until_start": "2",
                "hackathon_dashboard_url": "https://example.com/hackathons/1/dashboard",
            },
            "Hack 2026 startet in 2 Tag(en) - Hackathon Dashboard",
        ),
        (
            "security_login_new_device_en",
            "security_login_new_device",
            "en",
            {
                "user_name": "Grace",
                "login_time": "2026-04-15 09:00",
                "device_info": "Chrome on macOS",
                "location": "Berlin, Germany",
                "ip_address": "127.0.0.1",
            },
            "New device sign-in detected - Hackathon Dashboard",
        ),
    ],
)
def test_notification_email_template_rendering(
    snapshot_name: str,
    template_name: str,
    language: str,
    variables: dict[str, str],
    expected_subject: str,
) -> None:
    rendered = ENGINE.render_email(template_name, language, variables)

    assert rendered["subject"] == expected_subject
    assert rendered["subject"] == _read_snapshot(snapshot_name, "subject")
    assert rendered["text"] == _read_snapshot(snapshot_name, "text")
    assert rendered["html"] == _read_snapshot(snapshot_name, "html")


def test_notification_email_template_validator_report_is_clean() -> None:
    from app.utils.template_registry import TemplateRegistry

    report = TemplateRegistry.validate_template_files()

    assert report["valid"] is True
    assert report["issues"] == []
    assert report["missing_languages"] == []
    assert report["missing_templates"] == []
    assert report["unknown_templates"] == []


def _read_snapshot(snapshot_name: str, extension: str) -> str:
    return (
        SNAPSHOT_DIR / f"{snapshot_name}.{extension}"
    ).read_text(encoding="utf-8").rstrip("\n")
