# Spec Delta

## Purpose

Gerencia autenticação segura, registro público criando clientes e inicialização do primeiro administrador via variáveis de ambiente/secrets no Xano.

## ADDED Requirements

### Requirement: Role-based authentication and initialization
The Xano backend SHALL authenticate users securely, ensuring public registration always creates a client, and the first administrator is initialized exclusively via environment variables or secrets.

#### Scenario: Public registration creates client role
- **WHEN** a new user registers through the public endpoint
- **THEN** the system assigns the client role

#### Scenario: First administrator from environment variables
- **WHEN** the system initializes or authenticates the admin bootstrap credentials
- **THEN** it authenticates using email and password loaded from environment/secret variables without hardcoded credentials
