# Tasks

## 1. Xano Database & Admin Endpoints Setup

- [x] 1.1 Configure database tables in Xano for Locations, Slots, and Rates, and verify table schema relations.
- [x] 1.2 Implement Xano admin endpoints for creating, listing, and deleting locations with dependency guards, verifying that non-admin clients receive HTTP 403 and locations with linked slots/rates/reservations cannot be deleted.
- [x] 1.3 Implement Xano admin endpoints for managing slots per location (CRUD) with vehicle type classification (carro, moto, pcd, eletrico) and status, verifying admin authorization.
- [x] 1.4 Implement Xano admin endpoints for defining hourly rates per location and vehicle type, verifying admin authorization and `valor_hora > 0`.

## 2. Streamlit Administration Frontend

- [x] 2.1 Enable or implement Streamlit administrative views for managing locations and slots ("Locais & Vagas") with `@st.dialog` edit forms, ensuring visibility is restricted strictly to administrators.
- [x] 2.2 Implement Streamlit administrative views for managing hourly rates ("Tarifas") with `@st.dialog` edit forms, ensuring visibility is restricted strictly to administrators.

## 3. Verification & Testing

- [x] 3.1 Perform manual test verifying that authenticated clients attempting to access admin/write endpoints receive HTTP 403 Forbidden (403 de cliente em todas as escritas).
- [x] 3.2 Perform manual test verifying that client signup does not assign admin role by default (signup sem role).
- [x] 3.3 Perform manual test verifying duplicate rate prevention (duplicata de tarifa).
- [x] 3.4 Perform manual test verifying hourly rate validation (`valor_hora > 0`).
- [x] 3.5 Perform manual test verifying location deletion guard / dependency lock (trava de exclusão).
- [x] 3.6 Perform manual test verifying full CRUD operations (criar, editar, apagar) for local, vaga, and tarifa.
