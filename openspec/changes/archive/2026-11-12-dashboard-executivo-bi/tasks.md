# Tasks

## 1. BI Data Aggregation & Utility Functions

- [x] 1.1 Implement pure functions in `bi_metrics.py` to process reservations, slots, and tariff data into Pandas DataFrames for revenue, occupancy, average ticket, duration, and turnover metrics.
  - *Como testar*: Executar testes unitários com pytest cobrindo todas as métricas em `tests/test_bi_metrics.py`.

## 2. Executive Dashboard UI & Access Control

- [x] 2.1 Enforce strict admin access control on the Executive Dashboard view, displaying an access denied warning for regular client users.
  - *Como testar no app*: Fazer login com conta de cliente comum e verificar que o acesso ao Dashboard Executivo é negado.
- [x] 2.2 Add location selector dropdown in the Executive Dashboard administrative view to filter all BI metrics and reports by specific parking location (unidade).
  - *Como testar no app*: Selecionar diferentes locais no seletor e verificar que os dados do dashboard são filtrados corretamente.
- [x] 2.3 Implement session state caching (60s TTL, timestamp, and manual "Atualizar" button) with cache key including location_id and period.
  - *Como testar no app*: Clicar no botão de atualizar e verificar que os dados são recarregados respeitando o TTL.

## 3. Financial KPIs & Occupancy Analytics (Priority 1)

- [x] 3.1 Render financial summary KPI cards for daily, weekly, monthly revenue and revenue projections per location.
  - *Como testar no app*: Acessar o Dashboard Executivo como admin e verificar os cartões de faturamento e projeção.
- [x] 3.2 Render occupancy rate analytics chart showing current active reservations vs total location slots.
  - *Como testar no app*: Visualizar o gráfico de taxa de ocupação atual no painel.

## 4. Edge Cases & Data Robustness

- [x] 4.1 Handle locations with zero reservations without crashing or displaying errors (empty state).
  - *Como testar no app*: Selecionar um local sem reservas e verificar a mensagem de estado vazio.
- [x] 4.2 Handle empty date periods gracefully with clear feedback.
  - *Como testar no app*: Selecionar um filtro de período sem reservas e verificar a exibição correta de 0 ou avisos.
- [x] 4.3 Handle reservations with incomplete or missing timestamps/prices robustly.
  - *Como testar no app*: Inserir reservas com dados parciais e verificar que o cálculo não quebra a aplicação.

## 5. Peak Hours Heatmap & Turnover Indicators (Priority 2)

- [x] 5.1 Implement peak hours movement heatmap chart using Streamlit native components or Altair.
  - *Como testar no app*: Visualizar o gráfico de distribuição de horários de pico na interface.
- [x] 5.2 Implement vehicle turnover indicators chart/table showing reservations per slot per day.
  - *Como testar no app*: Visualizar a rotatividade de vagas no relatório do dashboard.

## 6. Testing & Verification

- [x] 6.1 Create unit tests for BI metrics calculation in `tests/test_bi_metrics.py` and verify test suite passes successfully.
  - *Como testar*: Executar `python -m pytest` e confirmar que todos os testes passam sem erros.
