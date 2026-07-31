import { motion } from 'framer-motion';
import SectionCard from '../components/ui/SectionCard';
import StatCard from '../components/ui/StatCard';

const dashboardStats = [
  { label: 'Total Assets', value: '1,284', detail: '+18 in the last 24h', tone: 'primary' as const },
  { label: 'Active Alerts', value: '42', detail: '7 need immediate review', tone: 'danger' as const },
  { label: 'Incidents', value: '9', detail: '3 unresolved cases', tone: 'warning' as const },
  { label: 'Threat Feed', value: '128', detail: 'Normalized events only', tone: 'info' as const },
  { label: 'Risk Score', value: '73/100', detail: 'Moderate enterprise risk', tone: 'warning' as const },
  { label: 'Network Status', value: 'Stable', detail: 'No service degradation', tone: 'primary' as const },
];

const recentActivity = [
  'Daily log ingestion pipeline initialized.',
  'Asset inventory sync completed successfully.',
  'Alert queue ready for future detection modules.',
  'Baseline logging and request tracing enabled.',
];

export default function DashboardPage() {
  return (
    <div className="space-y-6">
      <motion.div
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.45 }}
        className="rounded-[2rem] border border-white/5 bg-gradient-to-br from-white/8 via-white/5 to-transparent p-6 shadow-glow"
      >
        <p className="text-sm uppercase tracking-[0.35em] text-cyber-primary">Security Operations Center</p>
        <h1 className="mt-3 text-3xl font-semibold text-white md:text-5xl">CyberFusion AI Dashboard</h1>
        <p className="mt-4 max-w-3xl text-sm leading-7 text-slate-300 md:text-base">
          Enterprise foundation for cyber operations, observability, and future security workflows.
          Detection, AI, and threat intelligence modules are intentionally not implemented in Module 1.
        </p>
      </motion.div>

      <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        {dashboardStats.map((stat) => (
          <StatCard key={stat.label} {...stat} />
        ))}
      </section>

      <section className="grid gap-6 xl:grid-cols-3">
        <SectionCard
          title="Recent Activity"
          description="Placeholder operational stream for future integrations."
        >
          <ul className="space-y-3 text-sm text-slate-300">
            {recentActivity.map((item) => (
              <li key={item} className="rounded-2xl border border-white/5 bg-white/5 px-4 py-3">
                {item}
              </li>
            ))}
          </ul>
        </SectionCard>

        <SectionCard title="Operational Notes" description="Foundation-only platform state.">
          <div className="space-y-4 text-sm text-slate-300">
            <p className="rounded-2xl border border-cyber-primary/15 bg-cyber-primary/8 px-4 py-3">
              Backend health, API versioning, and PostgreSQL connectivity are prepared for future services.
            </p>
            <p className="rounded-2xl border border-white/5 bg-white/5 px-4 py-3">
              Frontend routing is in place for all required pages, with no authentication logic yet.
            </p>
          </div>
        </SectionCard>

        <SectionCard title="System Baseline" description="UI shell and enterprise presentation layer.">
          <div className="space-y-4 text-sm text-slate-300">
            <div className="flex items-center justify-between rounded-2xl border border-white/5 bg-white/5 px-4 py-3">
              <span>Theme</span>
              <span className="text-cyber-primary">Dark SOC</span>
            </div>
            <div className="flex items-center justify-between rounded-2xl border border-white/5 bg-white/5 px-4 py-3">
              <span>Layout</span>
              <span className="text-cyber-info">Responsive</span>
            </div>
            <div className="flex items-center justify-between rounded-2xl border border-white/5 bg-white/5 px-4 py-3">
              <span>Stack</span>
              <span className="text-cyber-warning">React 19 + Vite</span>
            </div>
          </div>
        </SectionCard>
      </section>
    </div>
  );
}
