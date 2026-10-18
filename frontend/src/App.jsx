import { Activity, Globe2, Search, ShieldCheck } from 'lucide-react';
import { useState } from 'react';
import { scanUrl } from './services/api.js';
import './scanner.css';

function validateUrl(value) {
  if (!value.trim()) return 'Enter a URL to analyze.';
  if (value.length > 2048) return 'URL must be 2,048 characters or fewer.';
  try {
    const parsed = new URL(value);
    if (!['http:', 'https:'].includes(parsed.protocol) || !parsed.hostname) {
      return 'Enter a complete HTTP or HTTPS URL, including its hostname.';
    }
  } catch {
    return 'Enter a valid HTTP or HTTPS URL, including its hostname.';
  }
  return '';
}

export default function App() {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [result, setResult] = useState(null);

  async function submit(event) {
    event.preventDefault();
    const validationError = validateUrl(url);
    setError(validationError);
    setResult(null);
    if (validationError) return;

    setLoading(true);
    try {
      setResult(await scanUrl(url.trim()));
    } catch (requestError) {
      setError(requestError.message || 'The scanner API is unavailable. Please try again.');
    } finally {
      setLoading(false);
    }
  }

  return <main className="shell"><nav><a className="brand" href="/"><span className="brand-icon"><ShieldCheck size={22}/></span> AEGIS<span className="version">2.0</span></a><span className="nav-state"><i/> URL analysis</span></nav>
    <section className="hero"><div className="eyebrow"><span/> SECURITY OPERATIONS CENTER</div><h1>Stay ahead of<br/><em>every threat.</em></h1><p className="intro">A unified workspace for URL risk analysis and threat intelligence. Start with a URL to see the scanner interface.</p>
      <form className="scan" onSubmit={submit} noValidate><Search size={20}/><input aria-label="URL to scan" placeholder="Enter a URL to analyze (e.g. https://example.com)" value={url} onChange={event=>setUrl(event.target.value)} disabled={loading}/><button type="submit" disabled={loading}>{loading ? 'Analyzing…' : 'Analyze URL'} <span>→</span></button></form>
      {error && <p className="status error" role="alert">{error}</p>}
      {loading && <p className="status" role="status">Analyzing URL text…</p>}
      {result && <section className="result" aria-live="polite" aria-label="Scan result"><div className="result-heading"><h2>Preliminary result</h2><span className={`verdict ${result.verdict}`}>{result.verdict.replaceAll('_', ' ')}</span></div><p className="result-url">{result.submitted_url}</p><p className="result-score">Heuristic indicator points: <strong>{result.risk_score}</strong> <span>(not a probability)</span></p><h3>Findings</h3>{result.findings.length ? <ul>{result.findings.map(finding=><li key={finding.code}><strong>{finding.severity}</strong> · {finding.description}</li>)}</ul> : <p>No listed heuristic indicators were found.</p>}<p className="method">Method: {result.analysis_method.replaceAll('_', ' ')} · Model: {result.model_status}</p><p className="disclaimer">{result.disclaimer}</p></section>}
      <div className="trust"><span><i/> URL-string heuristics</span><span><i/> No URL requests made</span><span><i/> No trained model configured</span></div></section>
    <section className="cards"><article><div className="card-icon"><Search size={19}/></div><h2>URL Analysis</h2><p>Inspect URL characteristics and assess potential risk.</p><span className="coming">PRELIMINARY</span></article><article><div className="card-icon"><Globe2 size={19}/></div><h2>Threat Intelligence</h2><p>Connect external intelligence providers to enrich results.</p><span className="coming">NOT CONNECTED</span></article><article><div className="card-icon"><Activity size={19}/></div><h2>Security Overview</h2><p>A clear view of scan history, alerts, and emerging risks.</p><span className="coming">NOT CONFIGURED</span></article></section>
    <footer><span>AEGIS 2.0 <span className="muted">· Security intelligence platform</span></span><span>Built for a safer web</span></footer></main>;
}
