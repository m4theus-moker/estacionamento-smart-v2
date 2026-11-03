# Design

## Context

See proposal.md - Why. The project uses Streamlit for client and admin UI and Xano as the backend (`XANO_PARKING_URL`). Draft reservation endpoints in `./xano-pendente` must be reviewed and validated before moving to `./xano-real`.

## Goals / Non-Goals

**Goals:**
- Implement Xano endpoints for availability checking, client booking/listing/cancellation, and admin oversight/cancellation.
- Enforce business rules strictly in Xano: overlap detection (`start < existing_end AND end > existing_start`), vehicle-slot compatibility (`carro` in car/electric, `moto` in moto, `pcd` in pcd/car), ceiling-hour pricing (`CEIL`) with rate snapshot, future start times, user ownership (`$auth.id`), and zero exposure of CPF/phone.
- Update frontend views ("Consultar & Reservar", "Minhas Reservas", "Todas as Reservas") and activate them when endpoints exist.
- Add deletion guards preventing deletion of locations, slots, or rates with linked reservations.
- Persist vehicle type (`carro`, `moto`, `pcd`) in the Xano `vehicle` table schema, `vehicle_POST`, and `vehicle/{id}_PUT`.

**Non-Goals:**
- Payments, notifications, pending status, SQLite persistence, or changes to authentication.

## Decisions & Architecture

- **Availability Logic**: Based exclusively on active reservation overlaps (`start < existing_end AND end > existing_start`). Slot static `status` is not altered. Touching periods (`start == existing_end`) are permitted.
- **Pricing & Snapshot**: Price is calculated in Xano by rounding up duration hours (`CEIL`) multiplied by the hourly rate for the (location, slot type). The resulting price is stored as a snapshot in the reservation record so future rate updates don't affect past bookings.
- **Security & Authorization**: `$auth.id` is derived from the JWT bearer token. Request bodies cannot override `user_id` or `role`. Response payloads omit CPF and phone number fields. Xano input validation runs before admin/role checks, meaning incomplete bodies return HTTP 400 instead of HTTP 403.
- **Xano Assets Review**: Review `./xano-pendente/api/parking_management` and `./xano-pendente/table/reservation.xs` before deploying to `./xano-real`.

## Risks / Trade-offs

- [Concurrency / Double Booking Risk] → **Partially Mitigated**. Xano does not provide an equivalent to SQL `BEGIN IMMEDIATE`. Mitigation implemented: strict overlap check (`start < existing_end AND end > existing_start`) executed in the function stack immediately before database insert. Residual risk: high-frequency race conditions under extreme concurrent load could theoretically bypass checks if two transactions query and insert simultaneously without database-level table locks.
- [Input Validation vs Auth Ordering] → Xano evaluates input validation before executing precondition authorization checks; consequently, malformed or missing body parameters yield HTTP 400 Bad Request rather than HTTP 403 Forbidden.
