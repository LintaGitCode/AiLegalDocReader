from fastapi import APIRouter

from app.schemas import ObservabilityEvent
from app.services.observability_service import list_events

router = APIRouter(prefix="/api/observability", tags=["observability"])


@router.get("/events", response_model=list[ObservabilityEvent])
def get_observability_events() -> list[ObservabilityEvent]:
    return list_events()
