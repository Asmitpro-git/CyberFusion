import { Link } from 'react-router-dom';

export default function NotFoundPage() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-cyber-bg px-4 text-center">
      <div className="max-w-lg rounded-3xl border border-white/5 bg-cyber-card p-10 shadow-glow">
        <p className="text-sm uppercase tracking-[0.35em] text-cyber-primary">404</p>
        <h1 className="mt-3 text-3xl font-semibold text-white">Page not found</h1>
        <p className="mt-4 text-sm leading-7 text-slate-400">
          The route does not exist in the current foundation build.
        </p>
        <Link
          to="/"
          className="mt-6 inline-flex rounded-2xl bg-cyber-primary px-5 py-3 font-semibold text-cyber-bg"
        >
          Return to dashboard
        </Link>
      </div>
    </main>
  );
}
