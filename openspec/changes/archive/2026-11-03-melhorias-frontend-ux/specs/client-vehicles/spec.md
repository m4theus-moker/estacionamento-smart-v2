# Spec Delta

## MODIFIED Requirements

### Requirement: Client can manage own vehicles
The Xano backend SHALL allow authenticated clients to register, list, and delete their own vehicles, ensuring that a vehicle belongs solely to the client who registered it. The Streamlit frontend SHALL validate license plates (old `ABC1234` and Mercosul `ABC1D23`), restrict years (1980 to current year + 1), clear the form after saving, collapse the "Adicionar veículo" expander by default when vehicles exist, provide edit and delete confirmation actions, display styled vehicle cards with monospace plate/border and vehicle type icons, and show a friendly empty state.

#### Scenario: Successful vehicle registration
- **WHEN** an authenticated client registers a vehicle with valid plate and type
- **THEN** the system saves the vehicle associated exclusively with that client

#### Scenario: Client can only view own vehicles
- **WHEN** a client requests the list of vehicles
- **THEN** the system returns only the vehicles belonging to the logged-in user

#### Scenario: Vehicle form validation and UX enhancements
- **WHEN** a client adds or edits a vehicle with invalid plate or year outside 1980-(current+1)
- **THEN** the Streamlit frontend displays clear error messages, clears form fields on successful save, collapses the add expander when vehicles exist, and requires confirmation before deletion.
