"""Tests for the Eventbrite API client."""

from unittest.mock import MagicMock, patch

import pytest

from eventbrite_extractor.client import EventbriteClient

# Sample API response for a single event
SAMPLE_EVENT = {
    "id": "111",
    "name": {"text": "Sample Event"},
    "description": {"text": "A sample event."},
    "start": {"utc": "2026-04-01T10:00:00Z", "timezone": "UTC"},
    "end": {"utc": "2026-04-01T12:00:00Z"},
    "online_event": False,
    "venue": {
        "name": "Test Venue",
        "address": {"city": "Boston", "region": "MA", "country": "US"},
    },
    "organizer": {"name": "Test Org"},
    "url": "https://www.eventbrite.com/e/111",
    "is_free": True,
    "category": {"name": "Technology"},
    "tags": [{"display_name": "python"}],
    "logo": {"url": "https://img.example.com/logo.png"},
    "capacity": 100,
}

SAMPLE_SEARCH_RESPONSE = {
    "events": [SAMPLE_EVENT],
    "pagination": {
        "page_number": 1,
        "page_count": 1,
        "page_size": 50,
        "object_count": 1,
    },
}


class TestEventbriteClient:
    """Tests for the EventbriteClient."""

    def _make_client(self):
        """Create a client with a fake API key."""
        return EventbriteClient(api_key="fake_token")

    @patch("eventbrite_extractor.client.requests.Session")
    def test_search_events_returns_events(self, mock_session_cls):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = SAMPLE_SEARCH_RESPONSE
        mock_response.raise_for_status = MagicMock()

        mock_session = MagicMock()
        mock_session.get.return_value = mock_response
        mock_session_cls.return_value = mock_session

        client = self._make_client()
        client._session = mock_session

        events = client.search_events(keyword="python", location="Boston")
        assert len(events) == 1
        assert events[0].event_id == "111"
        assert events[0].title == "Sample Event"
        assert events[0].location == "Boston, MA, US"

    @patch("eventbrite_extractor.client.requests.Session")
    def test_search_events_deduplicates(self, mock_session_cls):
        """Duplicate events across pages should be deduplicated."""
        response_page = {
            "events": [SAMPLE_EVENT, SAMPLE_EVENT],
            "pagination": {
                "page_number": 1,
                "page_count": 1,
                "page_size": 50,
                "object_count": 2,
            },
        }
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = response_page
        mock_response.raise_for_status = MagicMock()

        mock_session = MagicMock()
        mock_session.get.return_value = mock_response
        mock_session_cls.return_value = mock_session

        client = self._make_client()
        client._session = mock_session

        events = client.search_events(keyword="python")
        assert len(events) == 1

    @patch("eventbrite_extractor.client.requests.Session")
    def test_search_events_empty_response(self, mock_session_cls):
        empty_response = {
            "events": [],
            "pagination": {
                "page_number": 1,
                "page_count": 1,
                "page_size": 50,
                "object_count": 0,
            },
        }
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = empty_response
        mock_response.raise_for_status = MagicMock()

        mock_session = MagicMock()
        mock_session.get.return_value = mock_response
        mock_session_cls.return_value = mock_session

        client = self._make_client()
        client._session = mock_session

        events = client.search_events(keyword="nonexistent")
        assert len(events) == 0

    @patch("eventbrite_extractor.client.requests.Session")
    def test_get_event_by_id(self, mock_session_cls):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = SAMPLE_EVENT
        mock_response.raise_for_status = MagicMock()

        mock_session = MagicMock()
        mock_session.get.return_value = mock_response
        mock_session_cls.return_value = mock_session

        client = self._make_client()
        client._session = mock_session

        event = client.get_event_by_id("111")
        assert event.event_id == "111"
        assert event.title == "Sample Event"

    def test_client_requires_api_key(self):
        with (
            patch.dict("os.environ", {}, clear=True),
            patch(
                "eventbrite_extractor.config.os.getenv",
                return_value=None,
            ),
            pytest.raises(ValueError, match="EVENTBRITE_API_KEY"),
        ):
            EventbriteClient()
