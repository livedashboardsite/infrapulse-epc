import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useTheme } from '../context/ThemeContext';
import { useAuth } from '../context/AuthContext';
import Navbar from '../components/Navbar';
import MetricsPanel from '../components/MetricsPanel';
import SpecComplianceTab from '../components/SpecComplianceTab';
import RiskDashboardTab from '../components/RiskDashboardTab';
import CommissioningConsoleTab from '../components/CommissioningConsoleTab';
import RfiIntelligenceTab from '../components/RfiIntelligenceTab';
import { FileCheck, GanttChart, ClipboardList, FileText, BarChart3 } from 'lucide-react';

export default function Dashboard() {
  const { theme } = useTheme();
  const { user, loading } = useAuth();
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('spec');
  const [tasks, setTasks] = useState([]);
  const [metrics, setMetrics] = useState({});
  const [risks, setRisks] = useState({ risks: [] });
  const [weather, setWeather] = useState(null);
  const [supplyChain, setSupplyChain] = useState(null);
  const [commissioningSteps, setCommissioningSteps] = useState([]);
  const [delays, setDelays] = useState({});

  useEffect(() => {
    if (!loading && !user) {
      navigate('/');
    }
  }, [user, loading, navigate]);

  useEffect(() => {
    if (!user) return;

    const fetchData = async () => {
      fetch('http://localhost:8000/api/tasks').then(res => res.json()).then(data => {
        setTasks(data.tasks);
      });

      fetch('http://localhost:8000/api/metrics').then(res => res.json()).then(setMetrics);

      fetch('http://localhost:8000/api/schedule-risks').then(res => res.json()).then(setRisks);

      fetch('http://localhost:8000/api/weather').then(res => res.json()).then(setWeather);

      fetch('http://localhost:8000/api/supply-chain').then(res => res.json()).then(setSupplyChain);

      fetch('http://localhost:8000/api/commissioning/steps').then(res => res.json()).then(setCommissioningSteps);
    };

    fetchData();
  }, [user]);

  const handleInjectDelay = async (taskIds, days) => {
    const newDelays = { ...delays };
    taskIds.forEach(id => {
      newDelays[id] = (newDelays[id] || 0) + days;
    });
    setDelays(newDelays);
    const res = await fetch('http://localhost:8000/api/recalculate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ delays: newDelays })
    });
    const data = await res.json();
    setTasks(data.tasks);
  };

  const tabs = [
    { id: 'spec', name: 'Spec Compliance', icon: FileCheck },
    { id: 'risk', name: 'Schedule & GeoSupply', icon: GanttChart },
    { id: 'commissioning', name: 'Commissioning', icon: ClipboardList },
    { id: 'rfi', name: 'RFI Intelligence', icon: FileText },
    { id: 'metrics', name: 'Metrics', icon: BarChart3 }
  ];

  const projectEndDate = tasks.length > 0 ? tasks[tasks.length - 1].end_date : null;

  if (loading) {
    return (
      <div className={`canvas-background ${theme === 'light' ? 'light-mode' : 'dark-mode'}`}>
      <div className="mesh-gradient"></div>
      <div className="min-h-screen flex items-center justify-center">
        <p style={{ color: 'var(--text-primary)' }}>Loading...</p>
      </div>
      </div>
    );
  }

  return (
    <div className={`canvas-background ${theme === 'light' ? 'light-mode' : 'dark-mode'}`}>
      <div className="mesh-gradient"></div>
      <div className="relative z-10">
        <Navbar projectEndDate={projectEndDate} />
        <div className="px-6 mb-8">
          <div className="flex flex-wrap gap-3 mb-8">
            {tabs.map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`liquid-btn px-6 py-3 rounded-2xl font-semibold flex items-center gap-2 transition-all ${activeTab === tab.id ? 'bg-gradient-to-r from-violet-600 to-cyan-500 text-white' : ''}`}
                style={activeTab !== tab.id ? { color: 'var(--text-primary)' } : {}}
              >
                <tab.icon className="w-5 h-5" />
                {tab.name}
              </button>
            ))}
          </div>

          <div className="pb-12">
            {activeTab === 'spec' && <SpecComplianceTab />}
            {activeTab === 'risk' && <RiskDashboardTab tasks={tasks} risks={risks} weather={weather} supplyChain={supplyChain} />}
            {activeTab === 'commissioning' && <CommissioningConsoleTab steps={commissioningSteps} onInjectDelay={handleInjectDelay} />}
            {activeTab === 'rfi' && <RfiIntelligenceTab />}
            {activeTab === 'metrics' && <MetricsPanel metrics={metrics} />}
          </div>
        </div>
      </div>
    </div>
  );
}
