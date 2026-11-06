# Design

## Context

See proposal.md - Why. The application is a Streamlit multi-page/tab frontend (`app.py`) communicating with Xano REST APIs. All enhancements are implemented within `app.py` utilizing Streamlit components (`st.dialog`, `st.expander`, `st.tabs`, custom CSS, etc.).

## Goals / Non-Goals

**Goals:**
- Deliver a polished, responsive, and intuitive UX across all 4 screens in `app.py`.
- Ensure robust frontend validation for vehicle plates and reservation timestamps.
- Format timestamps correctly in `America/Sao_Paulo` timezone.
- Maintain consistency with the dark green theme (`#22c55e`).
- Structure implementation into independent phases (Phase 1: Bugs & Data, Phase 2: Usability, Phase 3: Visual & Polish) as requested.

**Non-Goals:**
- Altering the Xano backend database schema or REST endpoints.
- Introducing new external Python libraries beyond standard library and Streamlit/Requests.

## Decisions

- **Client-Side Validation & Formatting**: Python's `re` module for license plate regex matching (`^[A-Z]{3}[0-9][A-Z0-9][0-9]{2}$` or old `^[A-Z]{3}[0-9]{4}$`), and `datetime` with `zoneinfo` (`America/Sao_Paulo`) for timezone-aware formatting.
- **State Management & UI Control**: Use Streamlit session state (`st.session_state`) for form clearing flags, expander states, and confirmation dialogs (`st.dialog`).
- **Visual Parking Grid**: Render slot availability grid using columns or containers with CSS styling mirroring the login parking aesthetics (`#030504` background, green borders/accents).

## Risks / Trade-offs

- [Timezone conversion discrepancies across platforms] → Mitigation: Use standard `zoneinfo` or fallback offset calculations for `America/Sao_Paulo`.
- [Expander state management in Streamlit] → Mitigation: Use session state variables to track whether vehicles exist and control `expanded=` parameter of `st.expander`.
