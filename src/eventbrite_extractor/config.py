"""Configuration and environment variable management."""

import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env from the project root
_env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(_env_path)


def get_api_key() -> str:
    """Return the Eventbrite private token from environment variables.

    Raises:
        ValueError: If EVENTBRITE_API_KEY is not set.
    """
    key = os.getenv("EVENTBRITE_API_KEY")
    if not key:
        raise ValueError(
            "EVENTBRITE_API_KEY is not set. "
            "Copy .env.example to .env and add your Eventbrite private token."
        )
    return key


# Eventbrite API v3 base URL
BASE_URL = "https://www.eventbriteapi.com/v3"

# Default settings
DEFAULT_PAGE_SIZE = 50
DEFAULT_LOCATION = "New York"
REQUEST_TIMEOUT = 30
