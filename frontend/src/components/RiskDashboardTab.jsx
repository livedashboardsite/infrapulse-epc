import { useState, useEffect } from 'react';
import { GanttChart, AlertTriangle, CloudRain, Truck, MapPin, Calendar } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';

export default function RiskDashboardTab({ tasks, risks, weather, supplyChain }) {
  const ganttData = tasks.slice(0, 10).map(t => ({
    name: t.name,
    start: new Date(t.start_date).getTime(),
    end: new Date(t.end_date).getTime(),
    critical: t.is_critical
  }));

  return (
    <div className="grid lg:grid-cols-3 gap-6">
      <div className="lg:col-span-2 space-y-6">
        <div className="liquid-panel p-6">
          <div className="flex items-center gap-3 mb-6">
            <GanttChart className="w-7 h-7 text-violet-400" />
            <h2 className="text-2xl font-bold" style={{ color: 'var(--text-primary)' }}>Schedule & CPM Critical Path</h2>
          </div>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={ganttData} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                <XAxis type="number" domain={['dataMin', 'dataMax']} tickFormatter={(ts) => new Date(ts).toLocaleDateString()} stroke="var(--text-secondary)" />
                <YAxis dataKey="name" type="category" width={200} stroke="var(--text-secondary)" />
                <Tooltip
                  contentStyle={{ backgroundColor: 'var(--glass-bg)', borderColor: 'var(--glass-border)', borderRadius: '12px', backdropFilter: 'blur(10px)' }}
                  labelStyle={{ color: 'var(--text-primary)' }}
                  formatter={(value) => new Date(value).toLocaleDateString()}
                />
                <Bar dataKey="end" hide>
                  {ganttData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill="transparent" />
                  ))}
                </Bar>
                <Bar dataKey="start" hide>
                  {ganttData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill="transparent" />
                  ))}
                </Bar>
                <Bar dataKey={(d) => d.end - d.start} background={{ fill: '#333' }} radius={[4, 4, 4, 4]}>
                  {ganttData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.critical ? '#F43F5E' : '#10B981'} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="liquid-panel p-6">
          <div className="flex items-center gap-3 mb-6">
            <AlertTriangle className="w-7 h-7 text-amber-400" />
            <h2 className="text-2xl font-bold" style={{ color: 'var(--text-primary)' }}>Risk Register</h2>
          </div>
          <div className="space-y-4">
            {risks.risks.map((risk, i) => (
              <div key={i} className="liquid-panel p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-bold" style={{ color: 'var(--text-primary)' }}>{risk.task_name} · {risk.risk_type}</p>
                    <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>{risk.mitigation}</p>
                  </div>
                  <span className={`px-3 py-1 rounded-full text-sm font-bold ${risk.severity === 'High' ? 'bg-coral-danger text-white' : 'bg-amber-warning text-black'}`}>{risk.severity}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="space-y-6">
        <div className="liquid-panel p-6">
          <div className="flex items-center gap-3 mb-6">
            <CloudRain className="w-7 h-7 text-cyan-400" />
            <h2 className="text-2xl font-bold" style={{ color: 'var(--text-primary)' }}>Live Weather</h2>
          </div>
          {weather && (
            <div>
              <div className="flex items-center justify-between mb-4">
                <div>
                  <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>{weather.location}</p>
                  <p className="text-4xl font-bold gradient-text">{weather.current.temperature}°C</p>
                </div>
                <div className={`liquid-panel p-4 ${weather.operation_safe ? 'border-emerald-400' : 'border-coral-danger'} border-2`}>
                  <p className="font-bold text-sm" style={{ color: 'var(--text-primary)' }}>{weather.operation_safe ? 'Safe to Operate' : 'Operations Halted'}</p>
                </div>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div className="liquid-panel p-3 text-center">
                  <p className="text-2xl font-bold" style={{ color: 'var(--text-primary)' }}>{weather.current.wind_speed} km/h</p>
                  <p className="text-xs" style={{ color: 'var(--text-secondary)' }}>Wind Speed</p>
                </div>
                <div className="liquid-panel p-3 text-center">
                  <p className="text-2xl font-bold" style={{ color: 'var(--text-primary)' }}>{weather.current.precipitation} mm</p>
                  <p className="text-xs" style={{ color: 'var(--text-secondary)' }}>Precipitation</p>
                </div>
              </div>
              {weather.warning && <p className="mt-4 text-coral-danger font-semibold">{weather.warning}</p>}
            </div>
          )}
        </div>

        <div className="liquid-panel p-6">
          <div className="flex items-center gap-3 mb-6">
            <Truck className="w-7 h-7 text-cyan-400" />
            <h2 className="text-2xl font-bold" style={{ color: 'var(--text-primary)' }}>Supply Chain</h2>
          </div>
          {supplyChain && supplyChain.shipments.map((ship, i) => (
            <div key={i} className="liquid-panel p-4 mb-4">
              <div className="flex items-center justify-between mb-3">
                <p className="font-bold" style={{ color: 'var(--text-primary)' }}>{ship.item}</p>
                <span className="text-emerald-400 font-semibold text-sm">{ship.status}</span>
              </div>
              <div className="flex items-center gap-2 text-sm mb-3" style={{ color: 'var(--text-secondary)' }}>
                <MapPin className="w-4 h-4" />
                <span>{ship.origin} → {ship.destination}</span>
              </div>
              <div className="flex items-center gap-2 text-sm mb-3" style={{ color: 'var(--text-secondary)' }}>
                <Calendar className="w-4 h-4" />
                <span>ETA: {ship.eta_days} days</span>
              </div>
              {ship.mitigations.map((mit, j) => (
                <button key={j} className="w-full liquid-btn py-2 rounded-xl text-sm font-semibold mt-2" style={{ color: 'var(--text-primary)' }}>
                  {mit.option} · ${mit.cost_usd.toLocaleString()} · Save {mit.time_saved_days} days
                </button>
              ))}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
