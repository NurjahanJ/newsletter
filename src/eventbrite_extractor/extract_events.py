"""CLI script to extract AI events from Eventbrite."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from eventbrite_extractor.client import EventbriteClient
from eventbrite_extractor.config import NYC_PLACE_ID
from eventbrite_extractor.export import export_to_csv, export_to_json
from eventbrite_extractor.transform import transform_events

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# CLI argument parsing
# ---------------------------------------------------------------------------


def _build_parser() -> argparse.ArgumentParser:
    """Build and return the CLI argument parser."""
    parser = argparse.ArgumentParser(
        description="Extract AI events from Eventbrite.",
    )
    parser.add_argument(
        "-q",
        "--query",
        default="AI",
        help="Search keyword (default: 'AI').",
    )
    parser.add_argument(
        "--pages",
        type=int,
        default=3,
        help="Max pages to fetch (default: 3).",
    )
    parser.add_argument(
        "--page-size",
        type=int,
        default=20,
        help="Results per page (default: 20, max: 50).",
    )
    parser.add_argument(
        "--place-id",
        default=NYC_PLACE_ID,
        help="Who's On First place ID for location filter "
        "(default: NYC '85977539'). Use 'none' for worldwide.",
    )
    parser.add_argument(
        "--online-only",
        action="store_true",
        help="Only include online events.",
    )
    parser.add_argument(
        "--sort-by",
        choices=["date", "title"],
        default="date",
        help="Sort events by 'date' or 'title' (default: date).",
    )
    parser.add_argument(
        "--free-first",
        action="store_true",
        help="Show free events before paid events.",
    )
    parser.add_argument(
        "--format",
        choices=["json", "csv", "both"],
        default="both",
        help="Output format (default: both).",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        default="output",
        help="Output directory (default: 'output/').",
    )
    return parser


def _resolve_location(place_id_arg: str) -> tuple[str | None, str]:
    """Return (place_id, human-readable label) from the raw CLI value."""
    if place_id_arg.lower() == "none":
        return None, "worldwide"
    if place_id_arg == NYC_PLACE_ID:
        return place_id_arg, "NYC"
    return place_id_arg, place_id_arg


# ---------------------------------------------------------------------------
# Export helpers
# ---------------------------------------------------------------------------


def _export_events(
    enriched: list[dict],
    output_dir: str,
    fmt: str,
) -> None:
    """Write enriched event dicts to the requested file format(s)."""
    out = Path(output_dir)
    if fmt in ("json", "both"):
        path = export_to_json(enriched, out / "events.json")
        logger.info("JSON saved to %s", path)
    if fmt in ("csv", "both"):
        path = export_to_csv(enriched, out / "events.csv")
        logger.info("CSV saved to %s", path)


# ---------------------------------------------------------------------------
# Terminal summary
# ---------------------------------------------------------------------------


def _print_summary(
    enriched: list[dict],
    raw_count: int,
    location_label: str,
) -> None:
    """Print a human-readable event listing to stdout."""
    print(f"\n{'=' * 64}")
    print(f"  {len(enriched)} events in {location_label} (from {raw_count} raw)")
    print(f"{'=' * 64}\n")

    for i, ev in enumerate(enriched, 1):
        print(f"  {i}. [{ev['event_type']}] {ev['title']}")
        print(f"     {ev['display_date']}")
        print(f"     {ev['display_location']}")
        print(f"     {ev['display_price']}")
        print(f"     {ev['url']}")
        print()


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> None:
    """Run the event extraction pipeline."""
    args = _build_parser().parse_args(argv)
    place_id, location_label = _resolve_location(args.place_id)

    logger.info(
        "Searching Eventbrite for '%s' events in %s (max %d pages)...",
        args.query,
        location_label,
        args.pages,
    )

    # --- Extract ---
    client = EventbriteClient()
    raw_events = client.search_events(
        keyword=args.query,
        place_id=place_id,
        online_only=args.online_only,
        max_pages=args.pages,
        page_size=args.page_size,
    )

    if not raw_events:
        logger.warning("No events found for query '%s'.", args.query)
        sys.exit(0)

    logger.info("Found %d raw events. Transforming...", len(raw_events))

    # --- Transform ---
    enriched = transform_events(
        raw_events,
        sort_by=args.sort_by,
        free_first=args.free_first,
    )

    if not enriched:
        logger.warning("No events remaining after filtering.")
        sys.exit(0)

    logger.info("%d events after transform. Exporting...", len(enriched))

    # --- Export (enriched data, not raw) ---
    _export_events(enriched, args.output_dir, args.format)

    # --- Print summary ---
    _print_summary(enriched, raw_count=len(raw_events), location_label=location_label)


if __name__ == "__main__":
    main()
