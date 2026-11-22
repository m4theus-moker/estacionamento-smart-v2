# Design

## Context

See proposal.md - Why. The system uses Xano for backend endpoints and Streamlit for frontend UI. We want to leverage Xano's `util.send_email` and webhook integration capabilities (`NOTIFICATION_WEBHOOK_URL`).

## Goals / Non-Goals

**Goals:**
- Trigger automated emails and webhooks on booking, cancellation, and vehicle retrieval requests.
- Ensure notification failures do not break core transaction flows.

**Non-Goals:**
- Real-time WebSockets notifications.
- SMS or push notification gateways.

## Decisions

- **Asynchronous / Non-blocking Dispatch**: Notification triggers in Xano endpoints will be wrapped or handled such that if webhook/email delivery fails or times out, the core booking/cancellation transaction completes successfully.
- **Environment Config**: Use `NOTIFICATION_WEBHOOK_URL` from environment/secrets.

## Risks / Trade-offs

- [External API Failure / Timeout] → Mitigation: Wrap notification dispatches in error handlers so core actions never fail due to notification dispatch issues.
