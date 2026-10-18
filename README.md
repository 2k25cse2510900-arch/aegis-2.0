# Aegis 2.0

Aegis is a modular starter for URL risk analysis, threat intelligence, and security monitoring. The scanner includes a preliminary URL-string heuristic baseline. It does not fetch submitted URLs and is not a trained phishing model. Authentication, provider-backed threat checks, and database persistence are not connected to the scan workflow.

## Prerequisites

- Node.js 22 or newer and npm
- Python 3.12
- PostgreSQL 16 or newer for database-backed development
- Docker Compose (optional)

## Run locally (PowerShell)

Backend, in one terminal:

```powershell
cd backend
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
uvicorn app.main:app --reload
```

The health endpoint and OpenAPI UI do not connect to PostgreSQL. The database engine is configured from `DATABASE_URL`; migrations and persistence are not yet wired into routes. To use PostgreSQL, set `DATABASE_URL` in the environment before starting the API.

Frontend, in another terminal:

```powershell
cd frontend
Copy-Item .env.example .env.local
npm install
npm run dev
```

Set `VITE_API_BASE_URL` in `frontend/.env.local` if the API is hosted elsewhere. The form submits scans to `http://localhost:8000/api/scanner/scan` by default. Never put provider secrets in Vite environment variables.

## Docker Compose

From the repository root, copy `.env.example` to `.env`, replace the local database password, then run `docker compose up --build`. PostgreSQL is only exposed on the internal Compose network. The included starter is for local development, not production deployment.

## Useful commands

- Backend tests: `cd backend; python -m pytest`
- Frontend production build: `cd frontend; npm run build`
- Compose validation: `docker compose config`

## Project layout

- `frontend/`: React and Vite single-page application, API client, and Tailwind CSS.
- `backend/`: FastAPI health and URL-string scanner routes, settings, SQLAlchemy engine, Alembic environment, and API tests.
- `ml_engine/`: URL feature starter and explicit training/evaluation/prediction placeholders.
- `threat_intelligence/`: opt-in Google Safe Browsing and VirusTotal provider adapters.
- `tests/`: space for cross-module integration tests.
- `docs/`: architecture, API, and database notes.

## Model and dataset workflow

Place reviewed, licensed, labeled datasets under `ml_engine/data/raw/` and generated datasets under `ml_engine/data/processed/`; these paths are ignored by Git. Document dataset provenance and labels, construct leakage-safe train/validation/test splits, then implement `training/train_model.py` and `evaluation/evaluate_model.py`. Save the resulting artifact under `ml_engine/models/` (also ignored). `predict.py` raises `ModelUnavailableError` if no artifact exists. Feature extraction alone does not indicate whether a URL is malicious.

## Configuration and safety

Copy `.env.example` for local configuration. Never commit actual credentials. Scanner CORS defaults to `http://localhost:5173`. Provider API keys are read from environment variables, provider calls use bounded timeouts, and rate limits are surfaced; providers are not part of the scanner route and are not called during startup. Replace development database credentials before sharing or deployment.
