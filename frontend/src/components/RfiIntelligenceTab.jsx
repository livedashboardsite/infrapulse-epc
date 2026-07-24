import { useState, useEffect } from 'react';
import { Search, FileText, Clock, CheckCircle } from 'lucide-react';

export default function RfiIntelligenceTab() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [allRfis, setAllRfis] = useState([]);

  useEffect(() => {
    fetch('/api/rfi/all').then(res => res.json()).then(setAllRfis);
  }, []);

  const handleSearch = async () => {
    const res = await fetch(`/api/rfi/search?query=${encodeURIComponent(query)}`);
    const data = await res.json();
    // data may be {results:[...]}, or {total_results:N, results:[...]}, or a plain string fallback
    const parsed = Array.isArray(data) ? data : (Array.isArray(data?.results) ? data.results : []);
    setResults(parsed);
  };

  return (
    <div className="space-y-6">
      <div className="liquid-panel p-6">
        <h2 className="text-2xl font-bold mb-6" style={{ color: 'var(--text-primary)' }}>RFI & Project Knowledge Agent</h2>
        <div className="flex gap-4 mb-8">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
            placeholder="Search RFIs, submittals, standards..."
            className="flex-1 liquid-btn px-4 py-3 rounded-xl outline-none"
            style={{ color: 'var(--text-primary)' }}
          />
          <button onClick={handleSearch} className="bg-gradient-to-r from-violet-600 to-cyan-500 hover:from-violet-700 hover:to-cyan-600 text-white font-bold px-8 py-3 rounded-xl">
            <Search className="w-5 h-5" />
          </button>
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          <div>
            <h3 className="text-xl font-bold mb-4 flex items-center gap-2" style={{ color: 'var(--text-primary)' }}>
              <Search className="w-6 h-6 text-violet-400" />
              Search Results
            </h3>
            <div className="space-y-4">
              {results.length > 0 ? results.map(rfi => (
                <div key={rfi.id} className="liquid-panel p-4">
                  <p className="font-bold" style={{ color: 'var(--text-primary)' }}>{rfi.id}: {rfi.subject}</p>
                  <p className="text-sm mb-2" style={{ color: 'var(--text-secondary)' }}>{rfi.question}</p>
                  <p style={{ color: 'var(--text-primary)' }} className="mb-2">{rfi.answer}</p>
                  <div className="flex flex-wrap gap-2">
                    {rfi.citations.map((cit, i) => (
                      <span key={i} className="liquid-panel px-3 py-1 text-xs font-semibold gradient-text">{cit}</span>
                    ))}
                  </div>
                </div>
              )) : (
                <p style={{ color: 'var(--text-secondary)' }}>No results yet. Try searching for "cable tray" or "battery room".</p>
              )}
            </div>
          </div>
          <div>
            <h3 className="text-xl font-bold mb-4 flex items-center gap-2" style={{ color: 'var(--text-primary)' }}>
              <FileText className="w-6 h-6 text-cyan-400" />
              Past RFIs
            </h3>
            <div className="space-y-4">
              {allRfis.map(rfi => (
                <div key={rfi.id} className="liquid-panel p-4">
                  <div className="flex items-center justify-between mb-2">
                    <p className="font-bold" style={{ color: 'var(--text-primary)' }}>{rfi.id}: {rfi.subject}</p>
                    <span className="flex items-center gap-1 text-emerald-400 text-sm font-semibold">
                      <CheckCircle className="w-4 h-4" />
                      {rfi.status}
                    </span>
                  </div>
                  <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>{rfi.question}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
