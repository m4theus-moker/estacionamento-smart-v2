# Design: Executive Dashboard & Business Intelligence (BI)

## Context

See `proposal.md` - Why. The system currently features a Streamlit frontend (`app.py`), Xano backend endpoints for locations, slots, tariffs, and reservations, and helper modules like `slot_map.py`. To fulfill the 10-day timeline and deliver high-impact executive insights without complex external BI tooling, we will implement analytical aggregation in Python (using Pandas and Streamlit native components / Altair) directly consuming existing API endpoints and data structures.

## Repository Empirical Checks

- **Admin Reservations Endpoint**: `xano-pull-av/api/parking_management/admin/reservation_GET.xs` (lines 1-30).
  - *Accepts filter by location*: Yes (`$input.location_id`).
  - *Accepts period filter*: No (returns all reservations for the location; date/period filtering is performed client-side in Python/Pandas).
  - *Pagination*: None (returns `{type: "list"}` as a complete array).
  - *Fields returned*: `price`, `start_time`, `end_time`, `status`, `vaga_id`, `location_id`, `created_at`, `user_id`, `vehicle_id`, `ticket_code`, etc.
  - *Authorization*: Requires user role == "admin".

## Dependencies & Chart Rendering

- **Packages**: `pandas` is installed in the Python environment (though not explicitly in `requirements.txt`). `plotly` is NOT installed and NOT required.
- **Rendering Strategy**: Prioritize Streamlit native components (`st.metric`, `st.bar_chart`, `st.line_chart`) and Altair (built into Streamlit). Do not install new packages without explicit user approval.

## Caching Strategy

- **Session State Caching**: Replace `@st.cache_data` (which is shared globally across users) with `st.session_state` combined with a timestamp, 60-second TTL, and a manual "Atualizar" button.
- **Cache Key**: Must include `location_id` and period range to prevent cross-filter contamination.

## Metric Definitions

1. **Faturamento**: Sum of `price` across all reservations where `status` is NOT 'cancelada' / 'cancelado', grouped by reservation start date (`America/Sao_Paulo` timezone).
2. **Projeção de Faturamento**: Simple linear projection formula: `(Revenue so far in month / Elapsed days in month) * Total days in current month`.
3. **Ocupação Atual**: Number of active reservations right now (`start_time <= now < end_time` and `status == 'ativa'`) divided by total slots registered for the location.
4. **Ticket Médio**: Total valid revenue divided by total count of valid (non-cancelled) reservations.
5. **Tempo Médio de Permanência**: Average of reserved duration per reservation (`end_time - start_time` converted to hours/minutes).
6. **Rotatividade (Turnover)**: Total reservations per slot per day. *(Note: The database tracks reservations, not physical check-in/check-out events; therefore, this measures reservation turnover rather than physical physical rotation).*

## Architecture & Module Structure

- **`bi_metrics.py`**: New pure Python module containing standalone calculation functions (no Streamlit dependency), fully unit-tested with pytest in `tests/test_bi_metrics.py` following the exact pattern of `slot_map.py`.
- **`app.py`**: Streamlit UI renders charts and metrics using `bi_metrics.py` outputs. Access is strictly restricted to users with `role == 'admin'`.

## Goals / Non-Goals

**Goals:**
- Provide a location selector to filter all BI metrics by specific parking units (locais).
- Provide real-time financial tracking (daily, weekly, monthly revenue and projections) per location.
- Compute and render occupancy rate analytics and peak hours distribution using reservation timestamps per location.
- Calculate average ticket price and average parking duration per location.
- Display vehicle turnover rates per slot and for the parking lot overall per location.
- Integrate smoothly into the administrative section of `app.py`.

**Non-Goals:**
- Implementing complex multi-tenant data warehousing or external OLAP cubes.
- Real-time WebSocket streaming for BI metrics (polling or on-demand page load aggregation is sufficient).
- Automated payment gateway reconciliation.

## Decisions

- **Decision 1: Use Pandas & Streamlit Native Components / Altair for BI Aggregation**
  - *Rationale*: Leverages Python's powerful data manipulation libraries directly within the existing Streamlit app architecture without adding heavy infrastructure dependencies or uninstalled packages like Plotly.
  - *Alternatives considered*: External BI tools (PowerBI/Metabase) or Plotly — rejected due to complexity, uninstalled package dependencies, and tight 10-day delivery window.

- **Decision 2: Client-side/App-side Aggregation from Admin API Endpoints**
  - *Rationale*: Fetch reservation, slot, and tariff data from `admin/reservation` endpoint and aggregate metrics in memory using Pandas.
  - *Alternatives considered*: Creating custom SQL views in Xano — rejected to avoid modifying database schemas directly when endpoints already provide raw lists.

## Risks / Trade-offs

- [Performance with large datasets] → Mitigation: Cache aggregated data frames using `st.session_state` with 60s TTL and manual refresh button.
- [Incomplete reservation timestamps] → Mitigation: Robust datetime parsing (similar to `slot_map.py`) with fallback defaults for missing start/end times.

