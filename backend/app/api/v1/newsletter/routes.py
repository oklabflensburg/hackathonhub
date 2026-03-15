import json
from typing import Any, Optional

from fastapi import APIRouter, Header, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from pydantic import ValidationError

from app.core.database import get_db
from app.domain.schemas.newsletter import (
    NewsletterSubscribeRequest,
    NewsletterUnsubscribeRequest
)
from app.services.newsletter_service import newsletter_service

router = APIRouter()


@router.post("/subscribe")
async def subscribe_to_newsletter(
    request: Request,
    idempotency_key: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """Subscribe to newsletter with atomic duplicate prevention"""
    try:
        payload = await _parse_request_model(request, NewsletterSubscribeRequest)

        # Use the newsletter service to handle subscription
        result = newsletter_service.subscribe(
            db, email=payload.email, source=payload.source
        )

        subscription = result["subscription"]

        return {
            "message": "Successfully subscribed to newsletter",
            "email": subscription.email,
            "source": subscription.source,
            "already_subscribed": result["already_subscribed"],
            "subscribed_at": result["subscribed_at"],
            "welcome_email_sent": result["welcome_email_sent"]
        }
    except Exception as e:
        # Log the error and return a generic error message
        # In production, you'd want more specific error handling
        raise HTTPException(
            status_code=500,
            detail=f"Failed to subscribe to newsletter: {str(e)}"
        )


@router.post("/unsubscribe")
async def unsubscribe_from_newsletter(
    request: Request,
    db: Session = Depends(get_db)
):
    """Unsubscribe from newsletter"""
    payload = await _parse_request_model(request, NewsletterUnsubscribeRequest)
    result = newsletter_service.unsubscribe(db, email=payload.email)

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Email not found in newsletter subscriptions"
        )

    subscription = result["subscription"]

    return {
        "message": "Successfully unsubscribed from newsletter",
        "email": subscription.email,
        "unsubscribed_at": result["unsubscribed_at"]
    }


async def _parse_request_model(
    request: Request,
    model_class: type[NewsletterSubscribeRequest] | type[NewsletterUnsubscribeRequest],
) -> Any:
    try:
        raw_body = await request.body()
        if not raw_body:
            payload: Any = {}
        else:
            payload = json.loads(raw_body)
            if isinstance(payload, str):
                payload = json.loads(payload)
        return model_class.model_validate(payload)
    except (json.JSONDecodeError, ValidationError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
