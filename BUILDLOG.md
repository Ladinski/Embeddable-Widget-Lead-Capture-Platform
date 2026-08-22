# Build Log

## Project Setup

Created the project as a standalone Python/FastAPI backend using a layered architecture.

The application is split into:

- routers for HTTP handling
- services for business logic
- repositories for database access
- schemas for validation
- SQLAlchemy models for persistence
- core modules for configuration, authentication, database setup, and rate limiting

Docker Compose is used to run FastAPI and PostgreSQL.

## Authentication

Implemented user registration and login using JWT authentication.

Passwords are hashed using pwdlib.

An authentication dependency extracts the current user from the JWT and protects widget and dashboard routes.

## Widget Management

Implemented authenticated CRUD for widgets.

Widget ownership is included in repository queries so one user cannot access another user's widgets.

Each widget stores its type, title, description, button text, fields, status, and owner.

## Widget Delivery

Added an embed endpoint that generates a one-line script tag.

Created `widget.js`, which:

1. reads the widget ID from its script URL
2. fetches the public widget configuration
3. creates the form dynamically
4. inserts the widget into the customer page
5. submits data back to the public API

A plain HTML page served on port 5500 is used to verify cross-origin behavior.

## Public Submissions

Created a public endpoint for widget submissions.

Incoming fields are compared against the widget configuration before data is stored.

Required fields are enforced and unknown fields are rejected.

## CORS

Initially the widget JavaScript loaded successfully, but the configuration fetch was blocked by the browser because the API did not return CORS headers.

Added FastAPI CORSMiddleware for the customer-site origin.

Verified GET requests and POST preflight requests across ports 5500 and 8000.

## Abuse Protection

Added SlowAPI rate limiting to the public submission endpoint.

Added maximum field and string-length checks.

Added a hidden honeypot field to the widget form.

During implementation the honeypot field names became inconsistent between JavaScript, Pydantic, and the service layer. This caused valid submissions to be rejected and later caused a 500 error.

Standardized the field as `form_check` across all layers.

## Geo Enrichment

Added two IP geolocation providers.

Provider B is attempted if Provider A fails.

If both fail, enrichment returns no location and the submission continues normally.

Local Docker traffic uses a private network IP, so local submissions correctly store null geo values.

## Safe Side Effects

Added a notification action after storing a submission.

The notification is wrapped so failures are logged but do not affect the successful submission.

## Dashboard

Added authenticated endpoints for viewing stored submissions and basic analytics.

Statistics currently include total submissions, submissions per widget, and country breakdown.

## Testing

Added pytest integration and service tests.

The rate limiter initially caused unrelated integration tests to receive 429 responses because all TestClient requests came from the same client address.

The normal test fixture now disables the limiter, while a dedicated rate-limit test explicitly enables it.

Current test suite result:

```text
14 passed