# Tasks

## 1. Xano Database Schema & Tables Setup

- [ ] 1.1 Configure database tables in Xano for Users, Vehicles, Locations, Slots, Rates, and Reservations, and verify table relations via Xano database inspector.
- [ ] 1.2 Configure admin bootstrap authentication using Xano environment variables / secrets and verify admin login succeeds.

## 2. Parking Management & Vehicle Endpoints

- [ ] 2.1 Implement Xano endpoints for creating and listing parking locations, slots, and rates, verifying that locations with dependencies cannot be deleted.
- [x] 2.2 Implement Xano endpoints for client vehicle registration and listing, ensuring vehicles belong solely to the authenticated client.

## 3. Reservation & Availability Logic

- [ ] 3.1 Implement Xano availability check and reservation creation endpoints with pricing calculation (rounding up hours) and conflict detection returning HTTP 409, verifying via API tests.
- [ ] 3.2 Implement reservation cancellation endpoints for clients and administrators, verifying status updates correctly.

## 4. Streamlit Frontend Implementation

- [x] 4.1 Implement Streamlit main entry point and authentication view (login / registration) connecting to Xano auth API.
- [ ] 4.2 Implement Streamlit client views for vehicle management and parking reservation / availability consultation.
- [ ] 4.3 Implement Streamlit administrative views for managing locations, slots, rates, and viewing/canceling reservations.
