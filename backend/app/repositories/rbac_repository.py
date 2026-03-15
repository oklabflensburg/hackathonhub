from __future__ import annotations

from typing import Iterable, List, Sequence

from sqlalchemy.orm import Session, joinedload

from app.domain.models.rbac import Permission, Role, RolePermission, UserRole


class RoleRepository:
    def get_all(self, db: Session) -> List[Role]:
        return (
            db.query(Role)
            .options(joinedload(Role.permissions))
            .order_by(Role.name)
            .all()
        )

    def get_by_name(self, db: Session, name: str) -> Role | None:
        return (
            db.query(Role)
            .options(joinedload(Role.permissions))
            .filter(Role.name == name)
            .first()
        )

    def get_by_ids(self, db: Session, role_ids: Sequence[int]) -> List[Role]:
        if not role_ids:
            return []
        return (
            db.query(Role)
            .options(joinedload(Role.permissions))
            .filter(Role.id.in_(role_ids))
            .all()
        )


class PermissionRepository:
    def get_all(self, db: Session) -> List[Permission]:
        return db.query(Permission).order_by(Permission.code).all()

    def get_codes_for_user(self, db: Session, user_id: int) -> set[str]:
        rows = (
            db.query(Permission.code)
            .join(RolePermission, RolePermission.permission_id == Permission.id)
            .join(Role, Role.id == RolePermission.role_id)
            .join(UserRole, UserRole.role_id == Role.id)
            .filter(UserRole.user_id == user_id)
            .all()
        )
        return {row[0] for row in rows}


class UserRoleRepository:
    def get_user_roles(self, db: Session, user_id: int) -> List[Role]:
        return (
            db.query(Role)
            .join(UserRole, UserRole.role_id == Role.id)
            .options(joinedload(Role.permissions))
            .filter(UserRole.user_id == user_id)
            .order_by(Role.name)
            .all()
        )

    def set_user_roles(
        self, db: Session, user_id: int, roles: Iterable[Role]
    ) -> List[Role]:
        db.query(UserRole).filter(UserRole.user_id == user_id).delete(
            synchronize_session=False
        )
        role_list = list(roles)
        for role in role_list:
            db.add(UserRole(user_id=user_id, role_id=role.id))
        db.commit()
        return self.get_user_roles(db, user_id)
