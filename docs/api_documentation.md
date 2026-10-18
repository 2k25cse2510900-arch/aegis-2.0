# API documentation

Run `uvicorn app.main:app --reload` from `backend/`. Interactive OpenAPI documentation is available at `/docs`; the schema is at `/openapi.json`.

## Implemented

- `GET /api/health`: liveness response with service and version.
- `POST /api/scanner/scan`: validates and analyzes only the supplied URL string. It makes no request to that URL.

Request:

```json
{"url":"https://example.com/login"}
```

Example response shape (values are determined from URL text; this example is not a live domain assessment):

```json
{
  "submitted_url": "https://example.com/login",
  "verdict": "no_obvious_indicators",
  "risk_score": 0,
  "risk_score_type": "heuristic_indicator_points_not_probability",
  "findings": [],
  "analysis_method": "deterministic_url_string_heuristics",
  "model_status": "not_configured",
  "disclaimer": "Preliminary heuristic analysis only. No obvious indicators does not establish that a URL is safe."
}
```

`suspicious` means one or more listed string heuristics matched; `no_obvious_indicators` means none matched. Neither verdict is a trained-model result. Scores count heuristic indicator points and are not probabilities. Invalid, non-HTTP(S), whitespace-containing, or longer than 2,048 character URLs receive HTTP 422.

The deterministic score adds 40 points per high, 20 per medium, and 10 per low severity finding, capped at 100. It is a transparent indicator tally, not a calibrated estimate of phishing probability.

## Placeholders

- `GET /api/auth/status`: explicitly reports authentication is not configured.
- `POST /api/scan`: indicates scanning is not implemented.
- `GET /api/dashboard`, `/api/history`, `/api/threats`, `/api/alerts`: placeholder payloads only.

These endpoints do not represent real scan results, users, alerts, or threat intelligence. Authentication and request/response schemas should be specified before these routes become functional.
