import { BarChart3 } from 'lucide-react'
import { NavLink, Outlet } from 'react-router-dom'
import logoRutamar from '../../logo_rutamar.png'

const navigation = [['Dashboard', '/dashboard'], ['Transición Ruta 1', '/transicion-ruta-1'], ['Mapa', '/mapa'], ['Captura de ruta', '/captura']]

export default function MainLayout() {
  return <div className="min-h-screen bg-[#f7f7f8]"><header className="border-b border-slate-200 bg-white"><div className="mx-auto flex max-w-[1600px] items-center gap-3 px-6 py-3"><img src={logoRutamar} alt="RUTAMAR" className="h-12 w-auto object-contain" /><span className="font-semibold text-slate-800">Análisis de transporte</span></div></header><nav className="border-b border-slate-200 bg-white" aria-label="Navegación principal"><div className="mx-auto flex max-w-[1600px] gap-1 overflow-x-auto px-6">{navigation.map(([label, path]) => <NavLink key={path} to={path} className={({ isActive }) => `whitespace-nowrap px-3 py-3 text-sm ${isActive ? 'border-b-2 border-cyan-700 font-medium text-cyan-800' : 'text-slate-600 hover:text-slate-900'}`}>{label}</NavLink>)}</div></nav><main className="mx-auto max-w-[1600px] px-6 py-8"><Outlet /></main></div>
}
