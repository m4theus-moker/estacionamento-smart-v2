# Design

## Context
Extending the Streamlit frontend (`app.py`) with enhanced Python UI features: `st.toast` for user feedback, `st.cache_data` for location/tariff fetching, audit logs search & action filtering, and pandas/Streamlit CSV export for executive reports.

## Architecture & Approach
- **Toast Notifications**: Integrate `st.toast("...", icon="✅")` upon successful API mutations in respective pages (`page_consult_reservations`, `page_my_vehicles`, `page_admin_rates`, etc.).
- **API Caching**: Wrap location and tariff fetch helper functions in `st.cache_data(ttl=60)` to minimize HTTP requests to Xano.
- **Audit Logs Filtering**: Add text search input and action type dropdown in `page_admin_audit_logs` filtering the log records DataFrame.
- **CSV Export**: Convert BI metrics and report dataframes to CSV using Pandas (`df.to_csv(index=False).encode('utf-8')`) and serve via `st.download_button`.
