import { useEffect, useState } from 'react';
import { BellIcon, MagnifyingGlassIcon, MoonIcon, SunIcon } from '@heroicons/react/24/outline';

export default function Topbar() {
  const [currentTime, setCurrentTime] = useState(() => new Date());
  const [darkMode, setDarkMode] = useState(true);

  useEffect(() => {
    const timer = window.setInterval(() => {
      setCurrentTime(new Date());
    }, 1000);

    return () => window.clearInterval(timer);
  }, []);

  useEffect(() => {
    document.documentElement.classList.toggle('dark', darkMode);
  }, [darkMode]);

  return (
    <header className="sticky top-0 z-30 border-b border-white/5 bg-cyber-bg/85 backdrop-blur-xl">
      <div className="flex items-center justify-between gap-4 px-4 py-4 lg:px-6">
        <div className="flex min-w-0 flex-1 items-center gap-3 rounded-2xl border border-white/5 bg-white/5 px-4 py-3 shadow-glow">
          <MagnifyingGlassIcon className="h-5 w-5 text-slate-400" />
          <input
            type="search"
            placeholder="Search assets, alerts, incidents..."
            className="w-full border-0 bg-transparent p-0 text-sm text-white placeholder:text-slate-500 focus:outline-none focus:ring-0"
          />
        </div>

        <div className="hidden items-center gap-3 md:flex">
          <div className="rounded-2xl border border-white/5 bg-white/5 px-4 py-3 text-sm text-slate-300 shadow-glow">
            {currentTime.toLocaleString()}
          </div>
          <button
            type="button"
            className="flex h-12 w-12 items-center justify-center rounded-2xl border border-white/5 bg-white/5 text-slate-300 transition hover:bg-white/10 hover:text-white"
            aria-label="Notifications"
          >
            <BellIcon className="h-5 w-5" />
          </button>
          <button
            type="button"
            onClick={() => setDarkMode((value) => !value)}
            className="flex h-12 w-12 items-center justify-center rounded-2xl border border-white/5 bg-white/5 text-slate-300 transition hover:bg-white/10 hover:text-white"
            aria-label="Toggle dark mode"
          >
            {darkMode ? <MoonIcon className="h-5 w-5" /> : <SunIcon className="h-5 w-5" />}
          </button>
          <div className="flex items-center gap-3 rounded-2xl border border-white/5 bg-white/5 px-3 py-2">
            <div className="flex h-10 w-10 items-center justify-center rounded-full bg-cyber-primary/15 text-sm font-semibold text-cyber-primary">
              CF
            </div>
            <div>
              <p className="text-sm font-medium text-white">Security Operator</p>
              <p className="text-xs text-slate-500">Read-only foundation</p>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}
