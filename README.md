# FakeLetterboxd

**Disciplina:** INF1407 — Programação para Web  
**Integrantes:** Luísa Silveira, Rafael Ribeiro

---

## Escopo do projeto

O **FakeLetterboxd** é uma aplicação web inspirada no Letterboxd, voltada para o registro e compartilhamento de avaliações de filmes e séries. O site permite que usuários autenticados busquem títulos diretamente pela API do OMDB, registrem avaliações com nota e comentário, e visualizem as avaliações de toda a comunidade.

### Funcionalidades desenvolvidas

- **Portal público** — página inicial com apresentação do site e acesso ao cadastro/login.
- **Cadastro e autenticação de usuários** — registro de nova conta, login, logout e recuperação de senha por e-mail.
- **Perfil do usuário** — página com foto de perfil, bio, data de nascimento e histórico de avaliações do próprio usuário; edição dos dados do perfil.
- **Integração com a API OMDB** — busca de filmes e séries por título diretamente na API externa, com importação automática de pôster, sinopse, diretor, elenco, duração, idioma, país, classificação indicativa e número de temporadas.
- **Criação de avaliação** — busca a mídia via OMDB, seleciona o título e preenche nota (0 a 5), comentário e data em que assistiu.
- **Lista de avaliações** — exibe todas as avaliações da plataforma em cards com pôster, filtros por título, usuário, tipo de mídia (filme/série) e gênero, além de ordenação por nota.
- **Detalhe de avaliação** — página completa com todas as informações da mídia e da avaliação.
- **Edição e exclusão de avaliação** — disponíveis apenas para o autor da avaliação, tanto na lista quanto na página de detalhe (protegido também no backend com erro 403 para acesso direto via URL).
- **Perfil público de outros usuários** — visualização das avaliações de qualquer usuário da plataforma.

---

## Tecnologias utilizadas

| Tecnologia | Versão |
|---|---|
| Python | 3.x |
| Django | 6.x |
| Pillow | — |
| Requests | — |
| python-decouple | — |
| API OMDB | — |

---

## Como executar o projeto localmente

### Pré-requisitos

- Python 3.10+
- Uma chave de API gratuita do OMDB: [https://www.omdbapi.com/apikey.aspx](https://www.omdbapi.com/apikey.aspx)

### Passos

```bash
# 1. Clone o repositório
git clone <url-do-repositorio>
cd inf1407-Projeto1-FakeLetterboxd/projeto-letterboxd

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Crie o arquivo .env na raiz de NossoProjeto/ com o conteúdo:
#    OMDB_API_KEY=sua_chave_aqui

# 4. Aplique as migrações
cd NossoProjeto
python manage.py migrate

# 5. Crie um superusuário (opcional, para o painel admin)
python manage.py createsuperuser

# 6. Inicie o servidor
python manage.py runserver
```

Acesse em: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## Manual do usuário

### 1. Página inicial
Ao acessar o site, você verá a tela de boas-vindas. Se ainda não tiver conta, clique em **"Criar conta"**. Se já tiver, clique em **"Já tenho conta"**.

### 2. Cadastro
Preencha nome de usuário, e-mail e senha e clique em **"Cadastrar"**. Após o cadastro, você será redirecionado para a tela de login.

### 3. Login
Informe seu nome de usuário e senha e clique em **"Entrar"**. Caso tenha esquecido a senha, use o link **"Esqueceu a senha?"** para recebê-la por e-mail.

### 4. Lista de avaliações
Após o login, você acessa a lista geral de avaliações de todos os usuários. Use os filtros no topo para:
- Buscar por **título** da mídia ou por **nome de usuário**.
- Filtrar por **tipo** (filme ou série) e por **gênero**.
- Ordenar por **maior ou menor nota**.

Clique em qualquer card para ver os **detalhes completos** da avaliação.

### 5. Criar uma avaliação
Clique em **"Nova Avaliação"** na barra de navegação.
1. Digite o título do filme ou série no campo de busca e clique em **"Buscar"**.
2. Clique em **"Selecionar"** no resultado desejado.
3. Preencha a **nota** (de 0 a 5), a **data em que assistiu** (opcional) e o **comentário** (opcional).
4. Clique em **"Publicar Avaliação"**.

### 6. Editar ou excluir uma avaliação
Os botões **"Editar"** e **"Excluir"** aparecem apenas nas avaliações que você mesmo criou, tanto na lista quanto na página de detalhe. Apenas o autor pode realizar essas ações.

### 7. Perfil
Clique no seu nome de usuário na barra de navegação para acessar seu perfil. Lá você vê:
- Sua foto, bio e data de nascimento.
- Todas as suas avaliações com filtros.

Para editar as informações do perfil, clique em **"Editar perfil"**.

Você também pode clicar no nome de outro usuário em qualquer avaliação para ver o perfil público dele.

---

## O que funcionou

- Cadastro, login, logout e recuperação de senha por e-mail.
- Edição de perfil (foto, bio, data de nascimento).
- Busca de mídias via API OMDB com importação de todos os dados.
- Criação de avaliação com seleção de mídia da OMDB e preenchimento de nota (0 a 5), comentário e data em que assistiu.
- Listagem de avaliações com filtros por título, usuário, tipo, gênero e ordenação por nota.
- Página de detalhe da avaliação com informações completas da mídia.
- Edição e exclusão de avaliação restritas ao autor (proteção no frontend e no backend).
- Perfil público de outros usuários com suas avaliações e filtros.

