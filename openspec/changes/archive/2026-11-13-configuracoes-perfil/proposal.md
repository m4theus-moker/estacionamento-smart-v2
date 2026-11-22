# Proposal: Aba de Configurações de Perfil e Conta

## Why

Users and administrators need a dedicated settings page (`⚙️ Configurações`) to manage their personal profile details (name, phone, CPF, email), update passwords, upload profile avatars/photos, and customize account preferences.

## What Changes

- Add a new navigation option **"Configurações"** in the sidebar for both clients and administrators.
- Implement profile editing form (Name, Phone, CPF, Email).
- Implement avatar/photo upload capability (`st.file_uploader`) to display personalized user profile pictures in the sidebar.
- Implement password update security form.

## Capabilities

### New Capabilities
- `user-settings`: User profile management, avatar upload, and personal settings.

### Modified Capabilities
- `authentication`: Extended with user profile update and settings support.

## Impact
- Frontend updates (`app.py`, `ui/theme.py`) and backend API integration or session state persistence for user profile details.
