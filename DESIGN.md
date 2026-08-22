# Embeddable Widget & Lead Capture Platform — Design

## Problem

Customers need a way to create simple widgets such as signup forms, contact forms, and call-to-action popovers and embed them on external websites using a single script tag.

Visitors can then interact with those widgets and send submissions to the backend.

Because submissions come from websites and browsers that the application does not control, all public input must be treated as untrusted.

## Core Actors

### Widget Owner

An authenticated customer who can:

- Create widgets
- View their widgets
- Update their widgets
- Delete their widgets
- Generate embed snippets
- View submissions
- View submission statistics

### Website Visitor

An unauthenticated visitor who:

- Loads a widget on an external website
- Submits data through the widget

## Core Models

### User

Represents the owner of widgets.

Planned fields:

- id
- email
- hashed_password
- created_at

### Widget

Represents an embeddable widget.

Planned fields:

- id
- owner_id
- type
- title
- description
- button_text
- fields
- is_active
- created_at
- updated_at

### Submission

Represents data submitted through a widget.

Planned fields:

- id
- widget_id
- data
- ip_address
- country
- city
- created_at

## Embed Flow

1. Owner creates a widget.
2. Backend generates an embed snippet.
3. Customer adds the script tag to their website.
4. Browser loads widget.js.
5. widget.js requests the widget configuration.
6. JavaScript renders the widget.
7. Visitor submits the form.
8. Submission is sent to the public API.
9. Backend validates the payload.
10. Backend checks rate limits and spam protection.
11. Backend attempts geo enrichment.
12. Submission is stored.
13. A non-critical email or webhook side effect runs.
14. Owner can view the submission through the dashboard API.

## Non-Goal

A full visual drag-and-drop form builder is not part of the core project.

The widget UI will remain minimal because the focus of this capstone is backend architecture, security, resilience, and public API design.


## API Surface

### Authentication

#### POST /auth/register

Creates a new user account.

#### POST /auth/login

Authenticates a user and returns an access token.

---

## Widget Management API

All widget management endpoints require authentication.

### POST /widgets

Creates a new widget owned by the authenticated user.

### GET /widgets

Returns all widgets owned by the authenticated user.

### GET /widgets/{widget_id}

Returns one widget owned by the authenticated user.

### PUT /widgets/{widget_id}

Updates a widget owned by the authenticated user.

### DELETE /widgets/{widget_id}

Deletes a widget owned by the authenticated user.

### GET /widgets/{widget_id}/embed

Returns the script snippet used to embed the widget.

Example:

<script src="http://localhost:8000/static/widget.js?id=abc123"></script>

---

## Public Widget Delivery

These endpoints do not require authentication.

### GET /public/widgets/{widget_id}/config

Returns the public configuration required to render a widget.

The response should contain only information needed by the frontend widget.

Example response:

{
  "id": "abc123",
  "type": "contact",
  "title": "Contact us",
  "description": "Send us a message",
  "button_text": "Submit",
  "fields": [
    {
      "name": "email",
      "type": "email",
      "required": true
    }
  ]
}

The endpoint will use HTTP cache headers so widget configuration can be cached for a short period.

---

## Public Submission API

### POST /public/widgets/{widget_id}/submissions

Accepts a submission from an embedded widget.

Request flow:

1. Validate the request.
2. Verify that the widget exists and is active.
3. Apply rate limiting.
4. Check spam protection.
5. Attempt IP geolocation enrichment.
6. Store the submission.
7. Trigger a non-critical side effect.
8. Return a success response.

Invalid input should return a 4xx response rather than causing a server error.

Rate-limited requests should return HTTP 429.

Failures from geolocation providers or notification services must not cause a valid submission to fail.

---

## Dashboard API

All dashboard endpoints require authentication.

### GET /dashboard/submissions

Returns submissions belonging to widgets owned by the authenticated user.

Optional filters may include:

- widget_id
- start_date
- end_date
- limit
- offset

### GET /dashboard/stats

Returns basic submission statistics for the authenticated user.

Planned statistics:

- total submissions
- submissions per widget
- submissions over time
- country breakdown