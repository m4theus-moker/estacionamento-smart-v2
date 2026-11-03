# Spec Delta

## Purpose

Define a interface de usuário em Streamlit que consome os endpoints REST do Xano para clientes e administradores.

## ADDED Requirements

### Requirement: Streamlit frontend user interface
The Streamlit frontend SHALL provide pages for user login/registration, client vehicle management, slot availability and reservations, and administrative management of locations, slots, rates, and reservations, communicating exclusively via Xano REST APIs.

#### Scenario: Client navigation and reservation flow
- **WHEN** a client logs into Streamlit and requests available slots for a location and period
- **THEN** Streamlit fetches and displays available slots from Xano and allows booking with owned vehicles

#### Scenario: Admin management view
- **WHEN** an administrator logs into Streamlit
- **THEN** Streamlit displays management views for locations, slots, rates, and all location reservations via Xano APIs
