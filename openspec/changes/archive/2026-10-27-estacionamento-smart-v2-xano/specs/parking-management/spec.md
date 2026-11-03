# Spec Delta

## Purpose

Gerencia o cadastro de locais, vagas por tipo (carro, moto, pcd) e tarifas horárias no Xano, garantindo integridade de dados e restrições de exclusão.

## ADDED Requirements

### Requirement: Admin can manage parking locations, slots, and rates
The Xano backend SHALL provide endpoints for administrators to create, list, and delete parking locations, slots, and rates, ensuring that a location cannot be deleted if it has linked slots, rates, or reservations.

#### Scenario: Successful location creation
- **WHEN** an administrator submits valid location details
- **THEN** the system creates the location and returns a success response

#### Scenario: Deletion blocked for location with dependencies
- **WHEN** an administrator attempts to delete a location with linked slots, rates, or reservations
- **THEN** the system rejects the deletion and returns an error response

#### Scenario: Slot uniqueness per location
- **WHEN** an administrator creates a slot with a number already existing in that location
- **THEN** the system rejects the creation due to slot number uniqueness constraint within the location

#### Scenario: Rate restriction per slot type and location
- **WHEN** an administrator defines multiple rates for the same vehicle type in the same location
- **THEN** the system restricts it to ensure only one rate per type per location
