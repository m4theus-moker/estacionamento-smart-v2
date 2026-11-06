# Spec Delta

## Purpose

Provides reservation ticket issuance, server-side status calculation (strict 4 statuses), secure retrieval, and UI rendering and downloading capabilities.

## ADDED Requirements

### Requirement: Ticket Code Generation, Retry, Collision Abort, and Explicit 3-Step Deployment
The Xano backend SHALL implement an 8-character uppercase alphanumeric ticket code generator using a strict non-ambiguous alphabet (`ABCDEFGHJKMNPQRSTUVWXYZ23456789`, excluding `0, O, 1, I, L`), with up to 5 retry attempts upon reservation creation (`POST /reservation`) and aborting creation if all attempts collide. Furthermore, it shall execute an explicit 3-step deployment (1. optional column & POST generation, 2. backfill reusing generator, 3. unique index).

#### Scenario: Ticket code generation with retry and collision abort
- **WHEN** a client creates a reservation via `POST /reservation`
- **THEN** the backend attempts to assign a unique 8-character code (retrying up to 5 times); if all attempts collide, it aborts the transaction and returns an error response

#### Scenario: Explicit 3-step deployment and backfill
- **WHEN** the backend deployment runs in sequence (optional column & POST generation, backfill reusing the generator, and unique index creation)
- **THEN** all existing and new reservations receive valid unique ticket codes without errors

### Requirement: Secure Ticket Retrieval API and Error Handling
The Xano backend SHALL provide `GET /reservation/{id}/ticket` requiring authentication (`auth`), returning 401 if unauthenticated, 404 for both non-existent reservations and reservations belonging to another user (preventing ID enumeration), and allowing reservation owners or administrators (`auth.role == 'admin'`) to retrieve complete resolved ticket details.

#### Scenario: Owner retrieves ticket
- **WHEN** the reservation owner makes a GET request to `/reservation/{id}/ticket` with valid auth
- **THEN** the backend returns 200 with ticket details including resolved location name/address, slot number/type, vehicle plate/brand/model, client name (without CPF, phone, or email), period, duration, snapshot pricing (`price`), issued date, ticket code, and calculated status

#### Scenario: Administrator retrieves any ticket
- **WHEN** an administrator (`auth.role == 'admin'`) makes a GET request to `/reservation/{id}/ticket` for any user's reservation
- **THEN** the backend returns 200 with the complete ticket details

#### Scenario: Non-existent or unauthorized reservation returns 404
- **WHEN** a non-owner user or unauthenticated request targets a non-existent reservation or another user's reservation ID
- **THEN** the backend returns 404 Not Found (or 401 if unauthenticated) to prevent ID enumeration

### Requirement: Server-Side Ticket Status Calculation (Strict 4 Values)
The Xano backend SHALL calculate the reservation ticket status dynamically using server-side time (`now`) into exactly one of four values: `"Cancelado"`, `"Válido"`, `"Em andamento"`, or `"Expirado"`.

#### Scenario: Status calculation for cancelled reservation
- **WHEN** the reservation status is cancelled
- **THEN** the ticket status is calculated as `"Cancelado"`

#### Scenario: Status calculation for future reservation
- **WHEN** the server current time is before the reservation start time (`now < start_time`)
- **THEN** the ticket status is calculated as `"Válido"`

#### Scenario: Status calculation for ongoing reservation
- **WHEN** the server current time is between reservation start and end times (`start_time <= now < end_time`)
- **THEN** the ticket status is calculated as `"Em andamento"`

#### Scenario: Status calculation for expired reservation
- **WHEN** the server current time is after or equal to the reservation end time (`now >= end_time`)
- **THEN** the ticket status is calculated as `"Expirado"`

### Requirement: Frontend Ticket Modal, Session Caching with TTL, Invalidation, and Download
The Streamlit frontend SHALL provide a "Ver ticket" button right after reservation creation and in "Minhas Reservas" / admin screens, opening an `st.dialog` with ticket details, HTML escaping (`html.escape`), `st.session_state` caching keyed by reservation ID with a maximum TTL of 60 seconds (storing timestamp) and cache invalidation upon reservation cancellation, shared date formatting (`America/Sao_Paulo`), and a "Baixar ticket" button generating a self-contained printable HTML file named `ticket-<CODIGO>.html` including "Emitido em".

#### Scenario: User views reservation ticket via modal with 60s TTL session caching
- **WHEN** the user clicks "Ver ticket" after reservation creation or in reservation lists
- **THEN** an `st.dialog` opens displaying escaped ticket details, ticket code, status badge, and schedule formatted using the shared timezone/date formatter (`America/Sao_Paulo`), utilizing `st.session_state` caching with a 60s max TTL timestamp check

#### Scenario: Cache invalidation on reservation cancellation
- **WHEN** the user cancels a reservation
- **THEN** the cached ticket data for that reservation in `st.session_state` is immediately invalidated

#### Scenario: User downloads self-contained printable ticket HTML with "Emitido em"
- **WHEN** the user clicks "Baixar ticket" inside the ticket dialog
- **THEN** Streamlit downloads a standalone self-contained printable HTML file named `ticket-<CODIGO>.html` with inline CSS, `@media print`, and displaying "Emitido em" (issued at)
