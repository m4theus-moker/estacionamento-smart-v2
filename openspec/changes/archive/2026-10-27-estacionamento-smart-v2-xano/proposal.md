# Proposal

## Why

O Estacionamento Smart v2 adota oficialmente a stack **Streamlit + Xano completo**. O frontend em Streamlit cuida exclusivamente da interface de usuário (login, veículos, reservas, administração) consumindo os endpoints REST do Xano, enquanto o Xano fornece o backend, a lógica em XanoScript e o banco de dados gerenciado, garantindo persistência em nuvem, autenticação robusta e regras de negócio validadas.

## What Changes

- **Frontend em Streamlit**: Interface Python responsável por renderizar telas de login, gerenciamento de veículos, reservas e administração, comunicando-se unicamente via chamadas HTTP REST com a API do Xano (sem regras de negócio embutidas no frontend).
- **Backend & Database no Xano**: Xano como backend oficial e banco de dados gerenciado (substituindo qualquer protótipo local com SQLite standalone).
- **Regras de Negócio em XanoScript**: Implementação de entidades (Locais, Vagas por tipo, Tarifas por tipo e local, Clientes, Veículos e Reservas) diretamente no Xano.
- **Controle de Concorrência e Conflitos**: Tratamento de concorrência e sobreposição de horários no Xano, retornando código `409` em caso de conflitos.
- **Autenticação e Permissões**: Autenticação nativa do Xano onde o cadastro público cria clientes, e o primeiro administrador nasce de variáveis de ambiente/secrets do Xano.
- **Cálculo Preciso de Preços**: Cálculo no backend arredondando as horas para cima multiplicadas pela tarifa do local e tipo de vaga.

## Capabilities

### New Capabilities
- `streamlit-frontend`: Interface de usuário em Streamlit consumindo a API REST do Xano para clientes e administradores.
- `parking-management`: Gerenciamento de locais, vagas e tarifas por administradores no Xano.
- `client-vehicles`: Cadastro e gerenciamento de veículos pelos clientes via Xano.
- `reservations`: Consulta de disponibilidade, criação e cancelamento de reservas com validação de horários e conflitos (409) no Xano.
- `authentication`: Autenticação nativa e controle de acesso baseado em papéis (Cliente e Administrador) gerenciados pelo Xano.

### Modified Capabilities
- None.

## Impact

- **Frontend**: Nova aplicação Streamlit consumindo API REST.
- **Backend / Database**: Migração total para o Xano.
- **Segurança e Regras**: Lógica de autorização e cálculos centralizados estritamente no Xano.

