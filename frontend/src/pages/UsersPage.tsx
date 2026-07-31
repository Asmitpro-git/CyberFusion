import SectionCard from '../components/ui/SectionCard';

export default function UsersPage() {
  return (
    <SectionCard title="Users" description="Placeholder user administration page.">
      <div className="rounded-2xl border border-white/5 bg-white/5 px-4 py-6 text-sm text-slate-300">
        User management and RBAC are intentionally not implemented yet.
      </div>
    </SectionCard>
  );
}
