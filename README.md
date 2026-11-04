# Portal de Projetos — Flask

Versão Flask da API Node.js do Portal de Projetos, baseada na organização do exemplo do professor `helioesperidiao/api_flask_funcionario_cargo`.

## Como executar

1. Inicie o MySQL no XAMPP e utilize o schema `portal_de_projetos`.
2. No terminal, na raiz do repositório, execute: `python install.py`.
3. Crie um `.env` na raiz e defina `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`, `DB_PORT` e `JWT_SECRET`. A senha pode ficar vazia se seu MySQL não usar senha.
4. Execute: `python app.py`.
5. Abra `http://localhost:8000/Login.html`.

A API Flask e a API Node.js usam a **mesma porta 8000**, portanto execute apenas uma delas por vez. O frontend em `static/` foi mantido idêntico nos dois repositórios.

**Atenção:** `python install.py` instala apenas as dependências. O arquivo `docs/Banco.sql` contém `DROP SCHEMA` e apagaria os dados existentes se fosse executado manualmente; não é necessário executá-lo quando o banco já existe.

O Flask carrega o arquivo `.env` usando `python-dotenv`. Defina `JWT_SECRET` com uma chave própria (não deixe o texto de exemplo `coloque_aqui_seu_segredo_jwt`). O arquivo `.env` é ignorado pelo Git; não publique sua senha nem o segredo. Tokens de Flask e Node.js não são necessariamente intercambiáveis; faça login novamente ao trocar de API.

Exemplo de nomes das variáveis (substitua o segredo por uma chave forte e mantenha sua senha somente no `.env`):

```dotenv
DB_HOST=127.0.0.1
DB_USER=root
DB_PASSWORD=
DB_NAME=portal_de_projetos
DB_PORT=3306
JWT_SECRET=substitua_por_uma_chave_forte_e_aleatoria
```

## Organização

- `api/router/`: endpoints Flask com Blueprint e decorators de middleware
- `api/control/`: respostas HTTP e formato JSON
- `api/service/`: regras de negócio e autorização por proprietário
- `api/dao/`: SQL, transações e acesso ao MySQL
- `api/model/`: entidades de usuário, projeto e comentário
- `api/middleware/`: autenticação JWT e validação de dados
- `static/`: mesmo frontend do Node.js (incluindo upload PNG/JPG de até 2 MB)

## Endpoints compatíveis

- `/api/usuarios` — cadastro, listagem, alteração e exclusão
- `/api/usuarios/login` — login e token JWT
- `/api/usuarios/me` — perfil do usuário autenticado
- `/api/projetos` — CRUD de projetos
- `/api/projetos/imagem` — upload PNG/JPG
- `/api/comentarios` — CRUD de comentários
- `/api/comentarios/projeto/<idProjeto>` — comentários de um projeto

Criar, editar e excluir projetos/comentários exige JWT; alterar/excluir exige também a propriedade do registro. 
