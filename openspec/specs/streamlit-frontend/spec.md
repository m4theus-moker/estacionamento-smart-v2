# Streamlit Frontend

## Purpose

Define a interface de usuário em Streamlit que consome os endpoints REST do Xano para clientes e administradores.

## Requirements

### Requirement: Streamlit frontend user interface
The Streamlit frontend SHALL provide pages for user login/registration, client vehicle management, slot availability and reservations, and administrative management of locations, slots, rates, and reservations, communicating exclusively via Xano REST APIs. The frontend SHALL feature compact metrics cards with icons, distinct sidebar item icons, truncated usernames with tooltips, improved contrast for placeholders/labels, and standardized spacing and field heights across screens.

#### Scenario: Client navigation and reservation flow
- **WHEN** a client logs into Streamlit and requests available slots for a location and period
- **THEN** Streamlit fetches and displays available slots from Xano and allows booking with owned vehicles

#### Scenario: Admin management view
- **WHEN** an administrator logs into Streamlit
- **THEN** Streamlit displays management views for locations, slots, rates, and all location reservations via Xano APIs

#### Scenario: Frontend layout and UX enhancements
- **WHEN** any user navigates the Streamlit app
- **THEN** the sidebar displays icons, shortened nav label, truncated username with tooltip, metrics cards are compact with icons, and contrast/spacing are standardized.
