import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import App from './App.jsx';

beforeEach(() => vi.stubGlobal('fetch', vi.fn()));
afterEach(() => { cleanup(); vi.unstubAllGlobals(); });

describe('Aegis homepage', () => {
  it('renders the URL analysis placeholder', () => {
    render(<MemoryRouter><App /></MemoryRouter>);
    expect(screen.getByRole('heading', { name: /stay ahead of every threat/i })).toBeInTheDocument();
    expect(screen.getByRole('textbox', { name: /url to scan/i })).toBeInTheDocument();
  });

  it('shows the actual backend result returned by the API client', async () => {
    fetch.mockResolvedValue({ ok: true, json: async () => ({
      submitted_url: 'https://example.com', verdict: 'no_obvious_indicators', risk_score: 0,
      findings: [], analysis_method: 'deterministic_url_string_heuristics', model_status: 'not_configured',
      disclaimer: 'No obvious indicators does not establish that a URL is safe.',
    }) });
    render(<MemoryRouter><App /></MemoryRouter>);
    fireEvent.change(screen.getByRole('textbox', { name: /url to scan/i }), { target: { value: 'https://example.com' } });
    fireEvent.click(screen.getByRole('button', { name: /analyze url/i }));
    expect(await screen.findByText('no obvious indicators')).toBeInTheDocument();
    expect(screen.getByText(/not a probability/i)).toBeInTheDocument();
    expect(fetch).toHaveBeenCalledWith('http://localhost:8000/api/scanner/scan', expect.objectContaining({
      method: 'POST', body: JSON.stringify({ url: 'https://example.com' }),
    }));
  });

  it('shows API failures as errors without rendering a scan result', async () => {
    fetch.mockRejectedValue(new Error('Network is offline'));
    render(<MemoryRouter><App /></MemoryRouter>);
    fireEvent.change(screen.getByRole('textbox', { name: /url to scan/i }), { target: { value: 'https://example.com' } });
    fireEvent.click(screen.getByRole('button', { name: /analyze url/i }));
    expect(await screen.findByRole('alert')).toHaveTextContent(/could not reach/i);
    expect(screen.queryByLabelText('Scan result')).not.toBeInTheDocument();
  });

  it('rejects malformed input before contacting the backend', async () => {
    render(<MemoryRouter><App /></MemoryRouter>);
    fireEvent.change(screen.getByRole('textbox', { name: /url to scan/i }), { target: { value: 'ftp://example.com' } });
    fireEvent.click(screen.getByRole('button', { name: /analyze url/i }));
    await waitFor(() => expect(screen.getByRole('alert')).toBeInTheDocument());
    expect(fetch).not.toHaveBeenCalled();
  });
});
