from __future__ import annotations

from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict


class Permission(BaseModel):
    id: int
    code: str
    description: str | None = None
    resource: str
    action: str
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class Role(BaseModel):
    id: int
    name: str
    description: str | None = None
    is_system: bool = True
    created_at: datetime | None = None
    permissions: List[Permission] = []

    model_config = ConfigDict(from_attributes=True)


class UserRoleAssignmentRequest(BaseModel):
    role_ids: List[int]
