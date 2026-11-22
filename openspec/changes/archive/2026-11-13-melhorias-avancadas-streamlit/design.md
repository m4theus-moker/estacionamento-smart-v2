# Design

## Context
Extending Estacionamento Smart with professional Plotly charts, dynamic theme switching, webhook notifications, and Playwright E2E tests.

## Architecture & Approach
- **Plotly Charts**: Replace `st.bar_chart` and `st.line_chart` with `st.plotly_chart(px.bar(...))` and `px.line(...)` styled consistently with the parking theme.
- **Dynamic Theme Toggle**: Add `st.sidebar.selectbox` or `st.sidebar.toggle("Modo Escuro", value=True)` in `ui/theme.py` and `app.py` to adjust CSS variables dynamically.
- **Webhook Notifications**: Add a helper `send_notification_webhook(event_type, data)` that sends a POST request to an optional `NOTIFICATION_WEBHOOK_URL` configured in `.env`.
- **Playwright E2E Tests**: Add `tests/e2e/` with Playwright python test scripts (`test_e2e_app.py`) for automated UI testing.
