"""Export utilities for JSON and CSV output."""

from __future__ import annotations

import csv
import json
import logging
from pathlib import Path
from typing import Union

from eventbrite_extractor.models import Event

logger = logging.getLogger(__name__)

# Accept either Event objects or plain dicts (enriched data from transform)
EventData = Union[Event, dict]


def _to_dict(item: EventData) -> dict:
    """Normalise an Event or dict to a plain dictionary."""
    return item.to_dict() if isinstance(item, Event) else item


def export_to_json(
    events: list[EventData],
    filepath: str | Path,
    indent: int = 2,
) -> Path:
    """Export a list of events to a JSON file.

    Args:
        events: List of Event objects or enriched dicts.
        filepath: Output file path.
        indent: JSON indentation level.

    Returns:
        The Path to the written file.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    data = [_to_dict(event) for event in events]
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)

    logger.info("Exported %d events to %s", len(events), filepath)
    return filepath


def export_to_csv(
    events: list[EventData],
    filepath: str | Path,
) -> Path:
    """Export a list of events to a CSV file.

    Args:
        events: List of Event objects or enriched dicts.
        filepath: Output file path.

    Returns:
        The Path to the written file.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    if not events:
        logger.warning("No events to export.")
        filepath.write_text("", encoding="utf-8")
        return filepath

    rows = [_to_dict(event) for event in events]
    fieldnames = list(rows[0].keys())

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            # Convert any list values to comma-separated strings for CSV
            row = {
                k: (", ".join(v) if isinstance(v, list) else v) for k, v in row.items()
            }
            writer.writerow(row)

    logger.info("Exported %d events to %s", len(events), filepath)
    return filepath
