# Tasks

## 1. Xano Backend & Endpoints Setup

- [ ] 1.1 Implement 8-character uppercase alphanumeric ticket code generator using the strict non-ambiguous alphabet (`ABCDEFGHJKMNPQRSTUVWXYZ23456789`, excluding `0, O, 1, I, L`) with up to 5 retry attempts upon creation (`POST /reservation`). Abort reservation creation and return an error if all 5 attempts collide.
- [ ] 1.2 Implement explicit 3-step deployment and migration order:
  - **Step 1**: Add `ticket_code` as an optional string field to the `reservation` table and update `POST /reservation` to generate codes upon creation (reusing the generator).
  - **Step 2**: Run backend backfill routine for existing reservations missing a `ticket_code`, reusing the exact same generator function.
  - **Step 3**: Apply unique index on `ticket_code`.
- [ ] 1.3 Implement `GET /reservation/{id}/ticket` endpoint requiring authentication (`auth`), returning 401 if unauthenticated, 404 for both non-existent reservations and reservations belonging to another user (preventing ID enumeration), and allowing owners or administrators (`auth.role == 'admin'`) to retrieve resolved ticket details with price snapshot.
- [ ] 1.4 Implement server-side dynamic status calculation returning exactly one of four values: `"Cancelado"`, `"Válido"`, `"Em andamento"`, or `"Expirado"`.

## 2. Streamlit Frontend Integration & Security

- [ ] 2.1 Add "Ver ticket" button right after successful reservation creation in the "Consultar & Reservar" screen displaying the generated code and modal access.
- [ ] 2.2 Add "Ver ticket" button in "Minhas Reservas" (Active and History tabs) and the admin reservations screen.
- [ ] 2.3 Implement lazy-loaded `st.dialog` modal displaying ticket details, status badge, schedule formatted using the shared timezone/date formatter (`America/Sao_Paulo`) from `melhorias-frontend-ux`, and secure `st.session_state` caching keyed by reservation ID with a maximum TTL of 60 seconds (storing timestamp) and cache invalidation upon reservation cancellation.
- [ ] 2.4 Implement "Baixar ticket" download button inside the dialog generating a standalone, self-contained printable HTML file named `ticket-<CODIGO>.html` with inline CSS, `@media print`, displaying "Emitido em", and proper HTML escaping (`html.escape`).

## 3. Automated Tests & Manual Verification

- [ ] 3.1 Write automated unit test verifying that the ticket HTML generation function properly escapes potentially malicious input (e.g., `<script>` tags in client name or vehicle plate) and includes "Emitido em".
- [ ] 3.2 Perform manual test: New reservations successfully receive a unique 8-character non-ambiguous `ticket_code` (with retry logic and collision abort), and existing records are correctly backfilled via the 3-step deployment.
- [ ] 3.3 Perform manual test: Owner and administrator successfully retrieve ticket details, while unauthorized users or non-existent IDs receive HTTP 404 (preventing enumeration).
- [ ] 3.4 Perform manual test: Ticket status correctly evaluates to `"Cancelado"`, `"Válido"`, `"Em andamento"`, or `"Expirado"` using server time.
- [ ] 3.5 Perform manual test: Streamlit post-creation view, modal dialog, session-state caching (with 60s TTL timestamp check and invalidation on cancellation), and self-contained download (`ticket-<CODIGO>.html`) work correctly.
- [ ] 3.6 Run OpenSpec validation: `openspec validate gerar-ticket-de-reserva`.
