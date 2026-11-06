# Reservations Admin Spec

## Purpose

Gerencia o acesso administrativo para listagem de todas as reservas do sistema e cancelamento de qualquer reserva, além de travas de exclusão para locais, vagas e tarifas vinculadas.

## ADDED Requirements

### Requirement: Administrative reservation oversight and cancellation
The Xano backend SHALL provide endpoints for administrators to list all system reservations and cancel any reservation, enforcing strict administrator authorization (`role = admin`).

#### Scenario: Admin lists all reservations and cancels any reservation
- **WHEN** an authenticated administrator requests all system reservations or cancels any reservation
- **THEN** the system executes the operation successfully without exposing sensitive personal data (CPF/phone)

#### Scenario: Non-admin access denied with HTTP 403
- **WHEN** a client role user attempts to access administrative reservation endpoints
- **THEN** the system denies access and returns status code 403

### Requirement: Deletion guards for entities with linked reservations
The Xano backend SHALL prevent the deletion of locations, slots, or rates that have linked active or historical reservations.

#### Scenario: Deletion blocked for entities with reservations
- **WHEN** an administrator attempts to delete a location, slot, or rate linked to reservations
- **THEN** the system rejects the deletion and returns an error response
