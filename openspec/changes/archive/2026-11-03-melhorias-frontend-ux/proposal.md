# Proposal

## Why

The Estacionamento Smart Streamlit frontend requires comprehensive UX, bug fixes, and visual polish across its 4 screens (Login/Create Account, My Vehicles, Consult & Reserve, My Reservations). Users currently face unformatted timestamps, missing validation on forms, rigid UX patterns (e.g., vehicles form always expanded, no edit/delete confirmation), lack of visual feedback (status badges, pricing estimates, parking grid), and accessibility/aesthetic inconsistencies. These enhancements deliver a polished, responsive, and robust user experience aligned with the dark green theme (`#22c55e`).

## What Changes

- **Authentication Screen**:
  - Add "Esqueci minha senha" (Forgot password) recovery option.
  - Clear error messages and loading spinner/feedback on login/registration buttons.
  - Greeting uses user's first name or email prefix instead of full email.
- **Client Vehicles Screen**:
  - Automatically collapse "Adicionar veículo" expander by default when vehicles already exist.
  - Clear form fields after successful save.
  - Validate license plate format (old `ABC1234` and Mercosul `ABC1D23`) and year range (1980 to current year + 1), with clear error messages.
  - Add "Editar" (Edit) button on vehicle cards and confirmation before deletion.
  - Friendly empty state with action button when no vehicles are registered.
  - Vehicle cards styled with monospace plate + border and specific vehicle type icons (Car, Moto, PCD).
- **Consult & Reserve Screen**:
  - Set default end time to start time + 1h.
  - Validate that end time > start time and start time is not in the past.
  - Show estimated price before confirming reservation.
  - Display parking slots in a visual grid (free/busy), reusing the login screen parking aesthetic.
  - Encurtado sidebar label "Consultar & Reservar" to "Reservar".
- **My Reservations Screen**:
  - Format reservation dates from milliseconds timestamp to `dd/mm/aaaa HH:MM` (America/Sao_Paulo timezone).
  - Status displayed as clean badges (`ativa` = green, `cancelada` = red/gray, `concluída` = blue), capitalized without monospace.
  - Display reservation context in each card (location, slot, vehicle model + plate) instead of just "Reserva #N".
  - Sort reservations from newest to oldest.
  - Separate reservations into tabs: "Ativas" and "Histórico".
  - Require confirmation before canceling a reservation using `st.dialog`.
  - Friendly empty state with action button when no reservations exist.
- **General Frontend & Sidebar UI**:
  - Compact metrics cards with icons (Total, Cars, Motorcycles, PCD).
  - Sidebar icons for each nav item, truncated username with tooltip.
  - Improved contrast for placeholders and small labels, standardized spacing and field heights across screens.

## Capabilities

### New Capabilities
- None (all enhancements modify existing capabilities).

### Modified Capabilities
- `authentication`: Enhanced login/registration feedback, password recovery placeholder, and personalized user greeting.
- `client-vehicles`: Added validation (plate/year), form clearing, collapsible expander, edit/delete actions, vehicle card styling, and empty state.
- `parking-management`: Added default end time (+1h), time validation, price estimation, and visual parking slot grid.
- `reservations`: Added timestamp formatting (`dd/mm/aaaa HH:MM`, America/Sao_Paulo), status badges, rich reservation context cards, sorting, active/history tabs, cancellation confirmation dialog, and empty state.
- `streamlit-frontend`: Enhanced sidebar (icons, label, tooltip), compact metric cards, visual polish, and accessibility/contrast improvements.

## Impact

- **Codebase**: `app.py` (Streamlit frontend) will be updated with modular helper functions, validators, and UI component improvements.
- **APIs / Backend**: No backend schema changes required; relies existing Xano endpoints and data structures.
- **Dependencies**: No new external libraries introduced.
