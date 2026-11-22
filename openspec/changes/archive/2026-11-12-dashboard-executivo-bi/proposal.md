# Proposal: Executive Dashboard & Business Intelligence (BI)

## Why

Currently, the Estacionamento Smart system operates primarily as a basic CRUD for parking management and reservations. To provide strategic value for parking administrators and business stakeholders, the system lacks real-time executive metrics, financial tracking (revenue, projections), peak hours heatmaps, average duration, and turnover indicators. Adding an Executive Dashboard & BI module transforms the platform into an enterprise-grade management tool, enabling data-driven decisions within the 10-day project window.

## What Changes

- Add an Executive Dashboard & BI administrative view with real-time KPIs and interactive charts filtered by location (unidade de estacionamento).
- Implement revenue tracking and projections (daily, weekly, monthly) per location.
- Implement occupancy rate metrics and peak hours analysis (movement heatmaps) per location.
- Track average ticket price and average parking duration per location.
- Implement vehicle turnover indicators (how many times each slot or the entire parking lot was utilized per day) per location.

## Capabilities

### New Capabilities
- `executive-dashboard`: Real-time executive metrics, financial BI, occupancy analytics, peak hours heatmaps, average duration/ticket, and turnover indicators for administrators.

### Modified Capabilities
- (None)

## Impact

- Adds new analytical data queries and visualization components using Streamlit / Plotly / Pandas.
- Enhances administrative backoffice capabilities without altering core reservation transactional flows.
- Leverages existing Xano tables (reservations, slots, locations, rates) to aggregate BI metrics.
