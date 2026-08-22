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