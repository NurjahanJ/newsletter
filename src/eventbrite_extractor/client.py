"""Eventbrite API client for extracting public event data."""

from __future__ import annotations

import logging
import time

import requests

from eventbrite_extractor.config import (
    BASE_URL,
    DEFAULT_LOCATION,
    DEFAULT_PAGE_SIZE,
    REQUEST_TIMEOUT,
    get_api_key,
)
from eventbrite_extractor.models import Event

logger = logging.getLogger(__name__)


class EventbriteClient:
    """Client for the Eventbrite API v3.

    Handles authentication, event searching, pagination,
    and rate limit retries.
    """

    def __init__(self, api_key: str | None = None):
        """Initialize the client.

        Args:
            api_key: Eventbrite private token. If not provided,
                     reads from the EVENTBRITE_API_KEY env var.
        """
        self._api_key = api_key or get_api_key()
        self._session = requests.Session()
        self._session.headers.update(
            {
                "Authorization": f"Bearer {self._api_key}",
                "Content-Type": "application/json",
            }
        )

    def _request(self, endpoint: str, params: dict | None = None) -> dict:
        """Make a GET request to the Eventbrite API.

        Handles rate limiting with automatic retry.

        Args:
            endpoint: API endpoint path (e.g. "/events/search/").
            params: Query parameters.

        Returns:
            Parsed JSON response as a dict.

        Raises:
            requests.HTTPError: If the request fails after retries.
        """
        url = f"{BASE_URL}{endpoint}"
        max_retries = 3

        for attempt in range(max_retries):
            response = self._session.get(url, params=params, timeout=REQUEST_TIMEOUT)

            if response.status_code == 429:
                wait = int(response.headers.get("Retry-After", 2**attempt))
                logger.warning("Rate limited. Retrying in %d seconds...", wait)
                time.sleep(wait)
                continue

            response.raise_for_status()
            return response.json()

        # Final attempt without catching
        response = self._session.get(url, params=params, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.json()

    def search_events(
        self,
        keyword: str,
        location: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        max_pages: int = 1,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> list[Event]:
        """Search for public events on Eventbrite.

        Args:
            keyword: Search query (e.g. "python", "music").
            location: Location to search near (e.g. "New York").
                      Defaults to DEFAULT_LOCATION from config.
            start_date: Filter events starting after this UTC datetime
                        (ISO 8601 format, e.g. "2026-03-01T00:00:00Z").
            end_date: Filter events starting before this UTC datetime.
            max_pages: Maximum number of pages to fetch (for pagination).
            page_size: Number of results per page (max 50).

        Returns:
            A list of Event objects.
        """
        location = location or DEFAULT_LOCATION

        params: dict = {
            "q": keyword,
            "location.address": location,
            "page_size": min(page_size, 50),
            "expand": "venue,organizer,category,ticket_availability",
        }

        if start_date:
            params["start_date.range_start"] = start_date
        if end_date:
            params["start_date.range_end"] = end_date

        all_events: list[Event] = []
        seen_ids: set[str] = set()

        for page_num in range(1, max_pages + 1):
            params["page"] = page_num
            logger.info("Fetching page %d...", page_num)

            data = self._request("/events/search/", params=params)
            raw_events = data.get("events", [])

            if not raw_events:
                logger.info("No more events found on page %d.", page_num)
                break

            for raw in raw_events:
                event = Event.from_api_response(raw)
                if event.event_id not in seen_ids:
                    seen_ids.add(event.event_id)
                    all_events.append(event)

            # Check if there are more pages
            pagination = data.get("pagination", {})
            if page_num >= pagination.get("page_count", 1):
                logger.info("Reached last page (%d).", page_num)
                break

        logger.info("Extracted %d unique events.", len(all_events))
        return all_events

    def get_event_by_id(self, event_id: str) -> Event:
        """Fetch a single event by its Eventbrite ID.

        Args:
            event_id: The Eventbrite event ID.

        Returns:
            An Event object.
        """
        data = self._request(
            f"/events/{event_id}/",
            params={"expand": "venue,organizer,category,ticket_availability"},
        )
        return Event.from_api_response(data)
