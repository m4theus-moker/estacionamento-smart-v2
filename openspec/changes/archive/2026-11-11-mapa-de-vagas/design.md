# Design

## Context

See proposal.md - Why. The app uses Streamlit (`app.py`) communicating with Xano APIs (`XANO_PARKING_URL`, `XANO_API_URL`, `XANO_VEHICLES_URL`).

### Repository Empirical Checks
- **`GET /vaga?location_id={id}`**: Confirmed in `xano-pull-av/api/parking_management/vaga_GET.xs` (lines 1-19) and table schema in `xano-pull-av/table/vaga.xs` (lines 1-18). Accepts optional `location_id` and returns a list of slots containing `id`, `location_id`, `numero` (number), `tipo` (values: `carro`, `moto`, `pcd`, `eletrico`), `status` (values: `livre`, `ocupada`, `reservada`), and `created_at`. Note: The `status` field of the slot (`livre`, `ocupada`, `reservada`) is NOT used for classification; it is static, ignored. `POST /reservation` (`xano-pull-av/api/parking_management/reservation_POST.xs`, lines 1-122) does not update the slot status (estático, ignorado).
- **`GET /reservation/availability`**: Confirmed in `xano-pull-av/api/parking_management/reservation/availability_GET.xs` (lines 1-45). Accepts `location_id`, `vehicle_id`, `start_time`, and `end_time`. It validates vehicle ownership (`$vehicle.user_id == $auth.id`), requires vehicle type (`$vehicle.type`), validates time range (`start_time < end_time`), filters candidate slots matching vehicle type compatibility rules (`carro`/`eletrico`, `moto`, `pcd`/`carro`), and evaluates active overlapping reservations (`status == "ativa"`), returning only free compatible slots.
- **`GET /reservation`**: Confirmed in `app.py` (`page_my_reservations`) and Xano reservations endpoints. Returns the authenticated user's reservations containing `id`, `vaga_id`, `start_time`, `end_time`, `status`, etc., which is sufficient to determine user reservations locally (ignoring reservations with status `cancelada`).

## Goals / Non-Goals

**Goals:**
- Provide a comprehensive visual slot map showing all slots with empirical state classification (Livre, Indisponível, Sua reserva).
- Implement client-side state calculation, compound cache key including `location_id`, `vehicle_id`, `start_time`, and `end_time` (changing any parameter invalidates the cache), 60s TTL caching, and `st.session_state` persistence of consultation parameters and results to prevent map disappearance on rerun or filter change.
- Use strictly native Streamlit components without HTML.

**Non-Goals:**
- Changing backend endpoints, tables, or database schema.
- Implementing sectors, check-in, the 4-step wizard, dashboards, or admin panels.

## Decisions

### Decision: Client-side state classification vs backend aggregation
- **Choice**: Calculate slot states on the frontend using `GET /vaga?location_id={id}` (all slots), `GET /reservation/availability` (free slots), and `GET /reservation` (user active reservations, ignoring cancelled with status `cancelada`).
- **Rationale**: Avoids modifying backend code or endpoints while meeting the constraint of no new backend requirements.

### Decision: Handling slots excluded by availability
- **Choice**: Slots returned by `GET /vaga` that are excluded by `GET /reservation/availability` (defined as: vaga que o availability não devolveu para o veículo selecionado: ocupada por outra reserva OU incompatível com o tipo do veículo) are classified as `Indisponível` unless they belong to the user's active overlapping reservations (`Sua reserva`, ignoring cancelled reservations). The slot static `status` field in the database (`livre`, `ocupada`, `reservada`) is NOT used for classification; it is static, ignored. `POST /reservation` does not update it (estático, ignorado).
- **Rationale**: Keeps state classification robust and aligned with the availability endpoint logic.

### Decision: Caching strategy & session state persistence
- **Choice**: Cache location slots, availability, and user reservations in `st.session_state` with timestamp, 60s TTL, and a compound cache key including `location_id`, `vehicle_id`, `start_time`, and `end_time` (changing any parameter invalidates the cache). In addition, persist query parameters and consultation results in `st.session_state` so that changing filters or interacting with the screen does not wipe out the rendered map upon reruns.
- **Rationale**: Respects Xano free tier rate limits while ensuring smooth UI experience.

### Decision: Native UI components without HTML
- **Choice**: Use `st.container(border=True)`, `st.columns`, `st.badge`, `st.button`, `st.caption`, and `:material/...:` icons.
- **Rationale**: Adheres strictly to the main rule prohibiting HTML and `unsafe_allow_html`.

## Risks / Trade-offs

- [Client-side filtering lag with large slot counts] → Mitigated by typical small-to-medium parking lot sizes and efficient Python dict lookups.
- [Stale cache data] → Mitigated by 60s TTL, compound key validation, and manual "Atualizar" button.
