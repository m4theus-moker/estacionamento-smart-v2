# Authentication

## Purpose

Gerencia autenticação segura, registro público criando clientes e inicialização do primeiro administrador via variáveis de ambiente/secrets no Xano.

## Requirements

### Requirement: Role-based authentication and initialization
The Xano backend SHALL authenticate users securely, ensuring public registration always creates a client, and the first administrator is initialized exclusively via environment variables or secrets. The Streamlit frontend SHALL provide password recovery ("Esqueci minha senha"), clear error messages, loading spinners, and personalized user greetings (first name or email prefix).

#### Scenario: Public registration creates client role
- **WHEN** a new user registers through the public endpoint
- **THEN** the system assigns the client role

#### Scenario: First administrator from environment variables
- **WHEN** the system initializes or authenticate the admin bootstrap credentials
- **THEN** it authenticates using email and password loaded from environment/secret variables without hardcoded credentials

#### Scenario: Frontend login feedback and greeting
- **WHEN** a user logs into Streamlit with valid credentials
- **THEN** a loading spinner is displayed during authentication, errors are clearly reported, and the sidebar greets the user using their first name or email prefix.
