interface StatCardProps {
  label: string;
  value: string;
  detail: string;
  tone?: 'primary' | 'danger' | 'warning' | 'info';
}

const toneClasses: Record<NonNullable<StatCardProps['tone']>, string> = {
  primary: 'text-cyber-primary',
  danger: 'text-cyber-danger',
  warning: 'text-cyber-warning',
  info: 'text-cyber-info',
};

export default function StatCard({ label, value, detail, tone = 'primary' }: StatCardProps) {
  return (
    <div className="rounded-3xl border border-white/5 bg-white/5 p-5 shadow-glow">
      <p className="text-sm text-slate-400">{label}</p>
      <div className={`mt-3 text-3xl font-semibold ${toneClasses[tone]}`}>{value}</div>
      <p className="mt-2 text-sm text-slate-300">{detail}</p>
    </div>
  );
}
