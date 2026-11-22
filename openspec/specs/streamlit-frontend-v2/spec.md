# streamlit-frontend-v2 Specification

## Purpose
Modernize the Streamlit frontend with a design system (`ui/theme.py`), 4-step guided booking flow, visual slot map, active reservation client dashboard with countdown, and enhanced admin panels while respecting Xano free tier rate limits.

## Requirements

### Requirement: Design system and theme components
The Streamlit application SHALL provide a unified design system (`ui/theme.py`) featuring consistent color schemes (dark theme #030504 background, #22c55e green accents), reusable UI components (cards, status badges, metric cards, empty states, vehicle plates), and icon-driven sidebar navigation.

#### Scenario: Consistent theme rendering
- **WHEN** the Streamlit application loads or navigates between pages
- **THEN** it applies the centralized theme styling, custom CSS classes, and structured component helpers consistently.

### Requirement: Multi-step reservation booking flow
The Streamlit application SHALL provide a guided 4-step reservation booking flow (Local -> Vehicle -> Schedule -> Confirmation) with real-time validations, pricing preview, and success screen with ticket viewing.

#### Scenario: Guided booking flow execution
- **WHEN** a client initiates a new reservation
- **THEN** they progress through location selection, vehicle selection, date/time scheduling, and a final confirmation screen with pricing and ticket preview.

### Requirement: Visual slot map
The Streamlit application SHALL provide an interactive grid or visual map of all parking slots within a selected location, displaying 3 states (Livre, Indisponível, Sua reserva), vehicle type icons, summary counts, session state persistence, compound key 60s TTL caching, and filtering options by type and state.

#### Scenario: Viewing slot map status
- **WHEN** a client or admin views slot availability for a location
- **THEN** the interface renders an interactive grid reflecting real-time slot occupancy and status categories.

#### Scenario: Viewing slot map status with 3 states
- **WHEN** a client or admin views slot availability for a location and time range
- **THEN** the interface renders an interactive grid of all location slots categorized into Livre, Indisponível, and Sua reserva states.

#### Scenario: Slot state classification - Livre
- **WHEN** a slot is returned by the availability endpoint (`GET /reservation/availability`) for the selected vehicle and period
- **THEN** it is classified and rendered as **Livre** (free and selectable).

#### Scenario: Slot state classification - Indisponível
- **WHEN** a slot from location slots (`GET /vaga`) is not returned by the availability endpoint for the selected vehicle
- **THEN** it is classified and rendered as **Indisponível** (defined as a slot that availability did not return for the selected vehicle: ocupada por outra reserva OU incompatível com o tipo do veículo, and non-clickable).

#### Scenario: Slot state classification - Sua reserva
- **WHEN** a slot belongs to an active overlapping reservation of the authenticated user (`GET /reservation`), ignoring any reservations with status `cancelada`
- **THEN** it is classified and rendered as **Sua reserva** (non-clickable).

#### Scenario: Slot unavailable or user's reservation is not clickable
- **WHEN** o usuário vê uma vaga Indisponível ou Sua reserva
- **THEN** nenhum botão de seleção é exibido.

#### Scenario: Filtering slot map by type and state
- **WHEN** the user applies filters for vehicle type or slot state (Livre, Indisponível, Sua reserva) on the slot map
- **THEN** the grid updates dynamically to display only the matching slots, and the legend reflects the states.

#### Scenario: Caching and rate limit protection with compound key
- **WHEN** slot availability, location slots, and user reservations are fetched
- **THEN** results are cached in session state with a 60s TTL using a compound cache key including `location_id`, `vehicle_id`, `start_time`, and `end_time` (changing any parameter invalidates the cache), refreshed via a manual update button, limiting API calls to a maximum of 3 per query.

#### Scenario: Session state persistence of consultation and map
- **WHEN** consultation parameters or UI filters/interactions change
- **THEN** query parameters and results are persisted in `st.session_state` so that the slot map does not disappear upon page reruns.

#### Scenario: API failure handling without partial map
- **WHEN** any of the required API calls for slot map data fail
- **THEN** the application displays a clear error message and prevents rendering an incomplete or partial map.

### Requirement: Client dashboard and live countdown
The Streamlit application SHALL provide a personalized client dashboard featuring a greeting with the user's first name, fleet summary, quick action shortcuts, and active reservation card with live remaining time countdown.

#### Scenario: Client dashboard display
- **WHEN** a client logs in and views their dashboard
- **THEN** they see their greeting, active reservations with countdown timers, fleet summary, and quick booking actions.

### Requirement: Admin panel redesign
The Streamlit application SHALL provide an enhanced administrative panel overview with occupancy metrics, today's reservations list, and revenue per period analytics.

#### Scenario: Admin overview access
- **WHEN** an administrator accesses the admin management panel
- **THEN** they view aggregated occupancy stats, daily reservations, and revenue metrics across locations.

### Requirement: Floor plan sector layout
The Streamlit application SHALL provide a hierarchical floor plan ("Planta Baixa") grouping parking slots by location sectors or zones, displaying empirical status, vehicle type icons, filtering options, and summary statistics across sector tabs.

#### Scenario: Viewing slots grouped by sector in a floor plan
- **WHEN** a client or admin views slot availability for a location in the consultation page
- **THEN** the interface groups and displays parking slots by their respective sectors or zones (Planta Baixa) with state badges, summary counts, and filtering controls.
