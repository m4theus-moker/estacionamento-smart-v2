# Specification: Vehicle Retrieval Request (`vehicle-retrieval`)

## ADDED Requirements

### Requirement: Client Vehicle Pickup Request Button
The client reservations view SHALL display a "Solicitar Retirada / Estou Chegando" button for active reservations.

#### Scenario: Client clicks vehicle pickup request
- **WHEN** a client clicks the pickup request button on an active reservation
- **THEN** the reservation status updates to indicate retrieval is requested and a success toast is displayed.

### Requirement: Administrative Pickup Queue
The administrator reservations dashboard SHALL include a real-time pickup queue showing vehicles requested for retrieval by clients.

#### Scenario: Admin views pickup queue
- **WHEN** an administrator views the reservations or operations dashboard
- **THEN** all reservations with pending pickup requests are listed with vehicle details, slot, and request timestamp.
