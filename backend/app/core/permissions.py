from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.core.database import get_db
from app.domain.models.hackathon import Hackathon
from app.domain.models.project import Comment, Project
from app.domain.models.report import Report
from app.domain.models.shared import File
from app.domain.models.team import Team, TeamMember, TeamReport
from app.domain.models.user import User
from app.repositories.rbac_repository import (
    PermissionRepository, UserRoleRepository
)

SYSTEM_ROLE_NAMES = ("user", "moderator", "admin", "superuser")
PERMISSION_CODES = {
    "auth_manage_sessions": "auth:manage_sessions",
    "users_view": "users:view",
    "users_update_self": "users:update_self",
    "users_update_any": "users:update_any",
    "settings_update_self": "settings:update_self",
    "hackathons_create": "hackathons:create",
    "hackathons_update_any": "hackathons:update_any",
    "hackathons_delete_any": "hackathons:delete_any",
    "teams_create": "teams:create",
    "teams_update_any": "teams:update_any",
    "teams_delete_any": "teams:delete_any",
    "team_invitations_create": "team_invitations:create",
    "team_invitations_review": "team_invitations:review",
    "projects_create": "projects:create",
    "projects_update_any": "projects:update_any",
    "projects_delete_any": "projects:delete_any",
    "comments_create": "comments:create",
    "comments_moderate": "comments:moderate",
    "notifications_view_any": "notifications:view_any",
    "notifications_manage": "notifications:manage",
    "uploads_create": "uploads:create",
    "uploads_delete_any": "uploads:delete_any",
    "push_manage_self": "push:manage_self",
    "push_manage_any": "push:manage_any",
    "team_reports_create": "team_reports:create",
    "team_reports_view": "team_reports:view",
    "team_reports_review": "team_reports:review",
    "reports_create": "reports:create",
    "reports_view": "reports:view",
    "reports_review": "reports:review",
    "rbac_view": "rbac:view",
    "rbac_assign_roles": "rbac:assign_roles",
}

ROLE_PERMISSION_MAP = {
    "user": {
        PERMISSION_CODES["users_update_self"],
        PERMISSION_CODES["settings_update_self"],
        PERMISSION_CODES["hackathons_create"],
        PERMISSION_CODES["teams_create"],
        PERMISSION_CODES["projects_create"],
        PERMISSION_CODES["comments_create"],
        PERMISSION_CODES["uploads_create"],
        PERMISSION_CODES["push_manage_self"],
        PERMISSION_CODES["team_reports_create"],
        PERMISSION_CODES["reports_create"],
    },
    "moderator": {
        PERMISSION_CODES["users_view"],
        PERMISSION_CODES["comments_moderate"],
        PERMISSION_CODES["notifications_manage"],
        PERMISSION_CODES["notifications_view_any"],
        PERMISSION_CODES["team_reports_view"],
        PERMISSION_CODES["team_reports_review"],
        PERMISSION_CODES["reports_view"],
        PERMISSION_CODES["reports_review"],
        PERMISSION_CODES["rbac_view"],
    },
    "admin": {
        PERMISSION_CODES["users_view"],
        PERMISSION_CODES["users_update_any"],
        PERMISSION_CODES["hackathons_create"],
        PERMISSION_CODES["hackathons_update_any"],
        PERMISSION_CODES["hackathons_delete_any"],
        PERMISSION_CODES["teams_update_any"],
        PERMISSION_CODES["teams_delete_any"],
        PERMISSION_CODES["team_invitations_create"],
        PERMISSION_CODES["team_invitations_review"],
        PERMISSION_CODES["projects_update_any"],
        PERMISSION_CODES["projects_delete_any"],
        PERMISSION_CODES["comments_moderate"],
        PERMISSION_CODES["notifications_manage"],
        PERMISSION_CODES["notifications_view_any"],
        PERMISSION_CODES["uploads_delete_any"],
        PERMISSION_CODES["push_manage_any"],
        PERMISSION_CODES["team_reports_view"],
        PERMISSION_CODES["team_reports_review"],
        PERMISSION_CODES["reports_view"],
        PERMISSION_CODES["reports_review"],
        PERMISSION_CODES["rbac_view"],
    },
    "superuser": set(PERMISSION_CODES.values()),
}


user_role_repository = UserRoleRepository()
permission_repository = PermissionRepository()


@dataclass
class AccessContext:
    roles: list[str]
    permissions: list[str]

    @property
    def primary_role(self) -> str:
        for role_name in ("superuser", "admin", "moderator", "user"):
            if role_name in self.roles:
                return role_name
        return "user"


def get_user_access_context(db: Session, user: User | None) -> AccessContext:
    if not user:
        return AccessContext(roles=[], permissions=[])
    try:
        roles = user_role_repository.get_user_roles(db, user.id)
        role_names = [role.name for role in roles]
        permission_codes = sorted(
            permission_repository.get_codes_for_user(db, user.id))
        if not role_names:
            role_names = ["user"]
            permission_codes = sorted(ROLE_PERMISSION_MAP["user"])
        return AccessContext(roles=role_names, permissions=permission_codes)
    except Exception:
        return AccessContext(roles=["user"], permissions=sorted(
            ROLE_PERMISSION_MAP["user"]
        ))


def apply_access_context(db: Session, user):
    access = get_user_access_context(db, user)
    if hasattr(user, "roles"):
        user.roles = access.roles
    if hasattr(user, "permissions"):
        user.permissions = access.permissions
    if hasattr(user, "role"):
        user.role = access.primary_role
    return user


def user_has_permission(db: Session, user: User | None, code: str) -> bool:
    if not user:
        return False
    access = get_user_access_context(db, user)
    if "superuser" in access.roles:
        return True
    return code in access.permissions


def require_permission(code: str):
    def dependency(db: Session = Depends(get_db), current_user: User = Depends(
            get_current_user)):
        if not user_has_permission(db, current_user, code):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return current_user
    return dependency


def require_any_permission(codes: Iterable[str]):
    required = tuple(codes)

    def dependency(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ):
        if not any(
            user_has_permission(db, current_user, code) for code in required
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return current_user
    return dependency


def can_manage_hackathon(
    db: Session, user: User | None, hackathon: Hackathon | None
) -> bool:
    if not user or not hackathon:
        return False
    return hackathon.owner_id == user.id or user_has_permission(
        db, user, PERMISSION_CODES["hackathons_update_any"]
    )


def can_delete_hackathon(
    db: Session, user: User | None, hackathon: Hackathon | None
) -> bool:
    if not user or not hackathon:
        return False
    return hackathon.owner_id == user.id or user_has_permission(
        db, user, PERMISSION_CODES["hackathons_delete_any"]
    )


def can_manage_team(
    db: Session, user: User | None, team: Team | None
) -> bool:
    if not user or not team:
        return False
    if team.created_by == user.id or user_has_permission(
        db, user, PERMISSION_CODES["teams_update_any"]
    ):
        return True
    team_member = db.query(TeamMember).filter(
        TeamMember.team_id == team.id, TeamMember.user_id == user.id).first()
    return bool(team_member and team_member.role in {"owner", "admin"})


def can_delete_team(
    db: Session, user: User | None, team: Team | None
) -> bool:
    if not user or not team:
        return False
    if team.created_by == user.id or user_has_permission(
        db, user, PERMISSION_CODES["teams_delete_any"]
    ):
        return True
    return can_manage_team(db, user, team)


def can_manage_project(
    db: Session, user: User | None, project: Project | None
) -> bool:
    if not user or not project:
        return False
    if project.owner_id == user.id:
        return True
    if user_has_permission(db, user, PERMISSION_CODES["projects_update_any"]):
        return True
    if project.team_id:
        team = db.query(Team).filter(Team.id == project.team_id).first()
        if can_manage_team(db, user, team):
            return True
    if project.hackathon_id:
        hackathon = db.query(Hackathon).filter(
            Hackathon.id == project.hackathon_id
        ).first()
        if can_manage_hackathon(db, user, hackathon):
            return True
    return False


def can_delete_project(
    db: Session, user: User | None, project: Project | None
) -> bool:
    if not user or not project:
        return False
    return can_manage_project(db, user, project) or user_has_permission(
        db, user, PERMISSION_CODES["projects_delete_any"]
    )


def can_manage_hackathon_reports(
    db: Session, user: User | None, hackathon_id: int
) -> bool:
    if not user:
        return False
    if user_has_permission(db, user, PERMISSION_CODES["reports_view"]):
        return True
    hackathon = db.query(Hackathon).filter(Hackathon.id == hackathon_id).first()
    return bool(hackathon and hackathon.owner_id == user.id)


def can_manage_project_reports(
    db: Session, user: User | None, project_id: int
) -> bool:
    if not user:
        return False
    if user_has_permission(db, user, PERMISSION_CODES["reports_view"]):
        return True
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        return False
    if project.owner_id == user.id:
        return True
    if project.team_id:
        team = db.query(Team).filter(Team.id == project.team_id).first()
        if can_manage_team(db, user, team):
            return True
    if project.hackathon_id:
        hackathon = db.query(Hackathon).filter(
            Hackathon.id == project.hackathon_id
        ).first()
        if hackathon and hackathon.owner_id == user.id:
            return True
    return False


def can_review_report(
    db: Session, user: User | None, report: Report | None
) -> bool:
    if not user or not report:
        return False
    if user_has_permission(db, user, PERMISSION_CODES["reports_review"]):
        return True
    if report.resource_type == "hackathon":
        hackathon = db.query(Hackathon).filter(
            Hackathon.id == report.resource_id
        ).first()
        return bool(hackathon and hackathon.owner_id == user.id)
    if report.resource_type == "project":
        return can_manage_project_reports(db, user, report.resource_id)
    if report.resource_type == "team":
        team = db.query(Team).filter(Team.id == report.resource_id).first()
        return bool(team and can_manage_team(db, user, team))
    return False


def can_manage_team_reports_for_hackathon(
    db: Session, user: User | None, hackathon_id: int
) -> bool:
    if not user:
        return False
    if user_has_permission(db, user, PERMISSION_CODES["team_reports_view"]):
        return True
    hackathon = db.query(Hackathon).filter(
        Hackathon.id == hackathon_id).first()
    return bool(hackathon and hackathon.owner_id == user.id)


def can_review_team_report(
    db: Session, user: User | None, report: TeamReport | None
) -> bool:
    if not user or not report:
        return False
    if user_has_permission(db, user, PERMISSION_CODES["team_reports_review"]):
        return True
    team = db.query(Team).filter(Team.id == report.team_id).first()
    if not team:
        return False
    hackathon = db.query(Hackathon).filter(
        Hackathon.id == team.hackathon_id
    ).first()
    return bool(hackathon and hackathon.owner_id == user.id)


def can_view_notification(
    db: Session, user: User | None, notification
) -> bool:
    if not user or not notification:
        return False
    return notification.user_id == user.id or user_has_permission(
        db, user, PERMISSION_CODES["notifications_view_any"]
    )


def can_manage_comment(
    db: Session, user: User | None, comment: Comment | None
) -> bool:
    if not user or not comment:
        return False
    return comment.user_id == user.id or user_has_permission(
        db, user, PERMISSION_CODES["comments_moderate"]
    )


def can_manage_upload(
    db: Session, user: User | None, file_obj: File | None
) -> bool:
    if not user or not file_obj:
        return False
    return file_obj.uploaded_by == user.id or user_has_permission(
        db, user, PERMISSION_CODES["uploads_delete_any"]
    )
