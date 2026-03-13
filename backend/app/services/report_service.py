from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.domain.models.hackathon import Hackathon
from app.domain.models.project import Project
from app.domain.models.report import Report as ReportModel
from app.domain.models.team import Team
from app.domain.schemas.report import Report as ReportSchema, ReportResourceSummary, ReportUpdateRequest
from app.repositories.hackathon_repository import HackathonRepository
from app.repositories.project_repository import ProjectRepository
from app.repositories.report_repository import ReportRepository
from app.repositories.team_repository import TeamRepository


VALID_REPORT_STATUSES = {"pending", "reviewed", "resolved", "dismissed"}


class ReportService:
    def __init__(self):
        self.report_repo = ReportRepository()
        self.hackathon_repo = HackathonRepository()
        self.project_repo = ProjectRepository()
        self.team_repo = TeamRepository()

    def _resource_summary(self, db: Session, resource_type: str, resource_id: int):
        if resource_type == "hackathon":
            hackathon = self.hackathon_repo.get(db, resource_id)
            if not hackathon:
                return None, None
            return hackathon, ReportResourceSummary(
                id=hackathon.id,
                resource_type="hackathon",
                name=hackathon.name,
            )
        if resource_type == "project":
            project = self.project_repo.get(db, resource_id)
            if not project:
                return None, None
            return project, ReportResourceSummary(
                id=project.id,
                resource_type="project",
                name=project.title,
                hackathon_id=project.hackathon_id,
            )
        if resource_type == "team":
            team = self.team_repo.get(db, resource_id)
            if not team:
                return None, None
            return team, ReportResourceSummary(
                id=team.id,
                resource_type="team",
                name=team.name,
                hackathon_id=team.hackathon_id,
            )
        return None, None

    def _to_schema(self, db: Session, report: ReportModel) -> ReportSchema:
        schema = ReportSchema.model_validate(report)
        _, resource = self._resource_summary(db, report.resource_type, report.resource_id)
        schema.resource = resource
        return schema

    def create_report(self, db: Session, *, reporter_id: int, resource_type: str, resource_id: int, reason: str) -> ReportSchema:
        resource, _ = self._resource_summary(db, resource_type, resource_id)
        if not resource:
            raise ValueError(f"{resource_type.capitalize()} not found")

        report = self.report_repo.create(db, obj_in={
            "reporter_id": reporter_id,
            "resource_type": resource_type,
            "resource_id": resource_id,
            "reason": reason.strip(),
            "status": "pending",
        })
        report = self.report_repo.get_with_users(db, report.id) or report
        return self._to_schema(db, report)

    def list_reports_for_resource(self, db: Session, *, resource_type: str, resource_id: int, status: str | None = None, skip: int = 0, limit: int = 100):
        reports = self.report_repo.list_by_resource(
            db,
            resource_type=resource_type,
            resource_id=resource_id,
            status=status,
            skip=skip,
            limit=limit,
        )
        return [self._to_schema(db, report) for report in reports]

    def get_report(self, db: Session, report_id: int):
        report = self.report_repo.get_with_users(db, report_id)
        if not report:
            return None
        return self._to_schema(db, report)

    def get_report_model(self, db: Session, report_id: int):
        return self.report_repo.get_with_users(db, report_id)

    def review_report(self, db: Session, *, report_id: int, reviewer_id: int, update: ReportUpdateRequest):
        report = self.report_repo.get_with_users(db, report_id)
        if not report:
            return None
        if update.status not in VALID_REPORT_STATUSES:
            raise ValueError("Invalid report status")
        report.status = update.status
        report.reviewed_by = reviewer_id
        report.reviewed_at = datetime.now(timezone.utc)
        report.resolution_note = update.resolution_note.strip() if update.resolution_note else None
        db.add(report)
        db.commit()
        db.refresh(report)
        report = self.report_repo.get_with_users(db, report_id) or report
        return self._to_schema(db, report)

    def get_hackathon_for_project(self, db: Session, project_id: int):
        project = self.project_repo.get(db, project_id)
        if not project or not project.hackathon_id:
            return None
        return self.hackathon_repo.get(db, project.hackathon_id)


report_service = ReportService()
