# Proposal

## Why

The current slot consultation map presents a flat grid of slots, making it difficult for users to visualize the spatial arrangement of the parking lot (e.g., sectors, floors, or zones) across locations. Introducing a hierarchical "Planta Baixa" (Floor Plan / Sector Layout) structure organizes parking slots by sectors or zones, dramatically improving spatial awareness and professional parking management UX.

## What Changes

- Add sector/zone grouping to the parking slot consultation map in `page_consult_reservations`.
- Group slots by their respective location sectors/zones (or visual floor/corridor groupings) derived from location structure or metadata.
- Provide interactive floor plan navigation allowing users to filter and switch between sectors/zones of a parking location.
- Maintain the 3-state inventory display (Livre, Indisponível, Sua reserva), filtering, rate-limit caching, and session state persistence.
- Render sector-based slot groups clearly using native Streamlit components and visual icons.

## Capabilities

### New Capabilities
- None

### Modified Capabilities
- `streamlit-frontend-v2`: Enhance the visual slot map to support hierarchical sector/zone layout ("Planta Baixa") grouping slots by physical zones/sectors of the parking location.

## Impact

- Frontend `app.py` (`page_consult_reservations`)
- No backend changes required (utilizes existing location slots and metadata structure).
