# MS Prontuário Animal

Microsserviço responsável pelo gerenciamento de prontuários de animais em uma rede de clínicas veterinárias.

## Funcionalidades

- **Cadastro de Animais**: Cada animal possui cadastro único com dados do tutor (nome, CPF, contato).
- **Prontuário Médico**: Registro completo de consultas, diagnósticos, tratamentos, cirurgias e evolução do peso.
- **Anexos de Imagens**: Possibilidade de anexar imagens (URLs) aos registros médicos.
- **Histórico Médico**: Visualização completa do histórico de cada animal.
- **Proteção de Dados**: Animais com histórico médico não podem ser excluídos fisicamente, apenas inativados.

## Tecnologias

- **Python 3.8+**
- **Flask** - Framework web
- **SQLAlchemy** - ORM para banco de dados
- **PostgreSQL** - Banco de dados
- **Flasgger** - Documentação Swagger da API

## Instalação

1. Instalar dependências:
   ```bash
   pip install -r requirements.txt
   ```

2. Configurar banco de dados PostgreSQL:
   - Criar banco "ms_prontuario_animal"
   - Usuário: postgres
   - Senha: root

3. Executar o serviço:
   ```bash
   python run.py
   ```

## API Endpoints

### Animais

- `GET /api/v1/animais/` - Listar animais ativos (público)
- `GET /api/v1/animais/{id}` - Buscar animal por ID (autenticado)
- `POST /api/v1/animais/` - Cadastrar novo animal (autenticado)
- `PUT /api/v1/animais/{id}` - Atualizar animal (autenticado)
- `DELETE /api/v1/animais/{id}` - Inativar animal (autenticado)
- `GET /api/v1/animais/{id}/historico` - Histórico médico (autenticado)

### Consultas

- `POST /api/v1/consultas/` - Registrar consulta (autenticado)
- `GET /api/v1/consultas/{id}` - Buscar consulta (autenticado)
- `GET /api/v1/consultas/recentes` - Consultas recentes (autenticado)

### Saúde

- `GET /api/v1/health` - Verificar status do serviço

## Autenticação

Todas as rotas protegidas requerem token JWT no header `Authorization: Bearer {token}`.

O token é validado com o serviço de autenticação centralizado via ngrok.

## Documentação da API

Acesse `/apidocs` para visualizar a documentação Swagger completa.

## Validação com Postman

Importe a coleção Postman e configure o token JWT para testar os endpoints.

## Regras de Negócio

- Nome do Pet do tutor deve ser único no sistema. Não permite o mesmo nome e Pet no sistema, mas pode diferenciar colocando numerações e até descrições.
- Animais com histórico médico são inativados, não excluídos.
- Consultas registram diagnósticos, tratamentos, cirurgias e peso.
- Imagens são armazenadas como URLs JSON.
