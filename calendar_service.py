"""calendar_service.py

Reads calendar events from a local JSON file (FR-1).
Single responsibility: load, validate, and return event data (NFR-2).
"""

import json
from datetime import datetime
from pathlib import Path

REQUIRED_FIELDS = {"title", "start", "end", "location"}


class CalendarError(Exception):
    """Raised when the calendar file is missing or malformed."""


def load_events(path="calendar.json"):
    """Load events from a JSON calendar file.

    Returns a list of event dicts sorted by start time.
    Raises CalendarError on missing file, bad JSON, or schema violations.
    """
    file_path = Path(path)
    if not file_path.exists():
        raise CalendarError(f"Calendar file not found: {path}")

    try:
        raw = json.loads(file_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise CalendarError(f"Calendar file is not valid JSON: {exc}") from exc

    if not isinstance(raw, list):
        raise CalendarError("Calendar file must contain a JSON list of events.")

    events = []
    for i, event in enumerate(raw):
        missing = REQUIRED_FIELDS - set(event)
        if missing:
            raise CalendarError(
                f"Event {i} is missing required fields: {sorted(missing)}"
            )
        try:
            event["start_dt"] = datetime.fromisoformat(event["start"])
            event["end_dt"] = datetime.fromisoformat(event["end"])
        except ValueError as exc:
            raise CalendarError(
                f"Event '{event.get('title', i)}' has an invalid date: {exc}"
            ) from exc
        events.append(event)

    return sorted(events, key=lambda e: e["start_dt"])


def format_event(event):
    """Return a human-readable one-line summary of an event."""
    start = event["start_dt"].strftime("%a %b %d, %I:%M %p")
    return f"{event['title']} | {start} | {event['location']}"
