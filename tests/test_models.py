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
        assert event.description is None
        assert event.is_online is False
        assert event.is_free is False
        assert event.tags == []
        assert event.capacity is None

    def test_from_api_response_minimal(self):
        data = {
            "id": "456",
            "name": {"text": "Minimal Event"},
        }
        event = Event.from_api_response(data)
        assert event.event_id == "456"
        assert event.title == "Minimal Event"
        assert event.source_platform == "eventbrite"

    def test_from_api_response_full(self):
        data = {
            "id": "789",
            "name": {"text": "Full Event"},
            "description": {"text": "A full event description."},
            "start": {
                "utc": "2026-03-01T18:00:00Z",
                "timezone": "America/New_York",
            },
            "end": {"utc": "2026-03-01T21:00:00Z"},
            "online_event": False,
            "venue": {
                "name": "Central Park",
                "address": {
                    "city": "New York",
                    "region": "NY",
                    "country": "US",
                },
            },
            "organizer": {"name": "NYC Events Co."},
            "url": "https://www.eventbrite.com/e/789",
            "is_free": False,
            "ticket_availability": {
                "minimum_ticket_price": {
                    "display": "$25.00",
                    "currency": "USD",
                },
            },
            "category": {"name": "Music"},
            "tags": [
                {"display_name": "jazz"},
                {"display_name": "live"},
            ],
            "logo": {"url": "https://img.example.com/logo.png"},
            "capacity": 500,
        }
        event = Event.from_api_response(data)
        assert event.event_id == "789"
        assert event.title == "Full Event"
        assert event.description == "A full event description."
        assert event.start_datetime == "2026-03-01T18:00:00Z"
        assert event.end_datetime == "2026-03-01T21:00:00Z"
        assert event.timezone == "America/New_York"
        assert event.location == "New York, NY, US"
        assert event.venue_name == "Central Park"
        assert event.is_online is False
        assert event.organizer_name == "NYC Events Co."
        assert event.url == "https://www.eventbrite.com/e/789"
        assert event.is_free is False
        assert event.price == "$25.00"
        assert event.currency == "USD"
        assert event.category == "Music"
        assert event.tags == ["jazz", "live"]
        assert event.image_url == "https://img.example.com/logo.png"
        assert event.capacity == 500

    def test_from_api_response_online_event(self):
        data = {
            "id": "100",
            "name": {"text": "Online Workshop"},
            "online_event": True,
        }
        event = Event.from_api_response(data)
        assert event.is_online is True
        assert event.location == "Online"

    def test_from_api_response_free_event(self):
        data = {
            "id": "200",
            "name": {"text": "Free Meetup"},
            "is_free": True,
        }
        event = Event.from_api_response(data)
        assert event.is_free is True
        assert event.price is None

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
        assert len(d) == 19
