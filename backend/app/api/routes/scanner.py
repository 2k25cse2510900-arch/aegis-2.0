"""URL-string-only scan baseline. This module never makes requests to submitted URLs."""
import ipaddress
import re
from urllib.parse import urlsplit

from fastapi import APIRouter
from pydantic import BaseModel, Field, field_validator

router = APIRouter(prefix="/scanner", tags=["scanner"])
MAX_URL_LENGTH = 2048
_HOST_LABEL = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$", re.IGNORECASE)


class ScanRequest(BaseModel):
    url: str = Field(min_length=1, max_length=MAX_URL_LENGTH)

    @field_validator("url")
    @classmethod
    def validate_http_url(cls, value: str) -> str:
        if any(char.isspace() or ord(char) < 32 or ord(char) == 127 for char in value):
            raise ValueError("URL must not contain whitespace or control characters; encode spaces as %20")
        try:
            parsed = urlsplit(value)
            if parsed.scheme.lower() not in {"http", "https"}:
                raise ValueError("Only HTTP and HTTPS URLs are supported")
            if not parsed.netloc or not parsed.hostname:
                raise ValueError("URL must include a valid hostname")
            if parsed.netloc.rsplit("@", 1)[-1].endswith(":"):
                raise ValueError("URL port is malformed")
            # Accessing .port also checks malformed and out-of-range port values.
            port = parsed.port
            if port is not None and not 1 <= port <= 65535:
                raise ValueError("URL port must be between 1 and 65535")
            host = parsed.hostname
            try:
                ipaddress.ip_address(host)
            except ValueError:
                ascii_host = host.encode("idna").decode("ascii")
                normalized_host = ascii_host[:-1] if ascii_host.endswith(".") else ascii_host
                labels = normalized_host.split(".")
                if not labels or any(not label or len(label) > 63 or not _HOST_LABEL.fullmatch(label) for label in labels):
                    raise ValueError("URL must include a valid hostname")
        except (UnicodeError, ValueError) as exc:
            if isinstance(exc, ValueError) and str(exc).startswith("Only HTTP"):
                raise
            if isinstance(exc, ValueError) and str(exc).startswith("URL"):
                raise
            raise ValueError("URL is malformed") from exc
        return value


class Finding(BaseModel):
    code: str
    severity: str
    description: str


class ScanResponse(BaseModel):
    submitted_url: str
    verdict: str
    risk_score: int
    risk_score_type: str
    findings: list[Finding]
    analysis_method: str
    model_status: str
    disclaimer: str


def analyze_url_string(url: str) -> ScanResponse:
    """Apply explainable indicators to text only; do not resolve or fetch the host."""
    parsed = urlsplit(url)
    host = parsed.hostname or ""
    findings: list[Finding] = []

    def add(code: str, severity: str, description: str) -> None:
        findings.append(Finding(code=code, severity=severity, description=description))

    if parsed.username is not None or parsed.password is not None:
        add("embedded_credentials", "high", "The URL contains user information before the hostname.")
    try:
        ipaddress.ip_address(host)
    except ValueError:
        pass
    else:
        add("ip_literal_host", "medium", "The hostname is an IP address literal rather than a domain name.")
    if "xn--" in host.lower():
        add("punycode_hostname", "medium", "The hostname contains an IDN punycode label.")
    labels = host.rstrip(".").split(".")
    if len(labels) >= 6:
        add("many_subdomains", "low", "The hostname has four or more subdomain labels.")
    try:
        port = parsed.port
    except ValueError:
        port = None  # Invalid ports are rejected by request validation.
    if port is not None and port not in ({80} if parsed.scheme == "http" else {443}):
        add("nonstandard_port", "low", "The URL uses a non-default HTTP or HTTPS port.")

    weights = {"high": 40, "medium": 20, "low": 10}
    score = min(100, sum(weights[finding.severity] for finding in findings))
    return ScanResponse(
        submitted_url=url,
        verdict="suspicious" if findings else "no_obvious_indicators",
        risk_score=score,
        risk_score_type="heuristic_indicator_points_not_probability",
        findings=findings,
        analysis_method="deterministic_url_string_heuristics",
        model_status="not_configured",
        disclaimer="Preliminary heuristic analysis only. No obvious indicators does not establish that a URL is safe.",
    )


@router.post("/scan", response_model=ScanResponse)
def scan_url(request: ScanRequest) -> ScanResponse:
    return analyze_url_string(request.url)
