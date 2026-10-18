from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import alerts, auth, dashboard, history, scanner, threats
from app.core.config import get_settings

settings = get_settings()
app = FastAPI(title=settings.app_name, version="2.0.0", description="Aegis security intelligence API starter.")
app.add_middleware(CORSMiddleware, allow_origins=settings.allowed_origins, allow_credentials=False,
                   allow_methods=["GET", "POST", "OPTIONS"], allow_headers=["Accept", "Content-Type"])

for route_module in (auth, scanner, dashboard, history, threats, alerts):
    app.include_router(route_module.router, prefix=settings.api_prefix)


@app.get("/api/health", tags=["health"])
def health():
    return {"status": "ok", "service": "aegis-api", "version": "2.0.0"}
