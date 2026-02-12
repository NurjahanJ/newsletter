# API Reference

## Python API

The package exposes four public components:

```python
from eventbrite_extractor import EventbriteClient, Event, export_to_json, export_to_csv
```

---

## EventbriteClient

### `EventbriteClient(api_key=None)`

Creates a new API client. If `api_key` is not provided, it reads from the `EVENTBRITE_API_KEY` environment variable.

```python
client = EventbriteClient()
```

### `client.search_events(keyword, place_id=NYC_PLACE_ID, online_only=False, max_pages=1, page_size=20)`

Search for public events on Eventbrite.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `keyword` | `str` | *(required)* | Search query (e.g. `"AI"`) |
| `place_id` | `str \| None` | `"85977539"` (NYC) | Who's On First place ID. `None` for worldwide. |
| `online_only` | `bool` | `False` | Only return online events |
| `max_pages` | `int` | `1` | Maximum pages to fetch |
| `page_size` | `int` | `20` | Results per page (max 50) |

**Returns:** `list[Event]`

```python
events = client.search_events(keyword="AI", max_pages=3)
```

### `client.get_event_by_id(event_id)`

Fetch a single event by its Eventbrite ID.

**Returns:** `Event`

```python
event = client.get_event_by_id("1980413631483")
```

---

## Event

A dataclass representing a single Eventbrite event.

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `event_id` | `str` | Eventbrite event ID |
| `title` | `str` | Event name |
| `summary` | `str \| None` | Short description |
| `start_date` | `str \| None` | Start date (`YYYY-MM-DD`) |
| `start_time` | `str \| None` | Start time (`HH:MM`) |
| `end_date` | `str \| None` | End date |
| `end_time` | `str \| None` | End time |
| `timezone` | `str \| None` | Event timezone |
| `is_online` | `bool` | Whether the event is online |
| `venue_name` | `str \| None` | Venue name |
| `venue_address` | `str \| None` | Venue city, region, country |
| `organizer_name` | `str \| None` | Organizer name |
| `organizer_id` | `str \| None` | Organizer ID |
| `url` | `str \| None` | Eventbrite event page URL |
| `is_free` | `bool` | Whether the event is free |
| `price` | `str \| None` | Minimum ticket price |
| `currency` | `str \| None` | Price currency code |
| `category` | `str \| None` | Event category |
| `tags` | `list[str]` | Tag display names |
| `image_url` | `str \| None` | Event image URL |
| `is_cancelled` | `bool` | Whether the event is cancelled |
| `published` | `str \| None` | Publication timestamp |
| `source_platform` | `str` | Always `"eventbrite"` |

### Methods

- **`Event.from_api_response(data)`** — Create an Event from a raw API response dict
- **`event.to_dict()`** — Convert to a plain dictionary

---

## Export Functions

### `export_to_json(events, filepath, indent=2)`

Export events to a JSON file. Creates parent directories if needed.

**Returns:** `Path` to the written file.

```python
export_to_json(events, "output/events.json")
```

### `export_to_csv(events, filepath)`

Export events to a CSV file. List fields (tags) are joined as comma-separated strings.

**Returns:** `Path` to the written file.

```python
export_to_csv(events, "output/events.csv")
```

---

## Full Example

```python
from eventbrite_extractor import EventbriteClient, export_to_json, export_to_csv

client = EventbriteClient()

# Search for AI events in NYC
events = client.search_events(keyword="AI", max_pages=3)

# Export
export_to_json(events, "output/events.json")
export_to_csv(events, "output/events.csv")

# Print results
for event in events:
    print(f"{event.title} — {event.start_date} — {event.url}")
```
