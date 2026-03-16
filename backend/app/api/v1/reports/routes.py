from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.core.database import get_db
from app.core.permissions import can_review_report
from app.domain.schemas.report import Report, ReportUpdateRequest
from app.services.report_service import report_service
from app.api.openapi_responses import UNAUTHORIZED_RESPONSE

router = APIRouter(responses=UNAUTHORIZED_RESPONSE)


@router.get('/{report_id}', response_model=Report)
async def get_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    report_model = report_service.get_report_model(db, report_id)
    if not report_model:
        raise HTTPException(status_code=404, detail='Report not found')
    if not can_review_report(db, current_user, report_model):
        raise HTTPException(status_code=403, detail='Not authorized to view this report')
    return report_service.get_report(db, report_id)


@router.patch('/{report_id}', response_model=Report)
async def update_report(
    report_id: int,
    payload: ReportUpdateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    report_model = report_service.get_report_model(db, report_id)
    if not report_model:
        raise HTTPException(status_code=404, detail='Report not found')
    if not can_review_report(db, current_user, report_model):
        raise HTTPException(status_code=403, detail='Not authorized to review this report')
    try:
        updated = report_service.review_report(db, report_id=report_id, reviewer_id=current_user.id, update=payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if not updated:
        raise HTTPException(status_code=404, detail='Report not found')
    return updated
