# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**DIY Dictionary** is an LLM-powered English learning tool that helps users understand sentences and learn English through semantic, lexical, and grammatical explanations. The project is in early planning stages.

### Core Features
- **Sentence Understanding**: Semantic and grammatical analysis of sentences/sentence groups
- **Grammar Explanation**: Support for selecting text to get detailed grammatical explanations
- **Vocabulary Learning**: Multiple modes including:
  - 词义 (Known words used in unfamiliar contexts)
  - 生词 (Unknown words with common and contextual meanings)
- **Translation**: Sentence-level translation

## Technology Stack

- **Backend**: Python + FastAPI + SQLAlchemy ORM
- **Frontend**: Vue 3 + TypeScript + Vite
- **Database**: SQLite (development) / PostgreSQL (production)
- **LLM**: Claude, OpenAI, or Google Gemini (configurable)

## Architecture Notes

### Backend Structure
- **Services Layer** (`app/services/`): Business logic and external API integration
  - `llm_service.py`: Unified LLM API wrapper supporting multiple providers
  - `translation_service.py`, `grammar_service.py`, `vocabulary_service.py`: Feature-specific services
- **API Layer** (`app/api/v1/endpoints/`): RESTful endpoints
- **Database Layer** (`app/db/`): SQLAlchemy models and migrations
- **Config Layer** (`app/config.py`): Environment-aware configuration (dev vs. prod)

### Key Design Patterns
1. **Abstraction**: LLM service abstracts provider details - easy to switch providers
2. **Environment Agnostic**: SQLite for local dev, PostgreSQL for production (via `config.py`)
3. **Async Ready**: FastAPI with async/await support for scalability
4. **Migration Support**: Alembic for database schema management (future-proof)

### Frontend Structure
- **Single Page Application (SPA)** with client-side routing
- **Pinia** for state management
- **TypeScript** for type safety
- **Component-based** architecture for reusability

### Input Scope
The tool processes sentences or sentence groups, not full passages. Each request includes:
- Raw text input
- Optional selected portion for granular explanation
- Explanation type parameter

## Development Setup

### Quick Start
See `SETUP.md` for detailed instructions.

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt -r requirements-dev.txt
cp .env.example .env  # Configure LLM provider
uvicorn app.main:app --reload
```

### Frontend
```bash
bash init-frontend.sh
cd frontend
npm install
npm run dev
```

## Common Development Tasks

### Backend Commands
- **Run dev server**: `python -m app.main` (from `backend/` dir)
- **Run tests**: `pytest` (or `pytest tests/test_translation.py` for single file)
- **Format code**: `black app/`
- **Lint**: `flake8 app/`
- **Type check**: `mypy app/`

### Frontend Commands
- **Dev server**: `npm run dev` (from `frontend/` dir)
- **Build**: `npm run build`
- **Lint/Format**: `npm run lint`



## Important Notes for Development

1. **LLM Provider Configuration**: Check `.env` file - all three providers (Claude, OpenAI, Gemini) are supported via `llm_service.py`
2. **Local Development**: Backend runs on `:8000`, frontend on `:3000`. Vite proxy automatically forwards `/api/*` requests to backend
3. **Database**: Automatically uses SQLite in dev mode; no setup needed for local testing
4. **Async Operations**: LLM calls use async/await - keep this pattern when adding new features
5. **Testing**: Use pytest fixtures in `tests/conftest.py` for test database setup

绘图使用svg
永远不要使用✅之类的图标，项目进度类文件不要随便自己写，要和开发者确认
