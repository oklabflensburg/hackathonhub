from __future__ import annotations

from datetime import datetime
from typing import Optional, Literal, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict

if TYPE_CHECKING:
    from .user import PublicUser


ReportResourceType = Literal["team", "hackathon", "project"]
ReportStatus = Literal["pending", "reviewed", "resolved", "dismissed"]


class ReportResourceSummary(BaseModel):
    id: int
    resource_type: ReportResourceType
    name: str
    hackathon_id: Optional[int] = None


class ReportBase(BaseModel):
    reason: str


class ReportCreateRequest(ReportBase):
    pass


class ReportUpdateRequest(BaseModel):
    status: ReportStatus
    resolution_note: Optional[str] = None


class Report(BaseModel):
    id: int
    reporter_id: int
    resource_type: ReportResourceType
    resource_id: int
    reason: str
    status: ReportStatus
    resolution_note: Optional[str] = None
    reviewed_by: Optional[int] = None
    reviewed_at: Optional[datetime] = None
    created_at: datetime
    reporter: Optional["PublicUser"] = None
    reviewer: Optional["PublicUser"] = None
    resource: Optional[ReportResourceSummary] = None

    model_config = ConfigDict(from_attributes=True)
