# Proposal: Solicitar Retirada de Veículo (Estou Chegando)

## Why

To enhance customer experience and operational efficiency, clients should be able to notify the parking management system when they are heading to pick up their vehicle ("Estou Indo Buscar / Solicitar Retirada"). This alerts operators and prepares the vehicle/gate release in advance, reducing wait times.

## What Changes

- Add a **"🚗 Solicitar Retirada / Estou Chegando"** action button in the client's "Minhas Reservas" view for active reservations.
- Introduce a new reservation status or flag (`solicitando_retirada` / `retirada_solicitada`) communicated via API.
- Add an administrative **"Fila de Retiradas"** queue panel in the admin views to monitor vehicles requested for pickup.
- Trigger notification webhooks on vehicle retrieval requests.

## Capabilities

### New Capabilities
- `vehicle-retrieval`: Client vehicle pickup request flow and operator pickup queue.

### Modified Capabilities
- `reservations`: Added vehicle retrieval state and notification triggers.

## Impact
- Frontend updates (`app.py`) and backend API integration or simulated frontend state handling for vehicle pickup requests.
