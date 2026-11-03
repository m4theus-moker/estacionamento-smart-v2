# Proposal

## Why

With parking locations, slots, and hourly rates fully implemented and administered via Xano and Streamlit, the Estacionamento Smart system now needs to provide complete parking reservation capabilities. This includes querying slot availability based on active reservation overlaps, booking reservations with automated ceiling-hour pricing snapshots and vehicle-slot compatibility validation, managing personal bookings and cancellations for clients, and administrative oversight and cancellation for admins, while ensuring robust concurrency handling and security (no CPF/phone exposure, strict role enforcement).

## What Changes

- **Reservations Availability (`reservations-availability`)**: Endpoints and UI integration for querying free slots by location, vehicle type, and period (start/end) based strictly on active reservation overlaps, without altering slot static status.
- **Reservations Booking (`reservations-booking`)**: Endpoints and UI ("Consultar & Reservar" and "Minhas Reservas") for clients to create reservations (with ceiling-hour pricing snapshots, vehicle-slot compatibility, past-start prohibition, and 409 conflict checks), list their own bookings, and cancel active reservations.
- **Reservations Admin (`reservations-admin`)**: Endpoints and UI ("Todas as Reservas") for administrators to list all system reservations and cancel any reservation, while denying access (`403`) to non-admin users.
- **Dependency & Deletion Guards**: Updating deletion guards for locations, slots, and rates to prevent deletion when active or historical reservations are linked.
- **Frontend Activation**: Enabling "Consultar & Reservar", "Minhas Reservas", and "Todas as Reservas" views in Streamlit now that endpoints are fully specified.

## Capabilities

### New Capabilities
- `reservations-availability`: Free slot availability queries based on active reservation overlaps by location, type, and period.
- `reservations-booking`: Client reservation creation, pricing calculation (ceiling hours × hourly rate), personal listing, and cancellation.
- `reservations-admin`: Administrative listing and cancellation of all system reservations with strict role checks (`403`).

### Modified Capabilities
- None.

## Impact

- **Backend / Xano**: New reservation endpoints in Xano using `XANO_PARKING_URL` and reviewing `./xano-pendente` assets before migration to `./xano-real`.
- **Frontend Streamlit**: Activation and full implementation of "Consultar & Reservar", "Minhas Reservas", and "Todas as Reservas" views.
- **Database / Models**: Reservation records storing user ownership (`$auth.id`), vehicle reference, slot reference, start/end timestamps in UTC, status (`active`, `cancelled`), and price snapshot.
