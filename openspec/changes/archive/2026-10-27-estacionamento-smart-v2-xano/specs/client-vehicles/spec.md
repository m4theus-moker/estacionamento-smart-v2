# Spec Delta

## Purpose

Gerencia o cadastro e vínculo exclusivo de veículos aos respectivos clientes no Xano.

## ADDED Requirements

### Requirement: Client can manage own vehicles
The Xano backend SHALL allow authenticated clients to register, list, and delete their own vehicles, ensuring that a vehicle belongs solely to the client who registered it.

#### Scenario: Successful vehicle registration
- **WHEN** an authenticated client registers a vehicle with valid plate and type
- **THEN** the system saves the vehicle associated exclusively with that client

#### Scenario: Client can only view own vehicles
- **WHEN** a client requests the list of vehicles
- **THEN** the system returns only the vehicles belonging to the logged-in user
