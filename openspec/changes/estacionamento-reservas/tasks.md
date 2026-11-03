# Tasks

## 1. Xano Backend & Endpoints Setup

- [x] 1.1 Review draft reservation table and endpoints in `./xano-pendente` (reservation table and reservation endpoints) and prepare them for migration to `./xano-real`.
- [x] 1.2 Implement Xano availability endpoint (`reservations-availability`) querying free slots by location, vehicle type, and period based on active reservation overlaps (`start < existing_end AND end > existing_start`), leaving slot `status` unchanged and accepting touching intervals.
- [x] 1.3 Implement Xano booking endpoint (`reservations-booking`) validating future start time, end after start, user vehicle ownership (`$auth.id`), slot location, vehicle-slot type compatibility, ceiling-hour pricing (`CEIL`) with rate snapshot, and pre-insert overlap check returning HTTP 409 on conflict.
- [x] 1.4 Implement Xano client endpoints for listing own reservations and cancelling active reservations (updating status to `cancelled`), ensuring no CPF or phone number is exposed and preventing cancellation of other users' reservations (returning 403/404).
- [x] 1.5 Implement Xano admin endpoints (`reservations-admin`) allowing administrators (`role = admin`) to list all system reservations and cancel any reservation, returning HTTP 403 for client users.
- [x] 1.6 Implement deletion guards in Xano preventing the deletion of locations, slots, or rates that have linked active or historical reservations.

## 2. Frontend Streamlit Activation

- [x] 2.1 Activate and implement "Consultar & Reservar" and "Minhas Reservas" views for clients in Streamlit, connected to availability and booking endpoints.
- [x] 2.2 Activate and implement "Todas as Reservas" view for administrators in Streamlit, connected to admin oversight and cancellation endpoints.

## 3. Manual Verification & Testing

- [ ] 3.1 Perform manual test: Two clients (A and B); client B cannot view or cancel client A's reservation (receives 403/404).
- [ ] 3.2 Perform manual test: Overlapping reservation attempt returns 409; adjacent reservation (starting when another ends) is successfully accepted.
- [ ] 3.3 Perform manual test: Refusal checks for start in the past, end <= start, missing rate, other user's vehicle, other location's slot, and incompatible vehicle type.
- [ ] 3.4 Perform manual test: Double clicking on "Book" does not create duplicate or conflicting reservations.
- [ ] 3.5 Perform manual test: Administrator successfully lists and cancels any reservation, while client users receive HTTP 403 on admin routes.
- [ ] 3.6 Perform manual test: Correct pricing calculation (e.g., 1h05 duration charges 2 hours) and snapshot price preserved after editing the hourly rate.
- [ ] 3.7 Perform manual test: Reservation API and UI responses never expose CPF or phone number of any user.
- [ ] 3.8 Perform verification: Run `xano workspace push --dry-run` ensuring zero DROP statements occur before each push.
