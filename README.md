O que o sistema faz

Cliente

Cadastra e edita seus veículos (carro, moto ou PCD).
Consulta as vagas disponíveis em um local, para um período e um veículo. O sistema mostra só as vagas compatíveis com o tipo do veículo e esconde as que já têm reserva no horário.
Reserva uma vaga. O preço é calculado no servidor: horas × valor da tarifa, com mínimo de 1 hora e arredondamento para cima.
Consulta e cancela suas reservas.

Administrador

Gerencia locais, vagas e tarifas.
Consulta e controla todas as reservas.
Arquitetura
Camada	Tecnologia
Frontend	Streamlit (Python), arquivo app.py
Backend e banco	Xano, com XanoScript (grupos de API: Authentication, Parking Management, Vehicle Management, Event Logs)
Fluxo de trabalho	OpenSpec (spec-driven), com Gemini CLI e Xano CLI
Repositório	github.com/m4theus-moker/estacionamento-smart
Decisões de projeto
Regras de negócio no servidor. Validação de posse do veículo, compatibilidade entre tipo de veículo e de vaga, conflito de horário e cálculo de preço ficam no Xano, nunca no app.
Erros reais na tela. Os erros da API aparecem como erro, e não escondidos atrás de mensagens genéricas.
Desenvolvimento assistido por agente, com controle. Toda alteração passa por diff real e dry-run antes do push, e nada vai ao servidor sem autorização.
Modelo de dados

user, vehicle (com tipo), location, vaga (com tipo), tarifa (por local e tipo de vaga), reservation (com status e preço) e event_log.
