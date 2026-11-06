# reservations-booking Specification

## Purpose
Gerencia a criação de reservas por clientes, listagem das próprias reservas e cancelamento, com validações de compatibilidade, horários, preços e concorrência.

## Requirements

### Requirement: Client reservation creation with compatibility and pricing
The Xano backend SHALL allow authenticated clients to create reservations with automated ceiling-hour pricing snapshots and strict vehicle-slot compatibility validation.

#### Scenario: Successful reservation creation
- **WHEN** a client creates a reservation with a valid future start, end after start, owned vehicle, slot in chosen location, compatible vehicle-slot type, and configured rate
- **THEN** the system calculates the price (hours rounded up × hourly rate), saves the reservation with active status and price snapshot, and returns success

#### Scenario: Vehicle and slot type compatibility validation
- **WHEN** a reservation is attempted where vehicle type is incompatible with slot type (e.g., moto in car slot, car in moto slot)
- **THEN** the system rejects the request with a validation error

#### Scenario: Past start time or invalid interval rejection
- **WHEN** a reservation start time is in the past or end time is not after start time
- **THEN** the system rejects the reservation

### Requirement: Concurrency control and conflict handling
The Xano backend SHALL prevent double booking by checking for overlapping active reservations immediately before insert and returning HTTP 409 upon conflict.

#### Scenario: Conflict returns HTTP 409
- **WHEN** a reservation is attempted for a slot that is already booked in an overlapping interval (`start < existing_end AND end > existing_start`)
- **THEN** the system rejects the request and returns status code 409 with a clear message

### Requirement: Personal listing and cancellation
The Xano backend SHALL allow clients to list their own reservations and cancel active ones, ensuring ownership and data privacy.

#### Scenario: Client lists own reservations without CPF or phone exposure
- **WHEN** a client requests their list of reservations
- **THEN** the system returns only their reservations and never exposes CPF or phone number of any user

#### Scenario: Successful cancellation by owner
- **WHEN** a client cancels their own active reservation
- **THEN** the system updates its status to "cancelled" while maintaining the record
