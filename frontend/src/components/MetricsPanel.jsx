import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export default function MetricsPanel({ metrics }) {
  const chartData = [
    { name: 'Lead Time', value: metrics.days_delay_warning_lead_time, unit: 'days' },
    { name: 'Automation', value: metrics.test_automation_coverage_percent, unit: '%' },
    { name: 'Accuracy', value: metrics.spec_compliance_accuracy_percent, unit: '%' },
    { name: 'Hours Saved', value: metrics.hours_saved_per_week, unit: 'hrs/wk' }
  ];

  return (
    <div className="liquid-panel p-6">
      <h2 className="text-2xl font-bold mb-6" style={{ color: 'var(--text-primary)' }}>Benchmark Metrics</h2>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        {[
          { label: 'Delay Warning Lead Time', value: `${metrics.days_delay_warning_lead_time} days`, color: 'violet' },
          { label: 'Test Automation Coverage', value: `${metrics.test_automation_coverage_percent}%`, color: 'emerald' },
          { label: 'Spec Compliance Accuracy', value: `${metrics.spec_compliance_accuracy_percent}%`, color: 'cyan' },
          { label: 'Hours Saved', value: `${metrics.hours_saved_per_week}/wk`, color: 'amber' }
        ].map((stat, i) => (
          <div key={i} className="liquid-panel p-4 text-center">
            <p className="text-3xl font-bold gradient-text">{stat.value}</p>
            <p style={{ color: 'var(--text-secondary)' }} className="text-sm">{stat.label}</p>
          </div>
        ))}
      </div>
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
            <XAxis dataKey="name" stroke="var(--text-secondary)" />
            <YAxis stroke="var(--text-secondary)" />
            <Tooltip
              contentStyle={{
                backgroundColor: 'var(--glass-bg)',
                borderColor: 'var(--glass-border)',
                borderRadius: '12px',
                backdropFilter: 'blur(10px)'
              }}
              labelStyle={{ color: 'var(--text-primary)' }}
            />
            <Bar dataKey="value" fill="url(#colorGradient)" radius={[8, 8, 0, 0]} />
            <defs>
              <linearGradient id="colorGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#8B5CF6" />
                <stop offset="100%" stopColor="#06B6D4" />
              </linearGradient>
            </defs>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
