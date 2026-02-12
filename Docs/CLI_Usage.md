# CLI Usage

The package includes a command-line script for extracting events in a single command.

## Basic Usage

```bash
python -m eventbrite_extractor.extract_events
```

By default this searches for **AI events in New York City** and exports results to both JSON and CSV in the `output/` directory.

## Options

| Flag | Default | Description |
|------|---------|-------------|
| `-q`, `--query` | `AI` | Search keyword |
| `--pages` | `3` | Maximum number of pages to fetch |
| `--page-size` | `20` | Results per page (max 50) |
| `--place-id` | `85977539` (NYC) | Who's On First place ID for location filtering. Use `none` for worldwide. |
| `--online-only` | `False` | Only include online events |
| `--format` | `both` | Output format: `json`, `csv`, or `both` |
| `-o`, `--output-dir` | `output/` | Output directory |

## Examples

### Extract AI events in NYC (default)

```bash
python -m eventbrite_extractor.extract_events
```

### Search for machine learning events, 5 pages, JSON only

```bash
python -m eventbrite_extractor.extract_events -q "machine learning" --pages 5 --format json
```

### Online-only AI events (worldwide)

```bash
python -m eventbrite_extractor.extract_events --online-only --place-id none
```

### Export to a custom directory

```bash
python -m eventbrite_extractor.extract_events -o data/ai_events
```

## Output

The script produces:

- **`output/events.json`** — Full event data in JSON format
- **`output/events.csv`** — Tabular event data in CSV format

It also prints a summary of all extracted events to the terminal.
