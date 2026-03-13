from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session, joinedload

from app.domain.models.report import Report
from app.repositories.base import BaseRepository


class ReportRepository(BaseRepository[Report]):
    def __init__(self):
        super().__init__(Report)

    def _base_query(self, db: Session):
        return db.query(self.model).options(
            joinedload(self.model.reporter),
            joinedload(self.model.reviewer),
        )

    def get_with_users(self, db: Session, report_id: int) -> Optional[Report]:
        return self._base_query(db).filter(self.model.id == report_id).first()

    def list_by_resource(
        self,
        db: Session,
        *,
        resource_type: str,
        resource_id: int,
        status: str | None = None,
        skip: int = 0,
        limit: int = 100,
    ):
        query = self._base_query(db).filter(
            self.model.resource_type == resource_type,
            self.model.resource_id == resource_id,
        )
        if status:
            query = query.filter(self.model.status == status)
        return query.order_by(self.model.created_at.desc()).offset(skip).limit(limit).all()
