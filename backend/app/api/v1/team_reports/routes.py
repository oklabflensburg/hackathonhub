from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.core.database import get_db
from app.core.permissions import can_review_team_report
from app.domain.schemas.team import TeamReport, TeamReportUpdateRequest
from app.services.team_service import team_service

router = APIRouter()


@router.get('/{report_id}', response_model=TeamReport)
async def get_team_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    report = team_service.get_team_report(db, report_id)
    if not report:
        raise HTTPException(status_code=404, detail='Team report not found')
    if not can_review_team_report(db, current_user, report):
        raise HTTPException(
            status_code=403, detail='Not authorized to view this team report'
        )
    return report


@router.patch('/{report_id}', response_model=TeamReport)
async def update_team_report(
    report_id: int,
    payload: TeamReportUpdateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    report = team_service.get_team_report(db, report_id)
    if not report:
        raise HTTPException(status_code=404, detail='Team report not found')
    if not can_review_team_report(db, current_user, report):
        raise HTTPException(
            status_code=403, detail='Not authorized to review this team report'
        )
    try:
        updated_report = team_service.review_team_report(
            db, report_id, current_user.id, payload
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if not updated_report:
        raise HTTPException(status_code=404, detail='Team report not found')
    return updated_report
