import { useEffect, useState } from 'react'
import { CircleMarker, MapContainer, Polyline, Popup, TileLayer } from 'react-leaflet'
import { getRouteMap } from '../services/api'

const styles = { ruta1Ida: ['Ruta 1 · Ida', '#d7438f'], ruta1Regreso: ['Ruta 1 · Regreso', '#7950f2'], ruta2Ida: ['Ruta 2 · Ida', '#00a96b'], ruta2Regreso: ['Ruta 2 · Regreso', '#1495d1'] }

export default function RouteMap({ filters = {} }) {
  const [mapData, setMapData] = useState(null)
  const [selected, setSelected] = useState('ruta1Ida')
  useEffect(() => { setMapData(null); getRouteMap(filters).then(setMapData) }, [filters.route, filters.period, filters.timeframe, filters.time_value])
  if (!mapData) return <div className="flex h-[520px] items-center justify-center rounded-2xl bg-slate-50 text-slate-500">Cargando rutas geográficas…</div>
  const routeKey = selected.startsWith('ruta1') ? 'ruta_1_sentidos' : 'ruta_2_sentidos'
  const direction = selected.endsWith('Ida') ? 'ida' : 'regreso'
  const active = mapData[routeKey][direction]
  const [label, color] = styles[selected]
  return <div><div className="mb-4 flex flex-wrap gap-2">{Object.entries(styles).map(([key, [name, itemColor]]) => <button type="button" key={key} onClick={() => setSelected(key)} className={`rounded-full px-4 py-2 text-sm font-bold transition ${selected === key ? 'text-white shadow-sm' : 'bg-slate-100 text-slate-600'}`} style={selected === key ? { backgroundColor: itemColor } : {}}>{name}</button>)}</div><p className="mb-4 text-sm text-slate-500">Haz clic en un punto para ver ascensos, descensos y abrir su ubicación exacta.</p><div className="h-[520px] overflow-hidden rounded-2xl"><MapContainer key={selected} center={[21.1619, -86.821]} zoom={12} className="h-full w-full" scrollWheelZoom><TileLayer attribution="© OpenStreetMap" url="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png" subdomains="abcd" /><Polyline positions={active.trazo} pathOptions={{ color, weight: 5, opacity: .9 }} />{active.paradas.map((stop, index) => <CircleMarker key={`${selected}-${index}`} center={[stop.lat, stop.lng]} radius={7} pathOptions={{ color: '#fff', weight: 2, fillColor: color, fillOpacity: 1 }}><Popup><div className="min-w-44"><strong>{stop.nombre}</strong><p className="my-1 text-xs text-slate-500">{label}</p><p>Suben: <b>{stop.ascensos}</b></p><p>Bajan: <b>{stop.descensos}</b></p><a className="mt-2 inline-block font-semibold text-indigo-600 underline" href={`https://www.google.com/maps/search/?api=1&query=${stop.lat},${stop.lng}`} target="_blank" rel="noreferrer">Abrir ubicación exacta</a></div></Popup></CircleMarker>)}</MapContainer></div></div>
}
