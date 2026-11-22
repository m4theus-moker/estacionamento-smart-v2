# Estacionamento Smart

Sistema web de reserva de vagas de estacionamento, com perfis de **cliente** e **administrador**.

- **Vídeo de demonstração:** [PREENCHER: link do YouTube]
- **Aplicativo publicado:** [PREENCHER: link do deploy, ou apague esta linha se não houver]
- **Grupo:** [PREENCHER: nome do grupo]
- **Integrantes:** [PREENCHER: nomes completos]

## Sumário

1. [Apresentação](#1-apresentação)
2. [Acesso ao aplicativo](#2-acesso-ao-aplicativo)
3. [Perfis de usuários](#3-perfis-de-usuários)
4. [Funcionalidades](#4-funcionalidades)
5. [Manual de utilização](#5-manual-de-utilização)
6. [Exemplos de utilização](#6-exemplos-de-utilização)
7. [Limitações conhecidas](#7-limitações-conhecidas)
8. [Estrutura do repositório](#8-estrutura-do-repositório)
9. [Testes e desenvolvimento](#9-testes-e-desenvolvimento)

## 1. Apresentação

O **Estacionamento Smart** é um aplicativo web para gerenciar e reservar vagas de estacionamento.

**Problema que resolve:** o motorista não sabe se existe uma vaga livre e compatível com o seu veículo, e o gestor do estacionamento não enxerga ocupação, receita e movimento de forma organizada.

**Público-alvo:**

- motoristas que querem reservar uma vaga com antecedência;
- gestores e operadores de estacionamentos que precisam configurar vagas e tarifas e acompanhar os resultados.

**Tecnologias:**

- Front-end: Streamlit (Python 3.12)
- Back-end e banco de dados: Xano (API REST e XanoScript)
- Bibliotecas: pandas, plotly, requests, python-dotenv
- Testes: pytest
- Especificações das mudanças: OpenSpec

As regras de negócio e de segurança ficam no Xano. O front-end apenas consome a API.

## 2. Acesso ao aplicativo

**Versão publicada:** [PREENCHER: link do deploy, ou informe que o aplicativo roda localmente]

### Executar localmente

Pré-requisitos: Python 3.12 e acesso à internet (o app consome a API do Xano).

```bash
git clone [PREENCHER: URL do repositório]
cd [PREENCHER: pasta do repositório]
python -m venv .venv

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
# Linux ou macOS
source .venv/bin/activate

pip install -r requirements.txt
```

Crie o arquivo `.env` a partir do modelo `.env.example` e confira as três variáveis, que apontam para os grupos de API do Xano (autenticação, veículos e estacionamento):

```
XANO_API_URL=
XANO_VEHICLES_URL=
XANO_PARKING_URL=
```

Inicie o aplicativo e abra `http://localhost:8501` no navegador:

```bash
streamlit run app.py
```

> O arquivo `.env` não é versionado. Nunca coloque tokens ou credenciais no repositório.

### Contas de demonstração

| Perfil | E-mail | Senha |
|---|---|---|
| Cliente | [PREENCHER] | [PREENCHER] |
| Administrador | [PREENCHER] | [PREENCHER] |

Use somente contas fictícias, criadas para a demonstração.

## 3. Perfis de usuários

| Perfil | Responsabilidades e permissões |
|---|---|
| **Cliente** | Cadastra e gerencia os próprios veículos, consulta vagas, faz e cancela reservas e consulta os tickets. |
| **Administrador** | Cadastra locais, vagas e tarifas, acompanha todas as reservas, consulta o dashboard executivo e os logs de auditoria. |

- Contas criadas pela tela **Criar Conta** são de cliente.
- O primeiro administrador é definido na configuração do Xano.
- A autorização é verificada no Xano, não apenas na interface.

## 4. Funcionalidades

**Cliente**

- Cadastro, login e logout.
- **Meus Veículos:** cadastro com placa validada (formato antigo e Mercosul), edição, exclusão com confirmação, busca e contadores por tipo (carro, moto, PCD).
- **Reservar:** escolha de local, veículo e período, com preço estimado.
- **Mapa de vagas** do local, com os estados *Livre*, *Indisponível* e *Sua reserva*, ícone por tipo de vaga, filtros, legenda e resumo.
- **Minhas Reservas:** abas Ativas e Histórico, status calculado (Válido, Em andamento, Expirado, Cancelado) e cancelamento com confirmação.
- **Ticket** de reserva com código único de 8 caracteres e download em HTML imprimível.
- Solicitação de retirada do veículo. [CONFIRMAR antes de entregar]
- Configurações de perfil. [CONFIRMAR antes de entregar]

**Administrador**

- **Locais e Vagas:** cadastro, edição e exclusão de locais e vagas (carro, moto, PCD, elétrica), com geração de vagas em lote.
- **Tarifas:** valor por hora por local e tipo de vaga.
- **Todas as Reservas:** visão por unidade ou consolidada, com filtro de status, busca por ID, veículo, usuário ou ticket e exclusão de reservas.
- **Dashboard Executivo e BI:** seletor de unidade e de período, receita reservada (hoje, semana e mês), projeção mensal, taxa de ocupação, ticket médio, tempo médio de permanência, rotatividade, gráficos (tendência diária, status, categoria, dia da semana e horário de pico) e exportação em CSV.
- **Logs de Auditoria:** consulta de eventos com busca e filtro por ação.

**Regras do sistema**

- O preço da reserva é recalculado no backend.
- O sistema só oferece vagas compatíveis com o tipo do veículo e sem conflito de horário.
- Cada reserva gera um ticket com código único.
- Os horários seguem o fuso America/Sao_Paulo.
- Os dados da API ficam em cache por 60 segundos, com botão Atualizar, para respeitar o limite do plano gratuito do Xano.

## 5. Manual de utilização

Os nomes dos menus podem variar levemente. O caminho abaixo segue as jornadas principais do sistema.

### 5.1 Jornada do administrador: preparar o estacionamento

1. Entre com a conta de administrador na tela de login.

   ![Tela de login](docs/img/01-login.png)

2. Abra **Locais e Vagas**. Cadastre o local (nome, endereço e descrição) ou selecione um local existente.
3. Cadastre vagas uma a uma ou use a **geração em lote**: informe piso, fileira, tipo, quantidade e número inicial.

   ![Locais e vagas](docs/img/02-admin-locais-vagas.png)

4. Abra **Tarifas** e defina o valor por hora de cada tipo de vaga.

   ![Tarifas](docs/img/03-admin-tarifas.png)

**Resultado esperado:** as vagas aparecem na lista do local e ficam disponíveis para reserva com a tarifa definida.

### 5.2 Jornada do cliente: reservar uma vaga

1. Na tela de login, abra a aba **Criar Conta** e cadastre-se, ou entre com uma conta existente.
2. Abra **Meus Veículos** e cadastre um veículo: placa, marca, modelo, cor, ano e tipo. Uma placa fora do formato é recusada com mensagem de erro.

   ![Meus veículos](docs/img/04-cliente-veiculos.png)

3. Abra **Reservar**. Escolha o local, o veículo e as datas e horários de início e término. O **preço estimado** aparece abaixo do formulário.

   ![Formulário de reserva](docs/img/05-cliente-reservar.png)

4. Clique em **Consultar Disponibilidade**. O mapa mostra todas as vagas do local:
   - **Livre:** pode ser reservada;
   - **Indisponível:** ocupada no período ou incompatível com o tipo do veículo;
   - **Sua reserva:** vaga que você já reservou no período.

   Use os filtros por tipo e estado para localizar uma vaga.

   ![Mapa de vagas](docs/img/06-cliente-mapa.png)

5. Clique em **Reservar** em uma vaga livre.
6. Abra **Minhas Reservas** e clique em **Ver Ticket** para ver o código da reserva. Use **Baixar ticket** para salvar o ticket em HTML.

   ![Ticket de reserva](docs/img/07-cliente-ticket.png)

**Resultado esperado:** a reserva aparece na aba **Ativas** com status *Válido*, mostrando local, vaga e veículo, e o ticket tem um código único de 8 caracteres.

### 5.3 Jornada do administrador: acompanhar a operação

1. Abra **Todas as Reservas**. A reserva do cliente aparece na lista. Busque pelo código do ticket, pelo ID ou pelo veículo.

   ![Todas as reservas](docs/img/08-admin-reservas.png)

2. Abra o **Dashboard Executivo**, escolha a unidade e o período e consulte os cartões e gráficos.
3. Clique em **Atualizar** para buscar dados novos e use a exportação em CSV, se necessário.

   ![Dashboard executivo](docs/img/09-admin-dashboard.png)

**Resultado esperado:** os indicadores refletem as reservas da unidade selecionada.

### 5.4 Outras ações

- **Cancelar uma reserva:** em **Minhas Reservas**, clique em **Cancelar** e confirme. A reserva vai para o **Histórico** com status *Cancelado*.
- **Editar ou excluir um veículo:** em **Meus Veículos**, use os botões do cartão do veículo e confirme a exclusão.
- **Consultar auditoria:** em **Logs de Auditoria**, busque ou filtre por ação.
- **Sair:** use o botão **Sair** no menu lateral.

## 6. Exemplos de utilização

**Exemplo 1: reserva de um carro.** O cliente cadastra um carro com a placa `ABC1D23` e reserva uma vaga de carro no dia seguinte, por duas horas. O sistema mostra o preço estimado pela tarifa do tipo de vaga e, após a reserva, gera o ticket.

**Exemplo 2: vaga incompatível.** O cliente com um carro consulta um local que também tem vagas de moto. As vagas de moto aparecem como *Indisponível* para esse veículo.

**Exemplo 3: reserva cancelada.** O cliente cancela uma reserva futura. O status passa a *Cancelado* e a vaga volta a ficar livre no período.

**Exemplo 4: montar um estacionamento.** O administrador gera um lote de vagas (por exemplo, 8 de carro, 3 de moto, 2 PCD e 2 elétricas) e define a tarifa de cada tipo.

**Exemplo 5: leitura do dashboard.** O administrador seleciona a unidade, escolhe o período *Este mês* e compara receita reservada, ocupação e horários de pico.

**Dados de demonstração:** [PREENCHER: descreva o local, as vagas e as reservas de exemplo cadastradas para a apresentação]

## 7. Limitações conhecidas

- **Sem pagamento.** A "receita" do dashboard é receita *reservada*, não recebida.
- **Sem check-in e check-out.** Tempo de permanência e rotatividade são calculados sobre o período reservado, não sobre o uso real da vaga.
- **Limite do plano gratuito do Xano:** 10 requisições a cada 20 segundos, somando todos os usuários. Muitos acessos simultâneos ou cliques muito rápidos podem gerar erro 429. O cache de 60 segundos reduz o problema.
- **Mapa de vagas:** o estado *Indisponível* reúne vagas ocupadas e vagas incompatíveis com o veículo. O agrupamento por piso e fileira é deduzido do número da vaga.
- **Logs de Auditoria:** quando a API não retorna registros, a tela pode exibir dados de exemplo. [CONFIRMAR]
- **Recuperação de senha:** existe no backend, mas não tem tela no aplicativo.
- **Notificações por e-mail e webhook:** ainda em desenvolvimento. [CONFIRMAR]
- **Solicitação de retirada de veículo:** [CONFIRMAR: informe se os pedidos ficam salvos no Xano ou apenas em memória]
- **Deploy:** [PREENCHER: informe se o aplicativo está publicado ou se roda apenas localmente]

## 8. Estrutura do repositório

```
app.py                  Aplicativo Streamlit (telas, login, menu por perfil)
ui/theme.py             Tema visual (tema escuro com destaque verde)
slot_map.py             Classificação das vagas e agrupamento por piso e fileira
bi_metrics.py           Métricas do dashboard (funções puras)
reservation_status.py   Status calculado das reservas
tests/                  Testes automatizados (pytest)
openspec/               Especificações e histórico das mudanças
xano-pull-av/           Código do Xano (tabelas, funções e endpoints em XanoScript)
requirements.txt        Dependências Python
.env.example            Modelo das variáveis de ambiente
```

## 9. Testes e desenvolvimento

Executar os testes automatizados:

```bash
python -m pytest tests/
```

Fluxo de desenvolvimento: as mudanças são especificadas com OpenSpec (explorar, propor, revisar, aplicar e arquivar).

Código do Xano: fica em `xano-pull-av/`. Alterações são publicadas arquivo a arquivo com o Xano CLI, sempre com `--dry-run` antes:

```bash
xano workspace push -d xano-pull-av -i "<caminho do arquivo>" --dry-run
```
