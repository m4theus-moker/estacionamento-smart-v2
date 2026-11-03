# Design

## Context

See proposal.md - Why. The project uses Streamlit for the frontend UI and Xano for the complete backend and database, replacing local SQLite standalone prototypes and aligning with the architecture specified in `AGENTS.md`.

## Goals / Non-Goals

**Goals:**
- Implement Streamlit UI handling login, client vehicle management, reservation flows, and administrative views via REST API calls.
- Implement robust data models and REST endpoints in Xano using XanoScript.
- Enforce business logic in Xano (availability check, conflict prevention returning HTTP 409, hourly rate calculation rounding up).
- Maintain strict authorization rules between Client and Admin roles.

**Non-Goals:**
- Local SQLite database persistence in production (the existing `core/` and tests serve as reference and testing models only).
- Business logic residing inside the Streamlit frontend.

## Decisions

- **Streamlit + Xano Stack**: Streamlit exclusively for presentation and user sessions; Xano as the single source of truth for database, authentication, and business logic.
- **Conflict Handling**: Overlapping reservation checks performed in Xano query filters returning HTTP status 409 upon conflict.
- **Admin Bootstrap**: First administrator credentials provisioned via Xano environment variables / secrets.

## Risks / Trade-offs

- [Xano Rate Limits / Concurrency] → Mitigated by efficient query structuring in Xano and mitigation strategies for race conditions in table updates.
- [Streamlit Session Persistence] → Session login state managed within Streamlit browser session scope.

