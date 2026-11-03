# AGENTS.md — Estacionamento Smart

Este arquivo contém as regras de como o agente de IA deve trabalhar neste projeto.

## Documentação

Antes de propor ou implementar qualquer mudança significativa, consultar a documentação do projeto e as specs do OpenSpec. Não presumir funcionalidades ou regras não documentadas.

## Frontend

O frontend do projeto deve ser implementado exclusivamente com **Streamlit (Python)**. Utilize os componentes do Streamlit para interface (login, veículos, reservas, administração). A interface consome exclusivamente a API REST do Xano e não contém regras de negócio.

## Backend & Banco de Dados

O backend e o banco de dados do projeto devem ser implementados exclusivamente no **Xano**, usando endpoints REST e XanoScript. O código SQLite anterior (`core/` e testes) serve apenas como referência de regras e cenários de teste, não sendo utilizado em produção.

## Segurança e Autenticação

Toda regra de autorização e validação deve ser aplicada no Xano. O valor cobrado nas reservas deve sempre ser recalculado no backend. O primeiro administrador nasce de variáveis de ambiente/secrets do Xano. Nunca coloque tokens ou credenciais do Xano em arquivos versionados (utilize `.env` ignorado pelo `.gitignore`).

## Desenvolvimento e OpenSpec

Mudanças devem seguir o fluxo OpenSpec: explore → propose → review → apply → archive.
