"""Google Safe Browsing adapter. Calls are explicit; startup never contacts providers."""
import httpx

ENDPOINT = "https://safebrowsing.googleapis.com/v4/threatMatches:find"


async def check_url(url: str, api_key: str) -> dict:
    if not api_key:
        return {"provider": "google_safe_browsing", "status": "unconfigured"}
    payload = {"client": {"clientId": "aegis", "clientVersion": "2.0.0"}, "threatInfo": {
        "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE", "POTENTIALLY_HARMFUL_APPLICATION"],
        "platformTypes": ["ANY_PLATFORM"], "threatEntryTypes": ["URL"], "threatEntries": [{"url": url}],
    }}
    try:
        async with httpx.AsyncClient(timeout=8.0) as client:
            response = await client.post(ENDPOINT, params={"key": api_key}, json=payload)
            if response.status_code == 429:
                return {"provider": "google_safe_browsing", "status": "rate_limited"}
            response.raise_for_status()
            data = response.json()
            return {"provider": "google_safe_browsing", "status": "completed", "matches": data.get("matches", [])}
    except httpx.HTTPError:
        return {"provider": "google_safe_browsing", "status": "unavailable"}
