# Proposal

## Why

When a reservation is made, clients and administrators need access to a structured, printable reservation ticket containing details about the location, slot, vehicle, pricing (using reservation price snapshot), and precise status ("Cancelado", "Válido", "Em andamento", or "Expirado"). This improves usability and provides formal confirmation without requiring full check-in/check-out flows yet.

## What Changes

- **Backend (Xano)**:
  - Implement unique 8-character uppercase alphanumeric non-sequential ticket code generator using a strict non-ambiguous alphabet (`ABCDEFGHJKMNPQRSTUVWXYZ23456789`, excluding `0, O, 1, I, L`), with up to 5 retry attempts upon reservation creation (`POST /reservation`). If all 5 attempts collide, abort reservation creation and return an error.
  - Add optional `ticket_code` field to the `reservation` table and execute an explicit 3-step deployment/migration order: (1) Add optional column & update POST endpoint (reusing the generator), (2) Run backfill for existing reservations reusing the generator, (3) Apply unique index on `ticket_code`.
  - Implement `GET /reservation/{id}/ticket` endpoint with authentication (`auth`), returning 401 if unauthenticated, 404 for both non-existent reservations and reservations belonging to another user (preventing ID enumeration), and allowing admins (`auth.role == 'admin'`) or reservation owners to access comprehensive ticket details (resolved names, price and duration snapshot, server-calculated status).
- **Frontend (Streamlit)**:
  - Add "Ver ticket" button right after successful reservation creation in the "Consultar & Reservar" screen showing the generated code.
  - Add "Ver ticket" button in "Minhas Reservas" (Active and History tabs) and the admin reservations screen.
  - Open an `st.dialog` displaying the ticket with visual emphasis on the ticket code, status badge, and schedule (reusing timezone/date formatter from `melhorias-frontend-ux`).
  - Provide a "Baixar ticket" download button generating a standalone, self-contained printable HTML file named `ticket-<CODIGO>.html` with inline CSS, `@media print`, and displaying "Emitido em" (issued at).
  - Secure state caching: store fetched ticket data in `st.session_state` keyed by reservation ID with a maximum TTL of 60 seconds (storing timestamp) since status depends on current time, alongside cache invalidation upon reservation cancellation.
  - Ensure proper HTML escaping (`html.escape`) for all dynamic text fields.

## Capabilities

### New Capabilities
- `reservations-ticket`: Issuance, status calculation, secure retrieval, and UI rendering/downloading of reservation tickets.

### Modified Capabilities
- (None - using new capability for ticket management).

## Impact

- Database schema update: `ticket_code` column added to `reservation` table with unique index and 3-step deployment order.
- New API endpoint: `GET /reservation/{id}/ticket`.
- Frontend enhancements: Streamlit UI components (`st.dialog`, download button, modal view, post-creation ticket view, session state caching with 60s TTL and cancellation invalidation).
