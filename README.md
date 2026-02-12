# Eventbrite Data Extraction Package

A Python package that extracts public AI event data from Eventbrite as part of an ETL pipeline for newsletter content generation.

## Overview

This project implements the **Extract** stage of an ETL (Extract, Transform, Load) pipeline. It collects public event data from Eventbrite using the destination/search API, returning structured records that can be used to populate newsletters with upcoming events.

## Features

- Search events by keyword (e.g. "AI", "machine learning")
- Continuation-based pagination for large result sets
- Automatic deduplication of events
- Rate limit handling with exponential backoff
- Structured event records (title, date, venue, organizer, pricing, tags, etc.)
- JSON and CSV export
- CLI script for one-command extraction

## Project Structure

```
newsletter/
├── Docs/                              # Project documentation
├── src/
│   └── eventbrite_extractor/
│       ├── __init__.py                # Package public API
│       ├── client.py                  # Eventbrite API client
│       ├── models.py                  # Event data model
│       ├── config.py                  # Configuration management
│       ├── export.py                  # JSON/CSV export utilities
│       └── extract_events.py          # CLI entry point
├── tests/
│   ├── test_client.py                 # Client tests
│   ├── test_models.py                 # Model tests
│   └── test_export.py                 # Export tests
├── .env.example                       # Environment variable template
├── pyproject.toml                     # Project metadata and build config
├── requirements.txt                   # Python dependencies
└── README.md
```

## Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/NurjahanJ/newsletter.git
   cd newsletter
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Linux/macOS
   .venv\Scripts\activate      # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -e ".[dev]"
   ```

4. **Configure your API key**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your Eventbrite **Private token**. You can obtain one at https://www.eventbrite.com/platform/api.

## Usage

### CLI (Recommended)

Extract AI events with a single command:

```bash
python -m eventbrite_extractor.extract_events
```

Options:

| Flag | Default | Description |
|------|---------|-------------|
| `-q`, `--query` | `AI` | Search keyword |
| `--pages` | `3` | Max pages to fetch |
| `--page-size` | `20` | Results per page (max 50) |
| `--online-only` | `False` | Only include online events |
| `--format` | `both` | Output format: `json`, `csv`, or `both` |
| `-o`, `--output-dir` | `output/` | Output directory |

Examples:

```bash
# Extract AI events (default)
python -m eventbrite_extractor.extract_events

# Search for machine learning events, 5 pages, JSON only
python -m eventbrite_extractor.extract_events -q "machine learning" --pages 5 --format json

# Online-only AI events
python -m eventbrite_extractor.extract_events --online-only
```

### Python API

```python
from eventbrite_extractor import EventbriteClient, export_to_json, export_to_csv

client = EventbriteClient()

# Search for AI events
events = client.search_events(keyword="AI", max_pages=3)

# Export results
export_to_json(events, "output/events.json")
export_to_csv(events, "output/events.csv")

# Access event fields
for event in events:
    print(f"{event.title} — {event.start_date} — {event.url}")
```

### Event Fields

Each extracted event includes:

| Field | Description |
|-------|-------------|
| `event_id` | Eventbrite event ID |
| `title` | Event name |
| `summary` | Short description |
| `start_date` / `start_time` | Event start |
| `end_date` / `end_time` | Event end |
| `timezone` | Event timezone |
| `is_online` | Whether the event is online |
| `venue_name` / `venue_address` | Physical location |
| `organizer_name` / `organizer_id` | Event organizer |
| `url` | Eventbrite event page |
| `is_free` / `price` / `currency` | Pricing info |
| `category` / `tags` | Event categorization |
| `image_url` | Event image |
| `is_cancelled` | Cancellation status |
| `published` | Publication timestamp |

## Running Tests

```bash
pytest tests/ -v
```

## Linting and Formatting

```bash
ruff check .        # Lint
ruff check . --fix  # Lint with auto-fix
ruff format .       # Format
```

## License

This project is for educational purposes.
