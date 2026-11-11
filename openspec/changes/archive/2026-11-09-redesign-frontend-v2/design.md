# Design

## Context

- The Streamlit frontend currently interacts with Xano REST endpoints via `backend/database.py` or direct requests.
- Constraints: Xano free tier rate limit (10 requests per 20 seconds) requires robust caching (`st.session_state` with max 60s TTL) and batching data fetches on demand.
- Visual theme: Dark theme (`#030504` background, `#22c55e` green accents) using custom CSS and Streamlit components.

## Goals / Non-Goals

**Goals:**
- Modularize UI components into `ui/theme.py` and reusable helper modules.
- Implement a 4-step reservation wizard (`st.session_state`-driven).
- Provide visual slot grid mapping and active reservation countdown timers.
- Maintain full compatibility with existing Xano backend APIs without modifying backend logic.

**Non-Goals:**
- Modifying Xano database tables or backend REST endpoints.
- Introducing heavy external frontend frameworks outside Streamlit.

## Decisions

- **UI Component Modularization (`ui/theme.py`)**:
  - *Choice*: Create a dedicated `ui/theme.py` module containing custom CSS injections, color variables, metric cards, status badge generators, and vehicle plate formatters.
  - *Alternatives considered*: Inline CSS in every page (rejected due to code duplication and inconsistency).
- **State Management for Multi-Step Booking**:
  - *Choice*: Use `st.session_state` to track wizard steps (`step_index`), selected location, selected vehicle, and schedule parameters.
  - *Alternatives considered*: Separate pages with URL query params (rejected due to Streamlit page navigation limitations and state loss).
- **Caching & Rate Limit Protection**:
  - *Choice*: Cache API calls in `st.session_state` with a 60-second TTL and explicit refresh buttons.
  - *Alternatives considered*: Live polling without cache (rejected due to triggering Xano free tier rate limits).
- **Mapa de Vagas**:
  - *Choice*: Usar `GET /vaga?location_id={id}` para listar todas as vagas e o `availability GET` (que devolve só as livres) para marcar as demais como ocupadas. Sem campo de setor: grade simples por número. Três estados: livre, ocupada, sua reserva.
- **Contador Regressivo**:
  - *Choice*: Calcular o tempo restante localmente a partir do `end_time` já em cache (sem chamar a API a cada atualização).

## Risks / Trade-offs

- [Rate Limit Exceeded] → Mitigation: Implement aggressive session caching (`st.cache_data` / `st.session_state` TTL) and avoid redundant API calls on re-renders.
- [State Desync in Wizard] → Mitigation: Validate inputs at each step before allowing progression to the next step in `st.session_state`.
