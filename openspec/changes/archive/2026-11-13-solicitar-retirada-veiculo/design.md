# Design

## Context
Adding the "Solicitar Retirada / Estou Chegando" feature to Estacionamento Smart.

## Architecture & Approach
- **Client Side**: In `page_my_reservations`, for active reservations, add a button "🚗 Solicitar Retirada". When clicked, update local session state or make API request (e.g., `PUT /reservation/{id}` with status `retirada_solicitada` or store in `st.session_state.pickup_requests`) and trigger notification webhook.
- **Admin Side**: In `page_admin_reservations`, add an alert box / queue displaying reservations where pickup has been requested.
- **Notifications**: Trigger `send_notification_webhook("VEHICLE_RETRIEVAL_REQUESTED", {"reservation_id": res_id})`.
