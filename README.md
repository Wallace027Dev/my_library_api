# My Library API

Uma API para controle pessoal de biblioteca, desenvolvida em Python com Flask e SQLite. O objetivo deste projeto é gerenciar o acervo pessoal de livros e uma lista de desejos (“wishlist”) de forma simples, moderna e alinhada a boas práticas de arquitetura em projetos Flask.

## Características

- **Cadastro e gerenciamento de livros**: registre título, autor, editora, categoria, quantidade de páginas e mais.
- **Controle de status de leitura**: marque livros como “falta ler”, “lendo” ou “lido” e avalie com nota de 1 a 5 ao concluir leitura.
- **Lista de desejos** (wishlist): mantenha livros desejados separados do acervo principal.
- **Filtros por categoria, status, autor, etc.**
- **Rotas RESTful** para inclusão, alteração, remoção e consulta.
- **Documentação planejada com Swagger/OpenAPI** (em breve).
- **Projeto organizado** com separação de camadas: modelos, schemas, banco, rotas e lógica de negócio.
- **Foco em uso individual/pessoal** (não há autenticação/multusuários).

## Estrutura do Projeto

```
my_library_api/
│
├── app/
│   ├── __init__.py       # Inicializa a aplicação Flask
│   ├── database.py       # Configuração e inicialização do SQLite
│   ├── models.py         # Modelos do banco de dados (ORM)
│   ├── schemas.py        # Schemas para serialização e validação
│   └── ...               # (Demais arquivos como rotas e serviços)
│
├── requirements.txt      # Dependências do projeto
├── run.py                # Inicialização da aplicação
└── README.md
```

## Como rodar o projeto localmente

1. Clone este repositório:
   ```
   git clone https://github.com/Wallace027Dev/my_library_api.git
   cd my_library_api
   ```

2. Crie e ative um ambiente virtual:
   ```
   python -m venv venv
   source venv/bin/activate    # Linux/macOS
   venv\Scripts\activate       # Windows
   ```

3. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

4. (Opcional) Crie o banco de dados pela primeira vez:
   ```python
   # No terminal interativo python
   from app import db, create_app
   app = create_app()
   app.app_context().push()
   db.create_all()
   ```

5. Execute a aplicação:
   ```
   python run.py
   ```

A API estará disponível localmente, por padrão, em `http://127.0.0.1:5000/`.

## Tecnologias e Boas Práticas

- **Python 3**
- **Flask** (framework web)
- **SQLite** (banco de dados leve)
- **Flask-SQLAlchemy** (ORM)
- **Marshmallow** (serialização e validação)
- Separação de responsabilidades (princípios SOLID)

## Rotas principais (exemplo)

- `POST   /livros`           – Cadastrar livro
- `GET    /livros`           – Listar todos/filtro de livros
- `GET    /livros/<id>`      – Obter detalhes de um livro
- `PATCH  /livros/<id>`      – Alterar status/nota
- `DELETE /livros/<id>`      – Remover livro
- `POST   /wishlist`         – Adicionar à wishlist
- `GET    /wishlist`         – Listar wishlist
- `DELETE /wishlist/<id>`    – Remover da wishlist

**Veja detalhes das rotas em breve na documentação Swagger/OpenAPI!**

## Contribuição

Pull requests são bem-vindos! Para ideias, sugestões e correções, fique à vontade para abrir uma issue ou contribuir diretamente com código.

## Licença

Este projeto está sob a licença MIT.

---

> Projeto em desenvolvimento para fins de aprendizado e demonstração acadêmica.