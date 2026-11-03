# Reservations Availability Spec

## Purpose

Gerencia a consulta de disponibilidade de vagas livres por local, tipo de veículo e período (início/fim), baseando-se estritamente em sobreposições de reservas ativas.

## ADDED Requirements

### Requirement: Availability check based on active reservation overlaps
The Xano backend SHALL determine slot availability in a location for a given period and vehicle type by verifying that no active reservations overlap with the requested interval.

#### Scenario: Slot is free when no overlapping active reservations exist
- **WHEN** availability is queried for a location, vehicle type, and period with no overlapping active reservations
- **THEN** the system returns the available slots

#### Scenario: Touching reservation intervals are accepted
- **WHEN** a reservation starts exactly when another active reservation ends (`start == existing_end` or `end == existing_start`)
- **THEN** the system considers the slot available for the new reservation

#### Scenario: Independence from slot status field
- **WHEN** availability is calculated
- **THEN** the slot's static status field does not dictate availability and is not altered by reservations
