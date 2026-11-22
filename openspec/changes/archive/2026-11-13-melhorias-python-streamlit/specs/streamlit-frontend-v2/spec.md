# Streamlit Frontend v2 (Delta)

## ADDED Requirements

### Requirement: Floating Toast Notifications
The Streamlit frontend SHALL display floating toast notifications (`st.toast`) upon successful completion of key user actions (e.g., booking creation, vehicle addition, tariff update).

#### Scenario: Successful action triggers toast
- **WHEN** a user successfully completes a booking, vehicle registration, or rate update
- **THEN** the system triggers a floating toast notification informing the user of the success.

### Requirement: Short-term API Caching
The Streamlit frontend SHALL cache location list and tariff list requests using `st.cache_data` with a short TTL to prevent exceeding Xano rate limits.

#### Scenario: Fetching cached locations and tariffs
- **WHEN** the application requests location or tariff metadata repeatedly within the TTL window
- **THEN** cached data is returned without making redundant network calls.

### Requirement: Advanced Audit Logs Filtering
The administrative audit logs view SHALL provide search filtering by text and action type.

#### Scenario: Filtering audit logs
- **WHEN** an administrator enters search text or selects an action type filter in the audit logs page
- **THEN** the audit log table updates to display only matching entries.

### Requirement: CSV Report Export
The Executive Dashboard SHALL provide a CSV export download button (`st.download_button`) for filtered BI and revenue metrics.

#### Scenario: Downloading BI metrics as CSV
- **WHEN** an administrator clicks the export CSV button in the Executive Dashboard
- **THEN** the system generates and downloads a CSV file containing the current filtered financial and occupancy data.
