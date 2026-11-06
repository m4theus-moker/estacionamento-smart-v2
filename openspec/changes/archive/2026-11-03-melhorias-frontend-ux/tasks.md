# Tasks

## 1. Phase 1: Bugs and Data (Reservations & Vehicles)

- [x] 1.1 Format reservation timestamps as `dd/mm/aaaa HH:MM` in `America/Sao_Paulo` timezone and verify correct date rendering in `app.py`.
- [x] 1.2 Implement styled status badges (`ativa` = green, `cancelada` = red/gray, `concluída` = blue) with capitalized text and no monospace, and verify badge rendering.
- [x] 1.3 Display rich reservation context (location, slot, vehicle model + plate) on reservation cards and verify card details.
- [x] 1.4 Add vehicle form clearing after save and robust validation for license plates (`ABC1234` / `ABC1D23`) and year range (1980 to current year + 1), and verify validation error handling.

## 2. Phase 2: Usability (Reservations, Consult/Reserve, Vehicles, Login)

- [x] 2.1 Sort reservations newest to oldest and split into "Ativas" and "Histórico" tabs, and verify tab separation and sorting.
- [x] 2.2 Add confirmation dialog using `st.dialog` before canceling a reservation and verify cancellation workflow.
- [x] 2.3 Set default reservation end time to start + 1h, add start/end time validation (end > start, start not in past), calculate estimated price, and verify pricing/validation.
- [x] 2.4 Display parking slots in a visual grid (free/busy) with themed styling after consultation and verify grid rendering.
- [x] 2.5 Collapse "Adicionar veículo" expander by default when vehicles exist, add "Editar" button on cards and delete confirmation, and verify vehicle management UX.
- [x] 2.6 Add friendly empty states with action buttons for vehicles and reservations, and verify empty state displays.
- [x] 2.7 Add "Esqueci minha senha" placeholder, clear error handling, and loading spinner on login/registration, and verify login UX.

## 3. Phase 3: Visual Polish and Accessibility

- [x] 3.1 Update user greeting to use first name or email prefix instead of full email and verify greeting rendering.
- [x] 3.2 Make metric cards compact with icons (Total, Cars, Motorcycles, PCD) and verify metrics display.
- [x] 3.3 Style vehicle cards with monospace plate, border, and specific vehicle type icons (Car, Moto, PCD) and verify card aesthetics.
- [x] 3.4 Enhance sidebar with distinct icons, shortened "Reservar" label, and truncated username with tooltip, and verify sidebar navigation.
- [x] 3.5 Improve contrast for placeholders/small labels and standardize spacing/field heights across screens, and verify overall visual consistency.
