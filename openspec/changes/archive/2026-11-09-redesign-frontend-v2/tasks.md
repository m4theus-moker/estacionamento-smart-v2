# Tasks

## 1. Design System and Theme Module

- [ ] 1.1 Create `ui/theme.py` with centralized dark theme CSS styling, custom color variables, metric cards, status badges, and vehicle plate formatting functions, and verify import succeeds.
- [ ] 1.2 Add reusable component helpers for empty states and icon-driven sidebar navigation in `ui/theme.py` and verify component rendering.

## 2. Multi-Step Reservation Booking Flow

- [ ] 2.1 Implement the 4-step reservation wizard (`st.session_state`-driven: Local -> Vehicle -> Schedule -> Confirmation) with real-time validation and pricing preview, and verify step progression works correctly.
- [ ] 2.2 Add success screen with ticket viewing and confirmation dialogs for bookings, and verify ticket generation and rendering.

## 3. Visual Slot Map and Client Dashboard

- [ ] 3.1 Implement visual slot grid map displaying status (free, occupied, user's reservation), vehicle type icons, and filtering options, and verify grid renders correctly.
- [ ] 3.2 Implement personalized client greeting, fleet summary, quick action shortcuts, and active reservation card with live remaining time countdown, and verify dashboard displays correct data.

## 4. Admin Panel Redesign and Verification

- [ ] 4.1 Redesign the administrator management panel overview with occupancy metrics, today's reservations list, and revenue per period analytics, and verify admin views load properly.
- [ ] 4.2 Run end-to-end frontend tests and verify all UI components and API integrations function correctly without hitting Xano rate limits.
