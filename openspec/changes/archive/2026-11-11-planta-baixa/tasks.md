# Tasks

## 1. Planta Baixa & Sector Grouping Logic

- [x] 1.1 Implement sector/zone grouping utility for parking slots in `app.py` or helper module, ensuring unassigned slots fall back to a default sector and verify grouping logic with test cases.
  - *Como testar*: Executar testes unitários e verificar que slots são agrupados corretamente por setor/zona.

- [x] 1.2 Implement sector navigation tabs (`st.tabs`) or layout sections in `page_consult_reservations` to display slots organized by floor/sector (Planta Baixa).
  - *Como testar no app*: Acessar a página de consulta, selecionar um local e verificar que as vagas aparecem divididas por abas/seções de setores.

- [x] 1.3 Preserve 3-state inventory display (Livre, Indisponível, Sua reserva), filtering, rate-limit caching, and session state persistence across sectors.
  - *Como testar no app*: Interagir com os filtros de estado e tipo dentro de cada setor e verificar que o estado e o cache são mantidos corretamente sem perder o contexto.
