# Spec Delta

## Purpose

Gerencia a consulta de disponibilidade de vagas, criação de reservas com cálculo de preço e prevenção de conflitos, além do cancelamento por clientes e administradores.

## ADDED Requirements

### Requirement: Availability check based on active reservations
The Xano backend SHALL determine slot availability in a location for a given period by verifying that no active reservations overlap with the requested interval.

#### Scenario: Slot is free when no overlapping reservations exist
- **WHEN** availability is queried for a location and period with no overlapping active reservations
- **THEN** the system returns the available slots

#### Scenario: Touching reservation intervals are accepted
- **WHEN** a reservation starts exactly when another active reservation ends
- **THEN** the system considers the slot available for the new reservation

### Requirement: Reservation creation with concurrency control and pricing
The Xano backend SHALL calculate reservation prices by rounding up hours and multiplying by the local rate, rejecting past start times, invalid vehicle ownership, or conflicting intervals using robust concurrency locks.

#### Scenario: Successful reservation creation
- **WHEN** a client creates a reservation with valid future start, end (after start), owned vehicle, and slot in the chosen location with a defined rate
- **THEN** the system calculates the price, saves the reservation with active status, and returns success

#### Scenario: Conflict returns HTTP 409
- **WHEN** a reservation is attempted for a slot that is already booked in the overlapping interval
- **THEN** the system rejects the request and returns status code 409

#### Scenario: Refusal when no rate is defined
- **WHEN** a reservation is requested for a vehicle type without a configured rate in that location
- **THEN** the system rejects the reservation

### Requirement: Reservation cancellation
The Xano backend SHALL allow clients to cancel their own reservations and administrators to cancel any reservation, updating the status to cancelled while maintaining the record.

#### Scenario: Successful cancellation by owner
- **WHEN** a client cancels their own active reservation
- **THEN** the system updates its status to cancelled
