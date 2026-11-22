# Proposal

## Why

To enhance user experience and provide timely operational feedback, the Estacionamento Smart system needs automated notification capabilities. Users should receive notifications upon successful reservation booking, cancellation, and vehicle retrieval requests, and the system should support webhook notifications for integration with external monitoring or notification services.

## What Changes

- **Backend (Xano)**:
  - Implement automated email/webhook notification triggers upon successful reservation booking (`reservations-booking`), reservation cancellation, and vehicle retrieval request (`solicitar-retirada-veiculo`).
  - Add environment configuration support for notification webhooks (`NOTIFICATION_WEBHOOK_URL`) and email delivery via Xano's `util.send_email`.
- **Frontend (Streamlit)**:
  - Display success toast notifications and status updates in the UI when notifications are triggered.

## Capabilities

### New Capabilities
- `notifications`: Automated email and webhook notifications for reservations, cancellations, and vehicle retrieval events.

### Modified Capabilities
- (None - using new capability for notification management).

## Impact

- Backend API additions in Xano for notification dispatching.
- New capability specification (`notifications`).
