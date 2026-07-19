import { Sun, Moon, LogOut, Sparkles, Clock } from 'lucide-react';
import { useTheme } from '../context/ThemeContext';
import { useAuth } from '../context/AuthContext';

export default function Navbar({ projectEndDate }) {
  const { theme, toggleTheme } = useTheme();
  const { company, logout } = useAuth();

  return (
    <nav className="px-6 py-4 flex flex-wrap justify-between items-center gap-4">
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-violet-500 to-cyan-400 flex items-center justify-center">
          <Sparkles className="text-white w-6 h-6" />
        </div>
        <div>
          <span className="text-2xl font-bold gradient-text">InfraPulse EPC</span>
          {company && <p style={{ color: 'var(--text-secondary)' }} className="text-sm">{company.name} · {company.mwCapacity}MW · {company.tierLevel}</p>}
        </div>
      </div>

      <div className="flex items-center gap-4">
        <div className="liquid-panel px-4 py-2 flex items-center gap-2">
          <Clock className="w-5 h-5 text-violet-400" />
          <div>
            <p className="text-xs" style={{ color: 'var(--text-secondary)' }}>Est. Completion</p>
            <p className="font-bold" style={{ color: 'var(--text-primary)' }}>{projectEndDate ? new Date(projectEndDate).toLocaleDateString() : 'Calculating...'}</p>
          </div>
        </div>
        <div className="liquid-panel px-4 py-2 flex items-center gap-2">
          <span className="w-3 h-3 rounded-full bg-emerald-400 animate-pulse"></span>
          <span style={{ color: 'var(--text-primary)' }} className="font-semibold">5 Agents Active</span>
        </div>
        <button onClick={toggleTheme} className="liquid-btn p-2 rounded-xl">
          {theme === 'light' ? <Moon className="w-5 h-5" style={{ color: 'var(--text-primary)' }} /> : <Sun className="w-5 h-5" style={{ color: 'var(--text-primary)' }} />}
        </button>
        <button onClick={logout} className="liquid-btn p-2 rounded-xl">
          <LogOut className="w-5 h-5" style={{ color: 'var(--text-primary)' }} />
        </button>
      </div>
    </nav>
  );
}
