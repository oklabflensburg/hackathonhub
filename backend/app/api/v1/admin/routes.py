from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.permissions import PERMISSION_CODES, require_permission
from app.domain.schemas.rbac import (
    Permission as PermissionSchema,
    Role as RoleSchema,
    UserRoleAssignmentRequest
)
from app.repositories.rbac_repository import (
    PermissionRepository,
    RoleRepository,
    UserRoleRepository
)
from app.repositories.user_repository import UserRepository
from app.api.openapi_responses import UNAUTHORIZED_RESPONSE

router = APIRouter(responses=UNAUTHORIZED_RESPONSE)
role_repository = RoleRepository()
permission_repository = PermissionRepository()
user_role_repository = UserRoleRepository()
user_repository = UserRepository()


@router.get('/roles', response_model=list[RoleSchema])
async def get_roles(
    db: Session = Depends(get_db),
    current_user=Depends(require_permission(PERMISSION_CODES['rbac_view'])),
):
    return role_repository.get_all(db)


@router.get('/permissions', response_model=list[PermissionSchema])
async def get_permissions(
    db: Session = Depends(get_db),
    current_user=Depends(require_permission(PERMISSION_CODES['rbac_view'])),
):
    return permission_repository.get_all(db)


@router.get('/users/{user_id}/roles', response_model=list[RoleSchema])
async def get_user_roles(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_permission(PERMISSION_CODES['rbac_view'])),
):
    user = user_repository.get(db, user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail='User not found'
        )
    return user_role_repository.get_user_roles(db, user_id)


@router.patch('/users/{user_id}/roles', response_model=list[RoleSchema])
async def set_user_roles(
    user_id: int,
    payload: UserRoleAssignmentRequest,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(PERMISSION_CODES['rbac_assign_roles'])
    ),
):
    user = user_repository.get(db, user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail='User not found'
        )
    roles = role_repository.get_by_ids(db, payload.role_ids)
    if len(roles) != len(set(payload.role_ids)):
        raise HTTPException(
            status_code=400,
            detail='One or more roles do not exist'
        )
    return user_role_repository.set_user_roles(db, user_id, roles)
