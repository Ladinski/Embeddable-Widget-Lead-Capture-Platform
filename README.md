# Embeddable Widget & Lead Capture Platform

A backend platform for creating embeddable website widgets and safely collecting lead submissions from external websites.

A widget owner can create and manage widgets through an authenticated API, generate a one-line embed script, receive cross-origin form submissions, and view submissions and analytics through dashboard endpoints.

## Features

- JWT authentication
- Authenticated widget CRUD
- Tenant-isolated widget ownership
- One-line widget embed snippet
- Public cached widget configuration
- Embeddable JavaScript widget loader
- Cross-origin form submissions
- CORS and preflight handling
- Payload validation
- Oversized payload protection
- Honeypot spam protection
- Per-IP rate limiting
- IP geolocation enrichment
- Geo provider fallback
- Safe notification side effects
- Submission dashboard
- Submission statistics
- Automated integration tests

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Docker Compose
- Pydantic
- SlowAPI
- HTTPX
- Pytest
- Vanilla JavaScript

## Architecture

```text
Widget Owner
    |
    v
Authenticated API
    |
    +--> Auth
    |
    +--> Widget Management
    |        |
    |        v
    |    PostgreSQL
    |
    +--> Dashboard
             |
             v
         Submissions


Customer Website
    |
    | <script src=".../widget.js?id=1">
    v
widget.js
    |
    v
Public Widget Config API
    |
    v
Render Form
    |
    v
Public Submission API
    |
    +--> Validation
    |
    +--> Rate Limiting
    |
    +--> Honeypot Check
    |
    +--> Geo Provider A
    |       |
    |       +--> failure --> Provider B
    |
    +--> Store Submission
    |
    +--> Notification Side Effect