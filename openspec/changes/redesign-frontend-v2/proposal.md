# Proposal

## Why

The current Streamlit frontend of "Estacionamento Smart" requires a visual and usability overhaul to deliver a modern, polished, and intuitive experience while strictly respecting Xano's free tier rate limits (10 requests per 20s), dark theme aesthetics (#030504 background, #22c55e green accents), and robust caching (`st.session_state` with 60s max TTL). A structured design system (`ui/theme.py`), multi-step reservation flow, visual slot map, client dashboard with time countdown, and enhanced admin panels will significantly elevate user satisfaction and operational clarity.

## What Changes

- **Design System & Components (`ui/theme.py`)**:
  - Unified theme and reusable UI components (cards, status badges, metric cards, empty states, styled vehicle plates).
  - High-contrast typography and icon-driven sidebar navigation with concise labels.
- **Multi-Step Reservation Flow**:
  - 4-step guided booking flow (Local -> Vehicle -> Schedule -> Confirmation) with real-time validations, pricing preview, and success screen with ticket viewing.
- **Visual Slot Map**:
  - Interactive grid/map of parking slots displaying status (free, occupied, user's reservation), vehicle type icons, and filtering options.
- **Client Dashboard**:
  - Active reservation card with live countdown/remaining time, "Book again" quick action, fleet summary, and personalized greeting with the user's first name.
- **Polishing & UX Enhancements**:
  - Toasts, spinners, `st.dialog` confirmations, empty states, vehicle card editing, and responsive layout.
- **Admin Panel Redesign**:
  - Overview of occupancy, today's reservations list, and revenue per period metrics.

## Capabilities

### New Capabilities
- `streamlit-frontend-v2`: Modernized Streamlit UI, design system components, 4-step booking flow, visual slot map, client dashboard, and enhanced admin panel.

### Modified Capabilities
- (None - using new capability for frontend redesign).

## Impact

- Frontend modularization (`ui/theme.py` and component helpers) without altering backend schemas, REST APIs, or adding unapproved external libraries.
- Strict adherence to Xano rate limits (data on demand, 60s TTL session caching) and security (`html.escape()` for all API data rendered in HTML).
