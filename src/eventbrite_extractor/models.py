"""Data models for structured event records."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Event:
    """Structured representation of an Eventbrite event."""

    event_id: str
    title: str
    description: str | None = None
    start_datetime: str | None = None
    end_datetime: str | None = None
    timezone: str | None = None
    location: str | None = None
    venue_name: str | None = None
    is_online: bool = False
    organizer_name: str | None = None
    url: str | None = None
    is_free: bool = False
    price: str | None = None
    currency: str | None = None
    category: str | None = None
    tags: list[str] = field(default_factory=list)
    image_url: str | None = None
    capacity: int | None = None
    source_platform: str = "eventbrite"

    @classmethod
    def from_api_response(cls, data: dict) -> Event:
        """Create an Event from a raw Eventbrite API response dict.

        Args:
            data: A single event dict from the Eventbrite API.

        Returns:
            An Event instance with fields populated from the API data.
        """
        start = data.get("start", {})
        end = data.get("end", {})
        venue = data.get("venue", {})
        organizer = data.get("organizer", {})
        logo = data.get("logo", {})
        ticket_availability = data.get("ticket_availability", {})

        # Determine location string
        if data.get("online_event"):
            location = "Online"
        elif venue:
            address = venue.get("address", {})
            parts = [
                address.get("city"),
                address.get("region"),
                address.get("country"),
            ]
            location = ", ".join(p for p in parts if p) or None
        else:
            location = None

        # Determine pricing
        is_free = data.get("is_free", False)
        price = None
        currency = None
        if not is_free and ticket_availability:
            min_price = ticket_availability.get("minimum_ticket_price", {})
            if min_price:
                price = min_price.get("display")
                currency = min_price.get("currency")

        return cls(
            event_id=data.get("id", ""),
            title=data.get("name", {}).get("text", ""),
            description=data.get("description", {}).get("text", ""),
            start_datetime=start.get("utc"),
            end_datetime=end.get("utc"),
            timezone=start.get("timezone"),
            location=location,
            venue_name=venue.get("name") if venue else None,
            is_online=data.get("online_event", False),
            organizer_name=organizer.get("name") if organizer else None,
            url=data.get("url"),
            is_free=is_free,
            price=price,
            currency=currency,
            category=(
                data.get("category", {}).get("name") if data.get("category") else None
            ),
            tags=[
                tag.get("display_name", "")
                for tag in data.get("tags", [])
                if tag.get("display_name")
            ],
            image_url=logo.get("url") if logo else None,
            capacity=data.get("capacity"),
        )

    def to_dict(self) -> dict:
        """Convert the Event to a plain dictionary."""
        return {
            "event_id": self.event_id,
            "title": self.title,
            "description": self.description,
            "start_datetime": self.start_datetime,
            "end_datetime": self.end_datetime,
            "timezone": self.timezone,
            "location": self.location,
            "venue_name": self.venue_name,
            "is_online": self.is_online,
            "organizer_name": self.organizer_name,
            "url": self.url,
            "is_free": self.is_free,
            "price": self.price,
            "currency": self.currency,
            "category": self.category,
            "tags": self.tags,
            "image_url": self.image_url,
            "capacity": self.capacity,
            "source_platform": self.source_platform,
        }
