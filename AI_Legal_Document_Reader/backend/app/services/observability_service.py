import time
from contextlib import contextmanager
from typing import Iterator

from app.config import get_settings
from app.schemas import ObservabilityEvent

_EVENTS: list[ObservabilityEvent] = []


def record_event(
    event_type: str,
    metadata: dict[str, str | int | float | bool | None],
    duration_ms: float | None = None,
) -> None:
    if not get_settings().observability_enabled:
        return

    _EVENTS.append(
        ObservabilityEvent(
            event_type=event_type,
            duration_ms=duration_ms,
            metadata=metadata,
        )
    )


@contextmanager
def trace_event(
    event_type: str,
    metadata: dict[str, str | int | float | bool | None],
) -> Iterator[None]:
    start = time.perf_counter()
    try:
        yield
    finally:
        duration_ms = (time.perf_counter() - start) * 1000
        record_event(event_type, metadata, duration_ms)


def list_events() -> list[ObservabilityEvent]:
    return list(_EVENTS)


def clear_events() -> None:
    _EVENTS.clear()
