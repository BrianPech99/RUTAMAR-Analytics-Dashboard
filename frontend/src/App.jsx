import { Navigate, Route, Routes } from 'react-router-dom'
import MainLayout from './layouts/MainLayout'
import DashboardPage from './pages/DashboardPage'
import TransitionPage from './pages/TransitionPage'

const routes = [['dashboard', 'dashboard'], ['demanda', 'demanda'], ['ocupacion', 'ocupacion'], ['tiempo-recorrido', 'tiempo'], ['cobertura', 'cobertura'], ['mapa', 'mapa'], ['comparacion', 'comparacion']]

export default function App() {
  return <Routes><Route element={<MainLayout />}>{routes.map(([path, focus]) => <Route key={path} path={path} element={<DashboardPage focus={focus} />} />)}<Route path="transicion-ruta-1" element={<TransitionPage />} /></Route><Route path="/" element={<Navigate to="/dashboard" replace />} /><Route path="*" element={<Navigate to="/dashboard" replace />} /></Routes>
}
