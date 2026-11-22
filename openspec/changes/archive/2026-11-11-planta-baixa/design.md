# Design

## Context

See proposal.md - Why. The app uses Streamlit (`app.py`) communicating with Xano APIs (`/vaga`, `/reservation/availability`, `/reservation`).

## Goals / Non-Goals

**Goals:**
- Group parking slots by sectors or zones ("Planta Baixa") within `page_consult_reservations`.
- Provide sector-based navigation/tabs or expandable sections using native Streamlit components (`st.tabs` or `st.expander`).
- Preserve 3-state inventory display (Livre, Indisponível, Sua reserva), filtering, rate-limit caching, and session state persistence.

**Non-Goals:**
- Modifying backend APIs or database schema.
- Complex 2D canvas drawing libraries (keeping strictly to native Streamlit layout containers and metrics).

## Decisions

### Decision: Sector Grouping via Slot Metadata
- **Choice**: Group slots by `setor` / `zona` property (falling back to "Geral" or location name if sector field is absent in slot data).
- **Rationale**: Reuses existing slot data structures without backend changes.

### Decision: Navigation via Native Tabs (`st.tabs`)
- **Choice**: Use `st.tabs` for sectors/zones when multiple sectors exist, or clean section headers.
- **Rationale**: Clean, intuitive user experience native to Streamlit without custom HTML.

## Risks / Trade-offs

- [Slots without sector metadata] → Mitigated by grouping unassigned slots under a default "Principal / Geral" sector.
