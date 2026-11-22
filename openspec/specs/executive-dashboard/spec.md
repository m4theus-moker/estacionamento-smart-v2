# executive-dashboard Specification

## Purpose
Provides administrative users with an Executive Dashboard & Business Intelligence (BI) view featuring real-time financial tracking, occupancy rate analytics, peak hours movement heatmaps, average duration/ticket metrics, vehicle turnover indicators, location filtering, caching, and strict admin access control.

## Requirements

### Requirement: Administrative Access Control
The Executive Dashboard SHALL restrict access strictly to users with the 'admin' role, displaying an access denied notice for regular client users.

#### Scenario: Client user attempts to access Executive Dashboard
- **WHEN** a user with 'cliente' role tries to view the Executive Dashboard
- **THEN** the system denies access and displays an access restricted warning

### Requirement: Location Selection and Filtering
The system SHALL provide a location selector in the Executive Dashboard allowing administrators to filter all BI metrics, revenue reports, occupancy rates, and turnover indicators by a specific parking location (unidade).

#### Scenario: Selecting a parking location for BI metrics
- **WHEN** an administrator selects a specific location from the location dropdown in the dashboard
- **THEN** all financial KPIs, occupancy charts, and turnover indicators update to reflect data exclusively for that location

### Requirement: Session State Caching & Manual Refresh
The system SHALL cache aggregated metrics in `st.session_state` with a 60-second TTL and a manual "Atualizar" button, keyed by location and period.

#### Scenario: Manual refresh of dashboard data
- **WHEN** an administrator clicks the "Atualizar" button
- **THEN** the session cache is invalidated and fresh metrics are recomputed from the API

### Requirement: Financial Tracking and Revenue Projections
The system SHALL calculate and display daily, weekly, and monthly revenue (sum of non-cancelled reservation prices in America/Sao_Paulo timezone) and linear monthly projections.

#### Scenario: Viewing revenue and projections
- **WHEN** an administrator views the financial KPIs section
- **THEN** the system shows accurate accumulated revenue for today, week, month, and projected month-end revenue

### Requirement: Occupancy Rate Analytics
The system SHALL calculate and display current occupancy rate as active reservations right now divided by total location slots.

#### Scenario: Viewing current occupancy
- **WHEN** an administrator checks occupancy analytics
- **THEN** the system displays the percentage and count of currently occupied slots vs total slots

### Requirement: Average Ticket Price and Parking Duration
The system SHALL calculate and display average ticket price (total valid revenue divided by reservation count) and average reserved parking duration (`end_time - start_time`).

#### Scenario: Checking ticket and duration averages
- **WHEN** an administrator reviews operational metrics
- **THEN** the system shows average ticket value and average stay duration

### Requirement: Peak Hours Movement Heatmap
The system SHALL generate a peak hours movement heatmap based on reservation start timestamps across days of the week.

#### Scenario: Viewing peak hours distribution
- **WHEN** an administrator views the peak hours section
- **THEN** the system displays a distribution chart identifying high-demand time windows

### Requirement: Vehicle Turnover Indicators
The system SHALL calculate and display reservation turnover per slot and overall lot turnover per day.

#### Scenario: Viewing slot turnover
- **WHEN** an administrator inspects turnover metrics
- **THEN** the system lists reservation counts per slot per day

### Requirement: Graceful Empty States and Data Robustness
The system SHALL handle locations with zero reservations, empty periods, or incomplete reservation data gracefully without runtime exceptions.

#### Scenario: Viewing dashboard for an empty location or period
- **WHEN** an administrator selects a location or period with no reservations
- **THEN** the system displays zeroed metrics and an informative empty state message instead of crashing
