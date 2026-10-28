# Proposal

## Why

Com a autenticação e o cadastro de veículos já implementados e validados na change anterior, o Estacionamento Smart precisa prover o módulo de administração para que administradores possam gerenciar os locais de estacionamento, as vagas (com seus respectivos tipos `carro`, `moto`, `pcd`, `eletrico` e status `livre`, `ocupada`, `reservada`) e as tarifas horárias (com validação `valor_hora > 0`), além de permitir a edição completa de locais, vagas e tarifas via modais (`st.dialog`), utilizando o grupo de API de gestão de vagas via `XANO_PARKING_URL`.

## What Changes

- **Gerenciamento de Locais (Parking Locations)**: Endpoints e interface para criação, listagem, edição (`PUT /location/{id}`) e exclusão de locais de estacionamento, garantindo que locais vinculados a vagas, tarifas ou reservas não possam ser apagados.
- **Gerenciamento de Vagas (Parking Slots)**: Endpoints e interface para cadastro, listagem e edição (`PUT /vaga/{id}`) de vagas por local, classificadas por tipo (`carro`, `moto`, `pcd`, `eletrico`) e status (`livre`, `ocupada`, `reservada`), enviando `location_id`.
- **Gerenciamento de Tarifas (Parking Rates)**: Endpoints e interface para definição, listagem e edição (`PUT /tarifa/{id}`) de tarifas por hora baseadas no local e no tipo de vaga, com validação `valor_hora > 0`.
- **Proteção e Autorização de Administrador**: Validação rigorosa no Xano exigindo o papel (`role = admin`) para rotas administrativas, retornando `403` para clientes comuns em todas as escritas.
- **Frontend Streamlit (Administração)**: Telas "Locais & Vagas" e "Tarifas" com formulários em modais (`st.dialog`), visíveis exclusivamente para administradores.

## Capabilities

### New Capabilities
- `parking-management`: Gerenciamento administrativo de locais, vagas por tipo/status e tarifas horárias no Xano (via `XANO_PARKING_URL`), protegido por autorização de administrador.

### Modified Capabilities
- None.

## Impact

- **Backend / Xano**: Endpoints administrativos (`GET`, `POST`, `PUT`, `DELETE`) para locais, vagas e tarifas protegidos com verificação de papel (`role = admin`).
- **Frontend Streamlit**: Adição das telas de administração de locais, vagas e tarifas com modais de edição (`st.dialog`) na navegação exclusiva do administrador.
- **Segurança**: Garantia de que rotas administrativas retornem `403` para clientes em operações de escrita/leitura restrita e que parâmetros obrigatórios como `location_id` sejam corretamente enviados.
