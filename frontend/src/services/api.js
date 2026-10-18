const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export async function scanUrl(url) {
  let response;
  try {
    response = await fetch(`${API_BASE_URL}/api/scanner/scan`, {
      method: 'POST',
      headers: { Accept: 'application/json', 'Content-Type': 'application/json' },
      body: JSON.stringify({ url }),
    });
  } catch {
    throw new Error('Could not reach the scanner API. Check that the backend is running.');
  }
  const payload = await response.json().catch(() => ({}));
  if (!response.ok) {
    const detail = payload.detail;
    const message = Array.isArray(detail) ? detail.map(item => item.msg).join('; ') : detail;
    throw new Error(message || `Scanner API request failed (${response.status}).`);
  }
  return payload;
}

export { API_BASE_URL };
