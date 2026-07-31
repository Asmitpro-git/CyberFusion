import { useState } from 'react';
import { Bars3Icon } from '@heroicons/react/24/outline';
import { Outlet } from 'react-router-dom';
import Sidebar from '../components/layout/Sidebar';
import Topbar from '../components/layout/Topbar';

export default function Layout() {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="min-h-screen bg-cyber-bg text-white">
      <div className="flex min-h-screen">
        <Sidebar />

        <div className="flex min-w-0 flex-1 flex-col">
          <div className="flex items-center justify-between border-b border-white/5 bg-cyber-sidebar/70 px-4 py-3 xl:hidden">
            <div>
              <p className="text-sm font-semibold tracking-[0.18em] text-cyber-primary">CYBERFUSION AI</p>
              <p className="text-xs text-slate-400">Enterprise Security Foundation</p>
            </div>
            <button
              type="button"
              onClick={() => setSidebarOpen((value) => !value)}
              className="rounded-xl border border-white/10 bg-white/5 p-2 text-slate-300"
              aria-label="Toggle sidebar"
            >
              <Bars3Icon className="h-5 w-5" />
            </button>
          </div>

          {sidebarOpen ? (
            <div className="border-b border-white/5 bg-cyber-sidebar px-4 py-4 xl:hidden">
              <Sidebar mobile />
            </div>
          ) : null}

          <Topbar />

          <main className="flex-1 px-4 py-6 lg:px-6">
            <Outlet />
          </main>
        </div>
      </div>
    </div>
  );
}
