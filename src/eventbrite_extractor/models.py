"""Data models for structured event records."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Event:
    """Structured representation of an Eventbrite event.

    Maps to the destination/search API response format.
    """

    event_id: str
    title: str
    summary: str | None = None
    start_date: str | None = None
    start_time: str | None = None
    end_date: str | None = None
    end_time: str | None = None
    timezone: str | None = None
    is_online: bool = False
    venue_name: str | None = None
    venue_address: str | None = None
    organizer_name: str | None = None
    organizer_id: str | None = None
    url: str | None = None
    is_free: bool = False
    price: str | None = None
    currency: str | None = None
    category: str | None = None
    tags: list[str] = field(default_factory=list)
    image_url: str | None = None
    is_cancelled: bool = False
    published: str | None = None
    source_platform: str = "eventbrite"

    @classmethod
    def from_api_response(cls, data: dict) -> Event:
        """Create an Event from a destination/search API result dict.

        Args:
            data: A single event dict from the Eventbrite
                  destination/search API response.

        Returns:
            An Event instance with fields populated from the API data.
        """
        # Ticket availability (present when expanded)
        ticket_info = data.get("ticket_availability", {})
        is_free = ticket_info.get("is_free", False)
        price = None
        currency = None
        if not is_free and ticket_info:
            min_price = ticket_info.get("minimum_ticket_price", {})
            if min_price:
                price = min_price.get("major_value")
                currency = min_price.get("currency")

        # Organizer (present when expanded)
        organizer = data.get("primary_organizer", {})

        # Venue (present when expanded)
        venue = data.get("primary_venue", {})
        venue_address = None
        if venue:
            addr = venue.get("address", {})
            parts = [
                addr.get("city"),
                addr.get("region"),
                addr.get("country"),
            ]
            venue_address = ", ".join(p for p in parts if p) or None

        # Image (present when expanded)
        image = data.get("image", {})

        # Tags — extract display names
        tags = [
            tag.get("display_name", "")
            for tag in data.get("tags", [])
            if tag.get("display_name")
        ]

        # Category — first tag with prefix "EventbriteCategory"
        category = None
        for tag in data.get("tags", []):
            if tag.get("prefix") == "EventbriteCategory":
                category = tag.get("display_name")
                break

        return cls(
            event_id=data.get("id", ""),
            title=data.get("name", ""),
            summary=data.get("summary"),
            start_date=data.get("start_date"),
            start_time=data.get("start_time"),
            end_date=data.get("end_date"),
            end_time=data.get("end_time"),
            timezone=data.get("timezone"),
            is_online=data.get("is_online_event", False),
            venue_name=venue.get("name") if venue else None,
            venue_address=venue_address,
            organizer_name=(organizer.get("name") if organizer else None),
            organizer_id=(organizer.get("id") if organizer else None),
            url=data.get("url"),
            is_free=is_free,
            price=price,
            currency=currency,
            category=category,
            tags=tags,
            image_url=image.get("url") if image else None,
            is_cancelled=bool(data.get("is_cancelled")),
            published=data.get("published"),
        )

    def to_dict(self) -> dict:
        """Convert the Event to a plain dictionary."""
        return {
            "event_id": self.event_id,
            "title": self.title,
            "summary": self.summary,
            "start_date": self.start_date,
            "start_time": self.start_time,
            "end_date": self.end_date,
            "end_time": self.end_time,
            "timezone": self.timezone,
            "is_online": self.is_online,
            "venue_name": self.venue_name,
            "venue_address": self.venue_address,
            "organizer_name": self.organizer_name,
            "organizer_id": self.organizer_id,
            "url": self.url,
            "is_free": self.is_free,
            "price": self.price,
            "currency": self.currency,
            "category": self.category,
            "tags": self.tags,
            "image_url": self.image_url,
            "is_cancelled": self.is_cancelled,
            "published": self.published,
            "source_platform": self.source_platform,
        }
