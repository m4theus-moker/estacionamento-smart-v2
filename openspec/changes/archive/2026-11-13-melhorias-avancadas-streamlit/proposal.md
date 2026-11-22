# Proposal

## Why

The Estacionamento Smart application can be further elevated with professional interactive Plotly charts, automated End-to-End (E2E) UI testing with Playwright, webhook/email notification hooks for reservations, and a dynamic light/dark theme toggle in the sidebar.

## What Changes

- Integrate **Plotly** (`plotly.express` / `plotly.graph_objects`) for rich, interactive data visualizations in the Executive Dashboard (revenue trends, peak hours, occupancy distribution).
- Add a **Dynamic Theme Toggle** in the sidebar allowing users/admins to switch between dark and light themes.
- Implement **Webhook & Email Notification Triggers** upon reservation booking and cancellation.
- Setup **Playwright End-to-End Tests** for automated verification of UI workflows (login, booking, admin dashboard).

## Capabilities

### New Capabilities
- `streamlit-frontend-advanced`: Plotly charts, dynamic theme switcher, notification webhooks, and Playwright E2E test suite.

### Modified Capabilities
- `streamlit-frontend`: Enhanced visualization and testing capabilities.

## Impact
- Purely frontend Python enhancements (`app.py`, `ui/theme.py`, new E2E test directory). No backend database schema changes required.
