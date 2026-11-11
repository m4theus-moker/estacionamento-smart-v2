# Proposal

## Why

The current "Grid de Vagas Disponíveis" only lists free slots, making it difficult for users to understand the overall occupancy and context of a parking location during booking consultation. Replacing it with a comprehensive visual slot map showing all slots, their availability states, and user reservations enhances spatial awareness and UX.

## What Changes

- Replace the simple available slots grid in `page_consult_reservations` with an interactive visual slot map of ALL slots in the selected location.
- Render slots ordered by number with 3 distinct states: Livre (free), Indisponível (unavailable: vaga que o availability não devolveu para o veículo selecionado: ocupada por outra reserva OU incompatível com o tipo do veículo), and Sua reserva (user's own overlapping active reservation, ignoring reservations with status `cancelada`).
- Frontend calculation of states: Livre from availability endpoint (`GET /reservation/availability`), Indisponível from location slots (`GET /vaga`) minus free slots, Sua reserva from user reservations (`GET /reservation`) overlapping query time range (`start_res < end_query` and `end_res > start_query`), excluding cancelled reservations.
- Add slot type icons (car, moto, PCD, electric) and filtering controls by type and state (Livre, Indisponível, Sua reserva), updating the legend and filters accordingly.
- Include a summary header (e.g., "12 livres de 20") and a state legend.
- Clicking a free slot triggers the existing reservation confirmation flow; unavailable and user's reserved slots are non-clickable.
- Xano rate limit protection: max 3 API calls per consultation (location slots, availability, user reservations), cached in `st.session_state` with 60s TTL and a cache key including `location_id`, `vehicle_id`, `start_time`, and `end_time` (changing any parameter invalidates the cache). Plus an "Atualizar" button.
- Persistence of query parameters and consultation results in `st.session_state` so that changing filters or interacting with the screen does not make the map disappear on reruns.
- Clear error handling on API failure without rendering a partial map.
- Responsive grid (4-5 columns per row) using native Streamlit components (no HTML, no `unsafe_allow_html`).

## Capabilities

### New Capabilities
- None

### Modified Capabilities
- `streamlit-frontend-v2`: Enhance visual slot map requirement with 3-state inventory display (Livre, Indisponível, Sua reserva), filtering, rate-limit caching with compound key (`location_id`, `vehicle_id`, `start_time`, `end_time`), session state persistence, and native Streamlit grid rendering.

## Impact

- Frontend `app.py` (`page_consult_reservations`)
- No backend changes, no new tables, no new endpoints.
