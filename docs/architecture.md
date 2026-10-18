# Architecture

The frontend is a React/Vite single-page application. Its API client targets the FastAPI service via `VITE_API_BASE_URL`. The backend groups HTTP route modules under `app/api/routes`, environment settings in `app/core`, persistence configuration in `app/database`, and business logic under `app/services`.

Machine learning is isolated in `ml_engine`: feature extraction is independent from model training and prediction. No model artifact ships with this starter. Threat-intelligence adapters are isolated under `threat_intelligence/providers`; calls must be explicitly invoked by future application services and never run during startup.

Compose runs frontend, API, and PostgreSQL. The database uses a persistent named volume and is not published to the host. The current API health and placeholder routes do not require a database connection.
