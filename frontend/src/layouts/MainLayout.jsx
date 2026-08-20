import { BarChart3 } from 'lucide-react'
import { NavLink, Outlet } from 'react-router-dom'

const navigation = [['Dashboard', '/dashboard'], ['Demanda', '/demanda'], ['Ocupación', '/ocupacion'], ['Tiempo de recorrido', '/tiempo-recorrido'], ['Cobertura', '/cobertura'], ['Mapa', '/mapa'], ['Comparación', '/comparacion'], ['Transición Ruta 1', '/transicion-ruta-1']]

export default function MainLayout() {
  return <div className="min-h-screen bg-slate-50"><header className="border-b border-slate-200 bg-white"><div className="mx-auto flex max-w-6xl items-center gap-3 px-6 py-4"><BarChart3 className="text-cyan-700" aria-hidden="true" /><span className="font-semibold text-slate-800">RUTAMAR · Análisis de transporte</span></div></header><nav className="border-b border-slate-200 bg-white" aria-label="Navegación principal"><div className="mx-auto flex max-w-6xl gap-1 overflow-x-auto px-6">{navigation.map(([label, path]) => <NavLink key={path} to={path} className={({ isActive }) => `whitespace-nowrap px-3 py-3 text-sm ${isActive ? 'border-b-2 border-cyan-700 font-medium text-cyan-800' : 'text-slate-600 hover:text-slate-900'}`}>{label}</NavLink>)}</div></nav><main className="mx-auto max-w-6xl px-6 py-10"><Outlet /></main></div>
}
