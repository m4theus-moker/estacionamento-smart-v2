# Proposal

## Why

The Estacionamento Smart Streamlit frontend can be further polished and optimized for performance and usability entirely in Python, adding toast notifications for feedback, short-term caching for API stability against Xano rate limits, advanced filtering in audit logs, and CSV report exports for administrators.

## What Changes

- Add floating toast notifications (`st.toast`) for successful actions (booking confirmation, vehicle registration, tariff updates).
- Implement short-term caching (`st.cache_data` with TTL) for location and tariff data fetching to respect Xano rate limits (10 req/20s).
- Add text search and action type filters to the audit logs administrative view.
- Add CSV export functionality (`st.download_button`) for Executive Dashboard financial and occupancy metrics.

## Capabilities

### New Capabilities

### Modified Capabilities
- `streamlit-frontend-v2`: Add UI feedback toasts, API caching, audit log filtering, and CSV report export.

## Impact
- Purely frontend Python (`app.py`). No backend database or Xano schema changes.
