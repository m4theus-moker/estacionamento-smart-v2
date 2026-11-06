# Design

## Context

See `proposal.md` for motivation. The project uses Xano (backend) and Streamlit (frontend) with XanoScript syntax rules and strict rate limit considerations on Xano free tier (10 requests per 20s).

## Goals / Non-Goals

**Goals:**
- Implement robust ticket code generation (`ticket_code`) with retry logic (up to 5 attempts with collision abort) and non-ambiguous alphabet.
- Implement explicit 3-step deployment order (1. optional column + POST generation, 2. backfill reusing generator, 3. unique index).
- Implement `GET /reservation/{id}/ticket` with server-side status calculation (strict 4 statuses), secure error handling (401/404), and price snapshot.
- Integrate ticket modal (`st.dialog`), post-creation button, session-state caching keyed by reservation ID with 60s max TTL (storing timestamp) and cache invalidation on cancellation, and self-contained HTML download (`ticket-<CODIGO>.html`) including "Emitido em".
- Adhere to XanoScript syntax standards, Xano free-tier rate limits, and reuse existing date formatters (`America/Sao_Paulo`).

**Non-Goals:**
- QR code generation, PDF generation, email dispatch, or check-in/check-out/billing flows (explicitly out of scope).

## Decisions

### 1. Backend: Code Generator, Retry, Collision Policy & Explicit 3-Step Deployment
- **Code Generation, Alphabet & Collision Policy**:
  - Alphabet: Strict non-ambiguous uppercase alphanumeric excluding `0, O, 1, I, L` -> `ABCDEFGHJKMNPQRSTUVWXYZ23456789`.
  - Length: Exactly 8 characters, generated using non-predictable randomness. O gerador usa UUID hex com 0->G e 1->H, um subconjunto do alfabeto permitido (16^8 códigos).
  - Collision handling & Failure behavior: Upon creation (`POST /reservation`), attempt to generate a unique code up to 5 times. If all 5 attempts collide against existing records, abort the reservation creation transaction and return an error response.
- **Explicit 3-Step Deployment Order**:
  1. **Step 1**: Add `ticket_code` as an optional string field to the `reservation` table and update `POST /reservation` to generate codes upon creation (reusing the generator).
  2. **Step 2**: Execute a backend backfill routine for existing reservations missing a `ticket_code`, reusing the exact same generator function.
  3. **Step 3**: Apply a unique index to the `ticket_code` column.

### 2. Backend Endpoint: `GET /reservation/{id}/ticket` & Authorization
- **Authentication & Authorization**:
  - Requires valid authentication (`auth`). Returns `401` if unauthenticated.
  - Role check for admin: `auth.role == 'admin'` (unified check, avoiding ambiguity).
  - Authorization check: Admins can access any reservation. Regular users can only access their own reservations (`auth.id == reservation.user_id`).
  - Security & Error Codes: To prevent ID enumeration, return `404 Not Found` both when a reservation does not exist AND when a regular user attempts to access another user's reservation.
- **Server-Side Status Calculation (Strict 4 Values)**:
  - Evaluated dynamically using server current time (`now`):
    - If reservation status is cancelled -> `"Cancelado"`
    - If `now < start_time` -> `"Válido"`
    - If `start_time <= now < end_time` -> `"Em andamento"`
    - If `now >= end_time` -> `"Expirado"`
- **Pricing Snapshot**:
  - `price` is retrieved directly from the reservation record (snapshot stored at creation time), ensuring ticket prices remain stable even if parking rates change later.

### 3. Frontend: Streamlit Integration & Security
- **Secure Caching with TTL & Invalidation**:
  - Store fetched ticket data in `st.session_state` keyed by reservation ID.
  - Enforce a maximum TTL of 60 seconds by storing a timestamp alongside the cached data in `st.session_state`, re-fetching if expired (since status depends on current time).
  - Invalidate the cached ticket entry in `st.session_state` immediately when a reservation is cancelled.
- **UI Integration**:
  - Add a "Ver ticket" button right after successful reservation creation in "Consultar & Reservar" displaying the generated code and modal access.
  - Add "Ver ticket" in "Minhas Reservas" (Active and History tabs) and admin reservations table.
  - Clicking opens an `st.dialog` displaying the ticket details, prominent code, status badge, and schedule formatted using the shared timezone/date formatter (`dd/mm/aaaa HH:MM`, `America/Sao_Paulo`) from `melhorias-frontend-ux`.
- **Downloadable HTML**:
  - Provide "Baixar ticket" button using `st.download_button` generating a self-contained, standalone printable HTML file named `ticket-<CODIGO>.html` with inline CSS, `@media print`, and displaying "Emitido em" (issued at).
- **Security**:
  - Escape all dynamic text data using `html.escape()` before rendering in HTML/Markdown.

## Risks / Trade-offs

- [Rate Limit on Xano Free Tier] → Mitigation: Fetch ticket data lazily on button click and use `st.session_state` caching with 60s TTL.
- [Ticket Code Collision] → Mitigation: 8-character non-ambiguous alphabet, unique index after backfill, 5 retry attempts, and abort on persistent collision.
