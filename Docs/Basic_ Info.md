# Eventbrite Data Extraction Package


## Overview

This project implements the Extract stage of an ETL (Extract, Transform, Load) pipeline by building a Python package that collects public event data from Eventbrite.

The extracted data is intended for use in a newsletter, where upcoming events can be highlighted based on topic, location, and date. This package focuses only on data collection, not transformation or publication.

## Project Goals

The main goals of this project are:

To programmatically extract public event data from Eventbrite

To organize raw event information into a structured, reusable format

To support automated content discovery for newsletters

To demonstrate the Extract phase of a real-world ETL pipeline

## What is Eventbrite?

Eventbrite is an online event discovery and ticketing platform where individuals and organizations publish events.

Eventbrite hosts information such as:

Event titles and descriptions

Dates and times

Physical and online locations

Organizer details

Pricing information

Because Eventbrite provides consistent, structured event data, it is a suitable source for automated data extraction.

## Why Eventbrite?

Eventbrite was chosen as the data source because:

It provides publicly accessible event listings

Event data is naturally suited for newsletters

Events can be searched by keyword, location, and date

Official developer documentation and usage guidelines are available

## ETL Pipeline Context

This project covers only the Extract (E) portion of the ETL pipeline.

### Included

Connecting to Eventbrite as a data source

Retrieving public event metadata

Returning structured event records

### Not Included

Data transformation or ranking

Newsletter formatting or publishing

Database storage or email delivery

### Data Extracted

The package extracts the following event fields (when available):

Event title

Event start and end date/time

Location (venue or online)

Organizer name

Event description summary

Event URL

Pricing information (free or paid)

Event category or tags

Source platform identifier

This data is intended to be newsletter-ready and easily consumable by downstream tools.

Project Scope
Minimum Scope

Extract events by keyword and location

Support a configurable date range

Return structured event records

### Optional Enhancements

Pagination support

Basic deduplication

Export to JSON or CSV formats

Rate limit handling

### Intended Use Case

This package is designed to support:

Automated event discovery

Weekly newsletters

Educational ETL pipeline demonstrations

Integration with other data sources (e.g., Reddit or Twitter)

### Data Source and Documentation

The data used in this project comes from Eventbrite’s official platform:

Eventbrite Platform API
https://www.eventbrite.com/platform/api

Authentication Documentation
https://www.eventbrite.com/platform/docs/authentication

Events Endpoint Documentation
https://www.eventbrite.com/platform/docs/events

Rate Limits
https://www.eventbrite.com/platform/docs/rate-limits

API Terms of Use
https://www.eventbrite.com/help/en-us/articles/833731/eventbrite-api-terms-of-use