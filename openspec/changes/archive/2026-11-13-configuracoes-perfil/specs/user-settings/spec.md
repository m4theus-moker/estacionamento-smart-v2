# Specification: User Settings and Profile (`user-settings`)

## ADDED Requirements

### Requirement: Dedicated Settings Page
The application SHALL provide a "Configurações" page in the navigation menu for authenticated users and administrators.

#### Scenario: User accesses settings page
- **WHEN** an authenticated user selects "Configurações" from the sidebar
- **THEN** the profile management form, avatar upload, and security settings are displayed.

### Requirement: Profile and Avatar Update
Users SHALL be able to update their personal information (name, phone, CPF) and upload a profile picture/avatar.

#### Scenario: User updates profile details and avatar
- **WHEN** a user modifies their profile data or uploads an image and clicks save
- **THEN** the updated profile information is saved in session state/API and a success toast is shown.
