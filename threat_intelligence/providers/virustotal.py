"""VirusTotal adapter. Calls are explicit; startup never contacts providers."""
import httpx

ENDPOINT = "https://www.virustotal.com/api/v3/urls"


async def check_url(url: str, api_key: str) -> dict:
    if not api_key:
        return {"provider": "virustotal", "status": "unconfigured"}
    try:
        async with httpx.AsyncClient(timeout=8.0) as client:
            response = await client.post(ENDPOINT, headers={"x-apikey": api_key}, data={"url": url})
            if response.status_code == 429:
                return {"provider": "virustotal", "status": "rate_limited"}
            response.raise_for_status()
            return {"provider": "virustotal", "status": "submitted", "data": response.json().get("data", {})}
    except httpx.HTTPError:
        return {"provider": "virustotal", "status": "unavailable"}
