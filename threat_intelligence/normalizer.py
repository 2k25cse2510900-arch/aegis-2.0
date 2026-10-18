"""Normalize provider responses without asserting a verdict from missing data."""

def normalize(provider_result: dict) -> dict:
    return {"provider": provider_result.get("provider", "unknown"),
            "status": provider_result.get("status", "unavailable"),
            "result": provider_result.get("matches", provider_result.get("data"))}
