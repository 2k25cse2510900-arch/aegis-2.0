"""Deterministic URL feature extraction starter (not a phishing classifier)."""
from urllib.parse import urlparse


def extract_url_features(url: str) -> dict[str, float]:
    parsed = urlparse(url if "://" in url else f"http://{url}")
    host = parsed.hostname or ""
    return {
        "url_length": float(len(url)),
        "host_length": float(len(host)),
        "dot_count": float(url.count(".")),
        "hyphen_count": float(url.count("-")),
        "uses_https": float(parsed.scheme == "https"),
        "has_ip_host": float(bool(host) and all(part.isdigit() for part in host.split("."))),
    }
