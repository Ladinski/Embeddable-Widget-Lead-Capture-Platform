# Evidence

## Widget Management

### Authenticated widget CRUD

Implemented authenticated widget creation, listing, retrieval, update, and deletion.

Endpoints:

- POST /widgets
- GET /widgets
- GET /widgets/{widget_id}
- PUT /widgets/{widget_id}
- DELETE /widgets/{widget_id}

### Tenant Isolation

Widget queries include the authenticated owner's ID.

A user can only retrieve or modify widgets that belong to their account.

---

## Widget Delivery

### Embed Snippet

Endpoint:

GET /widgets/{widget_id}/embed

Example output:

```html
<script src="http://localhost:8000/static/widget.js?id=1"></script>