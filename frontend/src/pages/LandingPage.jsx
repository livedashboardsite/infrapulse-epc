import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Zap, Shield, Truck, ClipboardList, BarChart3, ChevronRight, Sun, Moon, Building2, Users, Sparkles } from 'lucide-react';
import { useTheme } from '../context/ThemeContext';
import { useAuth } from '../context/AuthContext';

export default function LandingPage() {
  const { theme, toggleTheme } = useTheme();
  const { loginDemo } = useAuth();
  const navigate = useNavigate();
  const [mwSize, setMwSize] = useState(50);

  const handleLaunchPlatform = () => {
    loginDemo('adani-connex');
    navigate('/dashboard');
  };

  const calculatedSavings = (mwSize * 10000).toLocaleString();

  return (
    <div className={`canvas-background ${theme === 'light' ? 'light-mode' : 'dark-mode'}`}>
      <div className="mesh-gradient"></div>
      <div className="relative z-10">
        <nav className="px-6 py-4 flex justify-between items-center">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-violet-500 to-cyan-400 flex items-center justify-center">
              <Sparkles className="text-white w-6 h-6" />
            </div>
            <span className="text-2xl font-bold gradient-text">InfraPulse EPC</span>
          </div>
          <div className="flex items-center gap-4">
            <button onClick={toggleTheme} className="liquid-btn p-2 rounded-xl">
              {theme === 'light' ? <Moon className="w-5 h-5" style={{ color: 'var(--text-primary)' }} /> : <Sun className="w-5 h-5" style={{ color: 'var(--text-primary)' }} />}
            </button>
            <button onClick={() => { loginDemo('adani-connex'); navigate('/dashboard'); }} className="liquid-btn px-5 py-2 rounded-xl font-semibold" style={{ color: 'var(--text-primary)' }}>
              Sign In
            </button>
          </div>
        </nav>

        <section className="px-6 py-16 max-w-7xl mx-auto">
          <div className="text-center mb-12">
            <div className="flex flex-wrap justify-center gap-3 mb-6">
              <div className="liquid-panel px-4 py-2 flex items-center gap-2">
                <Zap className="w-4 h-4 text-amber-400" />
                <span style={{ color: 'var(--text-secondary)' }}>Agent: Spec Compliance</span>
              </div>
              <div className="liquid-panel px-4 py-2 flex items-center gap-2">
                <Shield className="w-4 h-4 text-emerald-400" />
                <span style={{ color: 'var(--text-secondary)' }}>Agent: Schedule Risk</span>
              </div>
              <div className="liquid-panel px-4 py-2 flex items-center gap-2">
                <Truck className="w-4 h-4 text-cyan-400" />
                <span style={{ color: 'var(--text-secondary)' }}>Agent: Supply Chain</span>
              </div>
              <div className="liquid-panel px-4 py-2 flex items-center gap-2">
                <ClipboardList className="w-4 h-4 text-violet-400" />
                <span style={{ color: 'var(--text-secondary)' }}>Agent: Commissioning</span>
              </div>
            </div>
            <h1 className="text-6xl md:text-7xl font-extrabold mb-6 leading-tight" style={{ color: 'var(--text-primary)' }}>
              AI Intelligence Layer for<br />
              <span className="gradient-text">Data Centre EPC Project Delivery</span>
            </h1>
            <p className="text-xl mb-8 max-w-3xl mx-auto" style={{ color: 'var(--text-secondary)' }}>
              Multi-agent orchestration that unifies compliance, scheduling, weather, supply chain, and commissioning to eliminate delays.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button onClick={handleLaunchPlatform} className="bg-gradient-to-r from-violet-600 to-cyan-500 hover:from-violet-700 hover:to-cyan-600 text-white font-bold py-4 px-10 rounded-2xl text-lg shadow-2xl transform hover:-translate-y-1 transition-all">
                Launch Platform
              </button>
              <button onClick={() => { loginDemo('ctrls-datacenters'); navigate('/dashboard'); }} className="liquid-btn py-4 px-10 rounded-2xl font-bold text-lg" style={{ color: 'var(--text-primary)' }}>
                Demo as CtrlS Datacenters
              </button>
            </div>
          </div>

          <div className="grid md:grid-cols-2 gap-12 mb-20">
            <div className="liquid-panel p-8">
              <h2 className="text-3xl font-bold mb-6 flex items-center gap-3" style={{ color: 'var(--text-primary)' }}>
                <Sparkles className="w-8 h-8 text-violet-500" />
                How It Works
              </h2>
              <div className="space-y-6">
                {[
                  { icon: Building2, title: 'Raw Data Ingestion', desc: 'Submittals, drawings, schedules, weather feeds' },
                  { icon: Zap, title: 'Multi-Agent Analysis', desc: '5 specialized agents process signals in parallel' },
                  { icon: BarChart3, title: 'Risk Graph', desc: 'Unified risk surface with critical path impact' },
                  { icon: Shield, title: 'Auto-Mitigation', desc: 'Prescriptive actions & schedule recalculation' }
                ].map((step, i) => (
                  <div key={i} className="flex gap-4">
                    <div className="liquid-btn p-3 rounded-xl flex-shrink-0">
                      <step.icon className="w-6 h-6 text-cyan-400" />
                    </div>
                    <div>
                      <h3 className="font-bold text-lg mb-1" style={{ color: 'var(--text-primary)' }}>{step.title}</h3>
                      <p style={{ color: 'var(--text-secondary)' }}>{step.desc}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="liquid-panel p-8">
              <h2 className="text-3xl font-bold mb-6" style={{ color: 'var(--text-primary)' }}>ROI Calculator</h2>
              <div className="mb-4">
                <div className="flex justify-between mb-2" style={{ color: 'var(--text-primary)' }}>
                  <span className="font-semibold">Project Size</span>
                  <span className="font-bold">{mwSize} MW</span>
                </div>
                <input type="range" min="50" max="250" value={mwSize} onChange={(e) => setMwSize(Number(e.target.value))} className="w-full h-2 rounded-lg appearance-none cursor-pointer" style={{ background: 'linear-gradient(to right, #8B5CF6, #06B6D4)' }} />
              </div>
              <div className="liquid-panel p-6 mt-6 text-center">
                <p className="text-sm mb-2" style={{ color: 'var(--text-secondary)' }}>Estimated Savings from Delay Prevention</p>
                <p className="text-4xl font-extrabold gradient-text">${calculatedSavings}</p>
              </div>
            </div>
          </div>

          <div className="mb-20">
            <h2 className="text-3xl font-bold mb-8 text-center" style={{ color: 'var(--text-primary)' }}>Enterprise Pricing</h2>
            <div className="grid md:grid-cols-3 gap-8">
              {[
                { name: 'Starter', price: '$2,500', features: ['Up to 20 MW', '3 Agents', 'Email Support'] },
                { name: 'Growth', price: '$7,500', features: ['Up to 100 MW', '5 Agents', 'Dedicated PM'], recommended: true },
                { name: 'Hyperscale', price: 'Custom', features: ['Unlimited MW', 'Custom Agents', 'Onsite Support'] }
              ].map((plan, i) => (
                <div key={i} className={`liquid-panel p-8 ${plan.recommended ? 'border-2 border-violet-500 scale-105' : ''}`}>
                  <h3 className="text-2xl font-bold mb-2" style={{ color: 'var(--text-primary)' }}>{plan.name}</h3>
                  <p className="text-4xl font-extrabold mb-6 gradient-text">{plan.price}<span className="text-lg font-normal" style={{ color: 'var(--text-secondary)' }}>/mo</span></p>
                  <ul className="space-y-3 mb-8">
                    {plan.features.map((feat, j) => (
                      <li key={j} className="flex items-center gap-2" style={{ color: 'var(--text-primary)' }}>
                        <span className="text-emerald-400">✓</span> {feat}
                      </li>
                    ))}
                  </ul>
                  <button onClick={handleLaunchPlatform} className="w-full liquid-btn py-3 rounded-xl font-bold" style={{ color: 'var(--text-primary)' }}>
                    Get Started
                  </button>
                </div>
              ))}
            </div>
          </div>

          <footer className="text-center py-12 border-t" style={{ borderColor: 'var(--glass-border)' }}>
            <div className="flex justify-center gap-6 mb-6">
              <div className="liquid-panel px-4 py-2">Uptime Institute</div>
              <div className="liquid-panel px-4 py-2">TIA-942</div>
              <div className="liquid-panel px-4 py-2">BICSI</div>
            </div>
            <p style={{ color: 'var(--text-secondary)' }}>© 2024 InfraPulse EPC. Built for the ET AI Hackathon.</p>
          </footer>
        </section>
      </div>
    </div>
  );
}
