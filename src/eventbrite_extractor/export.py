"""Export utilities for JSON and CSV output."""

from __future__ import annotations

import csv
import json
import logging
from pathlib import Path

from eventbrite_extractor.models import Event

logger = logging.getLogger(__name__)


def export_to_json(
    events: list[Event],
    filepath: str | Path,
    indent: int = 2,
) -> Path:
    """Export a list of events to a JSON file.

    Args:
        events: List of Event objects to export.
        filepath: Output file path.
        indent: JSON indentation level.

    Returns:
        The Path to the written file.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    data = [event.to_dict() for event in events]
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)

    logger.info("Exported %d events to %s", len(events), filepath)
    return filepath


def export_to_csv(
    events: list[Event],
    filepath: str | Path,
) -> Path:
    """Export a list of events to a CSV file.

    Args:
        events: List of Event objects to export.
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

    fieldnames = list(events[0].to_dict().keys())

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for event in events:
            row = event.to_dict()
            # Convert list fields to comma-separated strings for CSV
            row["tags"] = ", ".join(row.get("tags", []))
            writer.writerow(row)

    logger.info("Exported %d events to %s", len(events), filepath)
    return filepath
