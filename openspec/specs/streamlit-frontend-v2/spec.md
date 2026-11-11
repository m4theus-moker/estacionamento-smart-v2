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
The Streamlit application SHALL provide an interactive grid or visual map of parking slots displaying status (free, occupied, user's reservation), vehicle type icons, and filtering options.

#### Scenario: Viewing slot map status
- **WHEN** a client or admin views slot availability for a location
- **THEN** the interface renders an interactive grid reflecting real-time slot occupancy and status categories.

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
