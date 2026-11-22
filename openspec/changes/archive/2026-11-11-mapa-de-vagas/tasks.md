# Tasks

## 1. Slot Map Data Fetching, Caching & State Persistence

- [x] 1.1 Implement cached data retrieval helper for location slots (`GET /vaga`), availability (`GET /reservation/availability`), and user reservations (`GET /reservation`) in `st.session_state` with 60s TTL, a compound cache key including `location_id`, `vehicle_id`, `start_time`, and `end_time` (changing any parameter invalidates the cache), and a manual "Atualizar" button.
  - *Como testar no app*: Acessar a página de consulta, verificar que no máximo 3 chamadas de API são feitas, inspecionar `st.session_state` para confirmar o cache com timestamp e chave composta (`location_id`, `vehicle_id`, `start_time`, `end_time`), e clicar no botão "Atualizar" para forçar nova requisição.

- [x] 1.2 Implement persistence of consultation parameters and results in `st.session_state`, ensuring that changing filters or interacting with the screen does not cause the slot map to disappear upon reruns.
  - *Como testar no app*: Realizar uma consulta de mapa de vagas, alterar filtros de exibição ou interagir com componentes da página e verificar que o mapa permanece visível sem perder o estado.

- [x] 1.3 Implement API failure handling and error display without rendering partial maps.
  - *Como testar no app*: Simular falha em um dos endpoints e verificar que a mensagem de erro é exibida de forma clara e nenhuma grade parcial de vagas é renderizada.

## 2. Frontend State Calculation, Edge Cases & Grid Rendering

- [x] 2.1 Implement frontend state classification logic (Livre, Indisponível, Sua reserva) as a pure function based on availability and user reservations overlapping query time range (ignoring reservations with status `cancelada`), where "Indisponível" is defined as a slot that the availability endpoint did not return for the selected vehicle (ocupada por outra reserva OU incompatível com o tipo do veículo). Add automated unit tests in `tests/` (pytest) covering livre, indisponível, sua reserva, and reserva cancelada.
  - *Como testar no app/testes*: Executar `pytest tests/test_slot_classification.py` e validar via dados de teste que vagas livres, indisponíveis, da própria reserva (ativa) e reservas canceladas são classificadas corretamente.

- [x] 2.2 Implement edge case handling and validation for user without registered vehicle.
  - *Como testar no app*: Acessar a consulta de vagas com um usuário que não possui veículos cadastrados e verificar que a mensagem/alerta orienta o cadastro de veículo prévio.

- [x] 2.3 Implement edge case handling and validation for invalid period (`end <= start`).
  - *Como testar no app*: Definir data/hora de término anterior ou igual à de início e verificar que o sistema exibe erro de validação impedindo a consulta.

- [x] 2.4 Implement edge case handling and validation for location without slots (`GET /vaga` vazio).
  - *Como testar no app*: Selecionar um local que não possui vagas cadastradas (`GET /vaga` vazio) e verificar que uma mensagem informativa adequada é exibida.

- [x] 2.5 Implement responsive grid layout (4-5 columns per row) and slot cards with vehicle type icons (`:material/...:`).
  - *Como testar no app*: Visualizar o mapa de vagas na tela de consulta e verificar a disposição em grade responsiva, com número da vaga, tipo e ícone correspondente utilizando `st.container(border=True)`.

- [x] 2.6 Implement filtering controls by vehicle type and slot state (Livre, Indisponível, Sua reserva), updating the legend and filters accordingly.
  - *Como testar no app*: Selecionar filtros por tipo de veículo e estado e verificar que a grade exibe apenas as vagas correspondentes, com legenda atualizada.

- [x] 2.7 Implement summary header and state legend.
  - *Como testar no app*: Conferir o resumo estatístico no topo (ex.: "12 livres de 20") e a legenda explicativa dos estados.

- [x] 2.8 Implement selection of free slots leading to the existing reservation confirmation flow.
  - *Como testar no app*: Clicar em uma vaga livre no mapa e verificar que abre a confirmação de reserva existente.

- [x] 2.9 Implement non-clickable behavior for unavailable or user's reserved slots.
  - *Como testar no app*: Tentar interagir com uma vaga indisponível ou de sua reserva e verificar que nenhum botão de seleção/reserva aparece.
