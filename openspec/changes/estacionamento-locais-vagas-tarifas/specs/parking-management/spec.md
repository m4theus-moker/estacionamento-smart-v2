# Spec Delta

## Purpose

Gerencia o cadastro administrativo de locais de estacionamento, vagas por tipo (`carro`, `moto`, `pcd`, `eletrico`) e status (`livre`, `ocupada`, `reservada`), tarifas horárias (com `valor_hora > 0`), além da edição via modais (`st.dialog`), aplicando restrições de exclusão e autorização estrita de administrador (`403` para clientes).

## ADDED Requirements

### Requirement: Admin can manage parking locations (Create, List, Edit, Delete)
The backend SHALL provide endpoints via `XANO_PARKING_URL` for administrators to create, list, edit (`PUT /location/{id}`), and delete parking locations, ensuring that a location cannot be deleted if it has linked slots, rates, or reservations, and returning HTTP 403 for non-admin users.

#### Scenario: Successful location creation by administrator
- **WHEN** an authenticated administrator submits valid location details
- **THEN** the system creates the location and returns a success response

#### Scenario: Successful location update by administrator
- **WHEN** an administrator updates location details via `PUT /location/{id}`
- **THEN** the system updates the location successfully

#### Scenario: Deletion blocked for location with dependencies
- **WHEN** an administrator attempts to delete a location with linked slots, rates, or reservations
- **THEN** the system rejects the deletion and returns an error response

#### Scenario: Non-admin access denied with HTTP 403
- **WHEN** a client role user attempts to access administrative location endpoints
- **THEN** the system denies access and returns status code 403

### Requirement: Admin can manage parking slots per location (Create, List, Edit, Delete)
The backend SHALL provide endpoints via `XANO_PARKING_URL` for administrators to create, list, and edit (`PUT /vaga/{id}`) parking slots within a location, validating slot number uniqueness per location, vehicle type (`carro`, `moto`, `pcd`, `eletrico`), and status (`livre`, `ocupada`, `reservada`), including `location_id`.

#### Scenario: Successful slot creation or update
- **WHEN** an administrator creates or updates a slot with `location_id`, unique number, valid type, and status
- **THEN** the system saves or updates the slot associated with that location

#### Scenario: Slot number uniqueness per location
- **WHEN** an administrator creates a slot with a number already existing in that location
- **THEN** the system rejects the creation due to uniqueness constraint

### Requirement: Admin can manage hourly rates per location and vehicle type (Create, List, Edit, Delete)
The backend SHALL provide endpoints via `XANO_PARKING_URL` for administrators to define, update (`PUT /tarifa/{id}`), and delete hourly rates for each vehicle type (`carro`, `moto`, `pcd`, `eletrico`) within a location, requiring `location_id` and validating `valor_hora > 0`.

#### Scenario: Successful rate definition or update
- **WHEN** an administrator sets a valid hourly rate (`valor_hora > 0`) for a specific vehicle type and `location_id`
- **THEN** the system saves or updates the rate successfully

#### Scenario: Rate validation failure for zero or negative values
- **WHEN** an administrator attempts to set `valor_hora <= 0`
- **THEN** the system rejects the request with an input error
