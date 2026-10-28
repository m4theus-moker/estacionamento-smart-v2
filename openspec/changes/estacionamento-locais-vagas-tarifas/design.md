# Design

## Context

See proposal.md - Why. The project uses Streamlit for the admin/client UI (with `@st.dialog` modals for editing records) and Xano as the complete backend and database (using `XANO_PARKING_URL`), enforcing role-based authorization (`role = admin`) for administrative endpoints.

## Goals / Non-Goals

**Goals:**
- Implement Xano backend endpoints for managing locations, slots (`vaga`), and rates (`tarifa`), enforcing `role = admin` authorization and expecting appropriate payloads (`location_id`, `valor_hora > 0`, etc.).
- Implement Streamlit administrative views ("Locais & Vagas" and "Tarifas") with `@st.dialog` edit forms visible only to administrators.
- Ensure dependency checks prevent deleting locations that have linked slots, rates, or reservations.

**Non-Goals:**
- Client-facing reservation or availability consultation flows (deferred to the reservations change).
- Local SQLite database persistence or backend code outside Xano.

## Decisions

- **Admin Authorization Enforcement**: Validating `role == "admin"` directly in Xano function stacks using conditional preconditions or role enforcement helpers, returning HTTP 403 for unauthorized users on all write operations.
- **Dependency Guard on Location Deletion**: Xano queries checking child records (slots, rates, reservations) before allowing location deletion.
- **Payload Compliance**: Ensuring frontend sends `location_id` when updating/creating slots and rates, and validating `valor_hora > 0`.

## Risks / Trade-offs

- [Unauthorized Access Risk] → Mitigated by strict backend-level authorization checks (`403 Forbidden`) in Xano, independent of frontend menu visibility.
- [Missing Parameter Risk] → Mitigated by aligning frontend request payloads with Xano input specifications (`id_PUT.xs`).
