# Eventbrite Data Extraction Package

A Python package that extracts public event data from Eventbrite as part of an ETL pipeline for newsletter content generation.

## Overview

This project implements the **Extract** stage of an ETL (Extract, Transform, Load) pipeline. It collects public event data from Eventbrite, returning structured records that can be used to populate newsletters with upcoming events based on topic, location, and date.

## Features

- Search events by keyword and location
- Configurable date range filtering
- Structured event records (title, date, location, organizer, pricing, etc.)
- JSON and CSV export support

## Project Structure

```
newsletter/
├── Docs/                          # Project documentation
├── src/
│   └── eventbrite_extractor/
│       ├── __init__.py            # Package init
│       ├── client.py              # Eventbrite API client
│       ├── models.py              # Event data models
│       ├── config.py              # Configuration management
│       └── export.py              # JSON/CSV export utilities
├── tests/
│   ├── test_client.py             # Client tests
│   └── test_models.py             # Model tests
├── .env.example                   # Environment variable template
├── pyproject.toml                 # Project metadata and build config
├── requirements.txt               # Python dependencies
└── README.md
```

## Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/<your-username>/newsletter.git
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
   ```

4. **Configure your API key**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your Eventbrite OAuth token. You can obtain one at https://www.eventbrite.com/platform/api.

## Usage

*Coming soon — the API client is under development.*

## Running Tests

```bash
pytest
```

## License

This project is for educational purposes.
