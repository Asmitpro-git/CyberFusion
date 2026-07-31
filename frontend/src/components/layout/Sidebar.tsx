import { NavLink } from 'react-router-dom';
import {
  RectangleStackIcon,
  CpuChipIcon,
  BellAlertIcon,
  ExclamationTriangleIcon,
  ShieldCheckIcon,
  GlobeAltIcon,
  ChartBarIcon,
  FingerPrintIcon,
  BeakerIcon,
  UsersIcon,
  Cog6ToothIcon,
  ShieldExclamationIcon,
} from '@heroicons/react/24/outline';

const navigationItems = [
  { to: '/', label: 'Dashboard', icon: RectangleStackIcon },
  { to: '/assets', label: 'Assets', icon: CpuChipIcon },
  { to: '/alerts', label: 'Alerts', icon: BellAlertIcon },
  { to: '/incidents', label: 'Incidents', icon: ExclamationTriangleIcon },
  { to: '/threat-intelligence', label: 'Threat Intelligence', icon: ShieldCheckIcon },
  { to: '/network', label: 'Network', icon: GlobeAltIcon },
  { to: '/mitre-attack', label: 'MITRE ATT&CK', icon: ChartBarIcon },
  { to: '/forensics', label: 'Forensics', icon: FingerPrintIcon },
  { to: '/users', label: 'Users', icon: UsersIcon },
  { to: '/settings', label: 'Settings', icon: Cog6ToothIcon },
];

interface SidebarProps {
  mobile?: boolean;
}

export default function Sidebar({ mobile = false }: SidebarProps) {
  return (
    <aside
      className={[
        'h-screen w-72 shrink-0 border-r border-white/5 bg-cyber-sidebar/95 px-4 py-5 shadow-glow backdrop-blur',
        mobile ? 'flex flex-col xl:hidden' : 'hidden xl:flex xl:flex-col',
      ].join(' ')}
    >
      <div className="mb-8 flex items-center gap-3 rounded-2xl border border-white/6 bg-white/5 px-4 py-3">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-cyber-primary/15 text-cyber-primary">
          <ShieldExclamationIcon className="h-6 w-6" />
        </div>
        <div>
          <p className="text-sm font-semibold tracking-[0.18em] text-cyber-primary">CYBERFUSION AI</p>
          <p className="text-xs text-slate-400">Autonomous Security Operations</p>
        </div>
      </div>

      <nav className="space-y-1 overflow-y-auto pr-1">
        {navigationItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.to === '/'}
              className={({ isActive }) =>
                [
                  'group flex items-center gap-3 rounded-2xl px-4 py-3 text-sm font-medium transition-all duration-200',
                  isActive
                    ? 'bg-cyber-primary/12 text-cyber-primary shadow-[inset_0_0_0_1px_rgba(0,255,136,0.18)]'
                    : 'text-slate-300 hover:bg-white/5 hover:text-white',
                ].join(' ')
              }
            >
              <Icon className="h-5 w-5 transition-transform duration-200 group-hover:scale-110" />
              {item.label}
            </NavLink>
          );
        })}
      </nav>

      <div className="mt-auto rounded-3xl border border-cyber-primary/20 bg-gradient-to-br from-cyber-primary/10 to-transparent p-4 text-sm text-slate-300">
        <p className="font-semibold text-white">SOC Command Center</p>
        <p className="mt-2 leading-6 text-slate-400">
          Foundation only. Detection, AI, and threat intelligence modules will be added later.
        </p>
      </div>
    </aside>
  );
}
