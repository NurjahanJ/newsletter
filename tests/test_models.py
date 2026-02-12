"""Tests for event data models."""

from eventbrite_extractor.models import Event


class TestEvent:
    """Tests for the Event dataclass."""

    def test_create_event_with_required_fields(self):
        event = Event(event_id="123", title="Test Event")
        assert event.event_id == "123"
        assert event.title == "Test Event"
        assert event.source_platform == "eventbrite"

    def test_default_values(self):
        event = Event(event_id="1", title="E")
        assert event.summary is None
        assert event.is_online is False
        assert event.is_free is False
        assert event.is_cancelled is False
        assert event.tags == []

    def test_from_api_response_minimal(self):
        data = {
            "id": "456",
            "name": "Minimal Event",
        }
        event = Event.from_api_response(data)
        assert event.event_id == "456"
        assert event.title == "Minimal Event"
        assert event.source_platform == "eventbrite"

    def test_from_api_response_full(self):
        data = {
            "id": "789",
            "name": "AI Conference 2026",
            "summary": "A conference about AI.",
            "start_date": "2026-03-01",
            "start_time": "10:00",
            "end_date": "2026-03-01",
            "end_time": "17:00",
            "timezone": "America/New_York",
            "is_online_event": False,
            "primary_venue": {
                "name": "Convention Center",
                "address": {
                    "city": "New York",
                    "region": "NY",
                    "country": "US",
                },
            },
            "primary_organizer": {
                "name": "AI Events Co.",
                "id": "org123",
            },
            "url": "https://www.eventbrite.com/e/789",
            "ticket_availability": {
                "is_free": False,
                "minimum_ticket_price": {
                    "major_value": "25.00",
                    "currency": "USD",
                },
                "has_available_tickets": True,
                "is_sold_out": False,
            },
            "tags": [
                {
                    "prefix": "EventbriteCategory",
                    "tag": "EventbriteCategory/102",
                    "display_name": "Science & Technology",
                },
                {
                    "prefix": "EventbriteFormat",
                    "tag": "EventbriteFormat/1",
                    "display_name": "Conference",
                },
            ],
            "image": {
                "url": "https://img.example.com/logo.png",
            },
            "published": "2026-01-15T10:00:00Z",
        }
        event = Event.from_api_response(data)
        assert event.event_id == "789"
        assert event.title == "AI Conference 2026"
        assert event.summary == "A conference about AI."
        assert event.start_date == "2026-03-01"
        assert event.start_time == "10:00"
        assert event.end_date == "2026-03-01"
        assert event.end_time == "17:00"
        assert event.timezone == "America/New_York"
        assert event.is_online is False
        assert event.venue_name == "Convention Center"
        assert event.venue_address == "New York, NY, US"
        assert event.organizer_name == "AI Events Co."
        assert event.organizer_id == "org123"
        assert event.url == "https://www.eventbrite.com/e/789"
        assert event.is_free is False
        assert event.price == "25.00"
        assert event.currency == "USD"
        assert event.category == "Science & Technology"
        assert event.tags == ["Science & Technology", "Conference"]
        assert event.image_url == "https://img.example.com/logo.png"
        assert event.published == "2026-01-15T10:00:00Z"

    def test_from_api_response_online_event(self):
        data = {
            "id": "100",
            "name": "Online Workshop",
            "is_online_event": True,
        }
        event = Event.from_api_response(data)
        assert event.is_online is True

    def test_from_api_response_free_event(self):
        data = {
            "id": "200",
            "name": "Free Meetup",
            "ticket_availability": {
                "is_free": True,
                "has_available_tickets": True,
            },
        }
        event = Event.from_api_response(data)
        assert event.is_free is True
        assert event.price is None

    def test_from_api_response_cancelled_event(self):
        data = {
            "id": "300",
            "name": "Cancelled Event",
            "is_cancelled": True,
        }
        event = Event.from_api_response(data)
        assert event.is_cancelled is True

    def test_category_extracted_from_tags(self):
        data = {
            "id": "400",
            "name": "Tagged Event",
            "tags": [
                {
                    "prefix": "EventbriteSubCategory",
                    "display_name": "High Tech",
                },
                {
                    "prefix": "EventbriteCategory",
                    "display_name": "Science & Technology",
                },
            ],
        }
        event = Event.from_api_response(data)
        assert event.category == "Science & Technology"
        assert "High Tech" in event.tags
        assert "Science & Technology" in event.tags

    def test_to_dict(self):
        event = Event(
            event_id="1",
            title="Dict Test",
            tags=["a", "b"],
        )
        d = event.to_dict()
        assert isinstance(d, dict)
        assert d["event_id"] == "1"
        assert d["title"] == "Dict Test"
        assert d["tags"] == ["a", "b"]
        assert d["source_platform"] == "eventbrite"
        assert "event_id" in d
        assert len(d) == 23
