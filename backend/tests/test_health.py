from fastapi.testclient import TestClient

from app.main import app


def test_health_endpoint():
    response = TestClient(app).get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_route_modules_import():
    from app.api.routes import alerts, auth, dashboard, history, scanner, threats

    assert all(module.router for module in (alerts, auth, dashboard, history, scanner, threats))


def test_scan_accepts_http_and_https_urls_without_fetching_them():
    client = TestClient(app)
    for url in ("http://example.com/path", "https://example.com/path"):
        response = client.post("/api/scanner/scan", json={"url": url})
        assert response.status_code == 200
        assert response.json()["submitted_url"] == url
        assert response.json()["analysis_method"] == "deterministic_url_string_heuristics"
        assert response.json()["model_status"] == "not_configured"


def test_scan_rejects_invalid_urls():
    client = TestClient(app)
    for url in ("", "   ", "ftp://example.com", "https:///missing-host", "https://bad host/path", "https://example.com:99999"):
        response = client.post("/api/scanner/scan", json={"url": url})
        assert response.status_code == 422


def test_scan_rejects_urls_longer_than_limit():
    response = TestClient(app).post("/api/scanner/scan", json={"url": "https://example.com/" + "a" * 2048})
    assert response.status_code == 422


def test_scan_reports_heuristic_indicators_without_claiming_model_prediction():
    response = TestClient(app).post("/api/scanner/scan", json={"url": "http://192.0.2.10/login"})
    assert response.status_code == 200
    result = response.json()
    assert result["verdict"] == "suspicious"
    assert "ip_literal_host" in [finding["code"] for finding in result["findings"]]
    assert result["risk_score_type"] == "heuristic_indicator_points_not_probability"
    assert result["model_status"] == "not_configured"


def test_no_indicators_is_not_reported_as_safe():
    result = TestClient(app).post("/api/scanner/scan", json={"url": "https://example.com"}).json()
    assert result["verdict"] == "no_obvious_indicators"
    assert "does not establish that a URL is safe" in result["disclaimer"]
