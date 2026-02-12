"""Tests for export utilities."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from eventbrite_extractor.export import export_to_csv, export_to_json
from eventbrite_extractor.models import Event


def _make_events() -> list[Event]:
    """Create sample events for testing."""
    return [
        Event(
            event_id="1",
            title="AI Workshop",
            summary="Learn about AI.",
            start_date="2026-03-01",
            start_time="10:00",
            tags=["Science & Technology"],
            is_free=True,
        ),
        Event(
            event_id="2",
            title="ML Conference",
            summary="Machine learning talks.",
            start_date="2026-03-15",
            start_time="09:00",
            tags=["Conference", "Tech"],
            is_free=False,
            price="50.00",
            currency="USD",
        ),
    ]


class TestExportJson:
    """Tests for JSON export."""

    def test_export_creates_file(self, tmp_path: Path):
        events = _make_events()
        out = tmp_path / "events.json"
        result = export_to_json(events, out)
        assert result == out
        assert out.exists()

    def test_export_json_content(self, tmp_path: Path):
        events = _make_events()
        out = tmp_path / "events.json"
        export_to_json(events, out)

        data = json.loads(out.read_text(encoding="utf-8"))
        assert len(data) == 2
        assert data[0]["event_id"] == "1"
        assert data[0]["title"] == "AI Workshop"
        assert data[1]["price"] == "50.00"

    def test_export_empty_list(self, tmp_path: Path):
        out = tmp_path / "empty.json"
        export_to_json([], out)

        data = json.loads(out.read_text(encoding="utf-8"))
        assert data == []

    def test_export_creates_parent_dirs(self, tmp_path: Path):
        out = tmp_path / "sub" / "dir" / "events.json"
        export_to_json(_make_events(), out)
        assert out.exists()


class TestExportCsv:
    """Tests for CSV export."""

    def test_export_creates_file(self, tmp_path: Path):
        events = _make_events()
        out = tmp_path / "events.csv"
        result = export_to_csv(events, out)
        assert result == out
        assert out.exists()

    def test_export_csv_content(self, tmp_path: Path):
        events = _make_events()
        out = tmp_path / "events.csv"
        export_to_csv(events, out)

        with open(out, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        assert len(rows) == 2
        assert rows[0]["event_id"] == "1"
        assert rows[0]["title"] == "AI Workshop"
        assert rows[1]["price"] == "50.00"

    def test_export_csv_tags_as_string(self, tmp_path: Path):
        events = _make_events()
        out = tmp_path / "events.csv"
        export_to_csv(events, out)

        with open(out, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        assert rows[1]["tags"] == "Conference, Tech"

    def test_export_empty_list(self, tmp_path: Path):
        out = tmp_path / "empty.csv"
        export_to_csv([], out)
        assert out.read_text(encoding="utf-8") == ""
