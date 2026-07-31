import { Link } from 'react-router-dom';

export default function LoginPage() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-cyber-bg px-4">
      <div className="w-full max-w-md rounded-3xl border border-white/5 bg-cyber-card p-8 shadow-glow">
        <p className="text-sm uppercase tracking-[0.35em] text-cyber-primary">CyberFusion AI</p>
        <h1 className="mt-3 text-3xl font-semibold text-white">Sign in</h1>
        <p className="mt-2 text-sm text-slate-400">Authentication logic is intentionally not implemented yet.</p>
        <div className="mt-6 space-y-4">
          <div className="rounded-2xl border border-white/5 bg-white/5 px-4 py-3 text-sm text-slate-300">Email input placeholder</div>
          <div className="rounded-2xl border border-white/5 bg-white/5 px-4 py-3 text-sm text-slate-300">Password input placeholder</div>
          <button type="button" className="w-full rounded-2xl bg-cyber-primary px-4 py-3 font-semibold text-cyber-bg">
            Login placeholder
          </button>
        </div>
        <p className="mt-6 text-sm text-slate-400">
          Need an account? <Link to="/register" className="text-cyber-primary">Register</Link>
        </p>
      </div>
    </main>
  );
}
