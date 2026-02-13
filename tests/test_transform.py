"""Tests for the transform module."""

from __future__ import annotations

from datetime import date

from eventbrite_extractor.models import Event
from eventbrite_extractor.transform import (
    classify_event,
    filter_events,
    format_date_display,
    format_location,
    format_price,
    sort_events,
    transform_events,
)


def _event(**kwargs) -> Event:
    """Create an Event with sensible defaults, overridden by kwargs."""
    defaults = {
        "event_id": "1",
        "title": "AI Workshop",
        "start_date": "2026-03-15",
        "start_time": "10:00",
    }
    defaults.update(kwargs)
    return Event(**defaults)


class TestFilterEvents:
    """Tests for filter_events."""

    def test_removes_cancelled(self):
        events = [_event(), _event(event_id="2", is_cancelled=True)]
        result = filter_events(events, reference_date=date(2026, 1, 1))
        assert len(result) == 1
        assert result[0].event_id == "1"

    def test_keeps_cancelled_when_disabled(self):
        events = [_event(is_cancelled=True)]
        result = filter_events(
            events, remove_cancelled=False, reference_date=date(2026, 1, 1)
        )
        assert len(result) == 1

    def test_removes_past_events(self):
        events = [
            _event(event_id="past", start_date="2025-01-01"),
            _event(event_id="future", start_date="2026-06-01"),
        ]
        result = filter_events(events, reference_date=date(2026, 3, 1))
        assert len(result) == 1
        assert result[0].event_id == "future"

    def test_keeps_past_when_disabled(self):
        events = [_event(start_date="2020-01-01")]
        result = filter_events(
            events, remove_past=False, reference_date=date(2026, 3, 1)
        )
        assert len(result) == 1

    def test_keeps_events_with_no_date(self):
        events = [_event(start_date=None)]
        result = filter_events(events, reference_date=date(2026, 3, 1))
        assert len(result) == 1

    def test_keeps_todays_events(self):
        events = [_event(start_date="2026-03-01")]
        result = filter_events(events, reference_date=date(2026, 3, 1))
        assert len(result) == 1


class TestSortEvents:
    """Tests for sort_events."""

    def test_sort_by_date(self):
        events = [
            _event(event_id="b", start_date="2026-04-01"),
            _event(event_id="a", start_date="2026-03-01"),
        ]
        result = sort_events(events, by="date")
        assert result[0].event_id == "a"
        assert result[1].event_id == "b"

    def test_sort_by_title(self):
        events = [
            _event(event_id="z", title="Zebra Talk"),
            _event(event_id="a", title="AI Workshop"),
        ]
        result = sort_events(events, by="title")
        assert result[0].event_id == "a"
        assert result[1].event_id == "z"

    def test_free_first(self):
        events = [
            _event(event_id="paid", is_free=False, start_date="2026-03-01"),
            _event(event_id="free", is_free=True, start_date="2026-04-01"),
        ]
        result = sort_events(events, by="date", free_first=True)
        assert result[0].event_id == "free"
        assert result[1].event_id == "paid"

    def test_none_dates_sort_last(self):
        events = [
            _event(event_id="none", start_date=None),
            _event(event_id="dated", start_date="2026-03-01"),
        ]
        result = sort_events(events, by="date")
        assert result[0].event_id == "dated"
        assert result[1].event_id == "none"


class TestFormatPrice:
    """Tests for format_price."""

    def test_free_event(self):
        assert format_price(_event(is_free=True)) == "Free"

    def test_priced_event(self):
        result = format_price(_event(price="50.00", currency="USD"))
        assert result == "$50 USD"

    def test_priced_event_with_cents(self):
        result = format_price(_event(price="5.04", currency="USD"))
        assert result == "$5.04 USD"

    def test_zero_price_is_free(self):
        result = format_price(_event(price="0.00", currency="USD"))
        assert result == "Free"

    def test_no_price_shows_paid(self):
        assert format_price(_event(is_free=False, price=None)) == "Paid"

    def test_default_currency(self):
        result = format_price(_event(price="25.00", currency=None))
        assert result == "$25 USD"


class TestFormatDateDisplay:
    """Tests for format_date_display."""

    def test_full_date_and_time(self):
        result = format_date_display(
            _event(start_date="2026-03-04", start_time="10:00")
        )
        assert result == "Wed, Mar 4 at 10:00 AM"

    def test_afternoon_time(self):
        result = format_date_display(
            _event(start_date="2026-03-04", start_time="14:30")
        )
        assert result == "Wed, Mar 4 at 2:30 PM"

    def test_midnight(self):
        result = format_date_display(
            _event(start_date="2026-03-04", start_time="00:00")
        )
        assert result == "Wed, Mar 4 at 12:00 AM"

    def test_date_only(self):
        result = format_date_display(_event(start_date="2026-03-04", start_time=None))
        assert result == "Wed, Mar 4"

    def test_no_date_or_time(self):
        result = format_date_display(_event(start_date=None, start_time=None))
        assert result == "Date TBD"


class TestFormatLocation:
    """Tests for format_location."""

    def test_online(self):
        assert format_location(_event(is_online=True)) == "Online"

    def test_venue(self):
        assert format_location(_event(venue_name="Grand Hall")) == "Grand Hall"

    def test_no_location(self):
        event = _event(is_online=False, venue_name=None)
        assert format_location(event) == "Location TBD"


class TestClassifyEvent:
    """Tests for classify_event."""

    def test_conference(self):
        assert classify_event(_event(title="AI Summit 2026")) == "Conference"

    def test_workshop(self):
        assert classify_event(_event(title="Hands-On AI Workshop")) == "Workshop"

    def test_meetup(self):
        assert classify_event(_event(title="AI Networking Mixer")) == "Meetup"

    def test_webinar(self):
        assert classify_event(_event(title="AI Webinar Series")) == "Webinar"

    def test_hackathon(self):
        assert classify_event(_event(title="AI Hackathon NYC")) == "Hackathon"

    def test_talk(self):
        assert classify_event(_event(title="Keynote: Future of AI")) == "Talk"

    def test_course(self):
        assert classify_event(_event(title="AI Fundamentals Course")) == "Course"

    def test_fallback(self):
        assert classify_event(_event(title="AI and Philosophy")) == "Event"

    def test_uses_summary(self):
        event = _event(title="Something", summary="Join our networking mixer")
        assert classify_event(event) == "Meetup"

    def test_uses_tags(self):
        event = _event(title="Something", tags=["Workshop"])
        assert classify_event(event) == "Workshop"


class TestTransformEvents:
    """Tests for the full transform_events pipeline."""

    def test_full_pipeline(self):
        events = [
            _event(
                event_id="1",
                title="AI Summit",
                start_date="2026-04-01",
                start_time="09:00",
                is_free=True,
            ),
            _event(
                event_id="2",
                title="AI Workshop",
                start_date="2026-03-15",
                start_time="14:00",
                is_free=False,
                price="50.00",
                currency="USD",
            ),
            _event(event_id="3", is_cancelled=True),
        ]
        result = transform_events(events, reference_date=date(2026, 1, 1))

        # Cancelled event filtered out
        assert len(result) == 2

        # Sorted by date — March before April
        assert result[0]["event_id"] == "2"
        assert result[1]["event_id"] == "1"

        # Enriched fields present
        assert result[0]["display_price"] == "$50 USD"
        assert result[0]["display_date"] == "Sun, Mar 15 at 2:00 PM"
        assert result[0]["event_type"] == "Workshop"
        assert result[1]["display_price"] == "Free"
        assert result[1]["event_type"] == "Conference"

    def test_free_first_sorting(self):
        events = [
            _event(event_id="paid", start_date="2026-03-01", is_free=False),
            _event(event_id="free", start_date="2026-04-01", is_free=True),
        ]
        result = transform_events(
            events,
            free_first=True,
            reference_date=date(2026, 1, 1),
        )
        assert result[0]["event_id"] == "free"

    def test_empty_input(self):
        assert transform_events([]) == []
