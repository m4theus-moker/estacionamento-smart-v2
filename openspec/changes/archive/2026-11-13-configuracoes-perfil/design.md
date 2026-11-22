# Design

## Context
Adding user settings and profile management page (`page_user_settings`) to Estacionamento Smart.

## Architecture & Approach
- **Page Function**: `page_user_settings()` rendered when "Configurações" is selected in sidebar for both clients and admins.
- **Form Fields**: Name, email, phone, CPF, and password change fields.
- **Avatar Upload**: `st.file_uploader("Foto de Perfil", type=["png", "jpg", "jpeg"])` storing base64 or bytes in `st.session_state.user_avatar`.
- **Sidebar Avatar**: Render user avatar image in sidebar if available, falling back to initial letter circle.
- **Feedback**: `st.toast` on successful save.
