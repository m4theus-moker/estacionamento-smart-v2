# Design

## Context

See proposal.md - Why. The Streamlit frontend (`app.py`, `ui/theme.py`) provides the user interface for clients and administrators.

## Goals / Non-Goals

**Goals:**
- Provide polished UI components, consistent spacing, and refined styling.
- Ensure cross-screen responsiveness and robust visual hierarchy.

**Non-Goals:**
- Changing backend Xano APIs or database tables.

## Decisions

- **CSS Overrides via `ui/theme.py`**: Continue using Python-injected CSS through `st.markdown` with scoped selectors for Streamlit elements (containers, buttons, metrics, expanders) to maintain a cohesive dark SaaS theme.
- **Component Refinement**: Standardize padding, border colors, hover transitions, and badge styling across views.

## Risks / Trade-offs

- [Streamlit DOM structure changes across versions] → Mitigation: Use robust selectors (`[data-testid="..."]`) and test layout behavior.
