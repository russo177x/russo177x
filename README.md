## Instagram Carousel Studio (MVP)

Implementação inicial do projeto **Instagram Carousel Studio** com backend FastAPI, frontend React/Fabric.js e export ZIP com PNG/MP4, com quantidade dinâmica de slides.

## Scripts prontos (recomendado)

Você pode usar os dois scripts na pasta `scripts/`:

```bash
# Com Docker (sobe tudo em background)
./scripts/run_with_docker.sh

# Sem Docker (cria venv isolado e sobe backend+frontend)
./scripts/run_without_docker.sh
```

> O script sem Docker cria um ambiente virtual separado em `.venv-carousel-studio` para não misturar bibliotecas com o sistema global.

---

## 1) O que você precisa ter no PC

### Obrigatório
- **Docker Desktop** (Windows/Mac) ou Docker Engine + Compose Plugin (Linux).
- **Git**.

### Opcional (modo sem Docker)
- **Python 3.11+**.
- **Node.js 20+** e npm.
- **FFmpeg** instalado no sistema.

---

## 2) Clonar e entrar na pasta

```bash
git clone <url-do-repo>
cd russo177x
```

---

## 3) Configuração manual que falta (recomendada)

Se quiser usar Groq no backend, configure a variável:

```bash
# Linux / macOS
export GROQ_API_KEY="sua-chave"

# Windows PowerShell
$env:GROQ_API_KEY="sua-chave"
```

> Sem `GROQ_API_KEY`, o backend responde como provider `ollama` por fallback lógico da aplicação.

---

## 4) Rodar com Docker (recomendado)

```bash
cd carousel-studio
docker compose up --build
```

Acessos:
- Frontend: `http://localhost:5173`
- Backend: `http://localhost:8000`
- Healthcheck: `http://localhost:8000/health`

Para parar:

```bash
docker compose down
```

---

## 5) Rodar sem Docker (opcional)

### Backend
```bash
cd carousel-studio/backend
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Frontend (outro terminal)
```bash
cd carousel-studio/frontend
npm install
npm run dev -- --host 0.0.0.0 --port 5173
```

---

## 6) Testar funcionalidades básicas no seu PC

### Testes automatizados backend
```bash
python -m unittest discover -s carousel-studio/backend/tests -v
```

### Sanidade de compilação Python
```bash
python -m compileall carousel-studio/backend
```

### Formatação (Python)
```bash
python -m black --check carousel-studio/backend
```

---

## 7) Fluxo funcional esperado (checklist rápido)

1. Abrir frontend em `http://localhost:5173`.
2. Selecionar nicho/layout/template.
3. Definir quantidade de slides (5–15).
4. Inserir texto bruto e clicar em **GERAR**.
5. Confirmar retorno de `provider` e `modo mídia`.
6. Testar exportação em `POST /api/export`.
7. Verificar ZIP com `png/` e, quando FFmpeg estiver disponível, `mp4/carousel.mp4`.

---

## Endpoints principais

- `GET /health`
- `GET /api/themes`
- `GET /api/templates`
- `GET /api/layouts`
- `GET /api/capability`
- `GET /api/examples/games-news`
- `POST /api/generate` (com `slide_count` dinâmico de 5 a 15)
- `POST /api/export` (com `slide_count` dinâmico de 5 a 15)

---

## Regras de quantidade

- Carrosséis aceitam de **5 a 15 slides** (imagens, vídeos ou misto).
- Templates e preview se adaptam ao `slide_count` enviado.
