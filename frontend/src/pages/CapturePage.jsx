import { useEffect, useMemo, useState } from 'react'
import { ArrowLeft, ArrowRight, BusFront, CheckCircle2, Minus, Plus, Save } from 'lucide-react'
import { getCaptureOptions, saveCapture } from '../services/api'

const cardBase = 'flex min-h-20 flex-col items-center justify-center rounded-2xl border bg-slate-50 px-4 py-3 text-center transition'
const nowForInput = () => new Date(Date.now() - new Date().getTimezoneOffset() * 60000).toISOString().slice(0, 16)

function SelectCard({ active, onClick, children, tone = 'indigo' }) {
  const selected = tone === 'pink' ? 'border-pink-500 bg-cyan-50 text-pink-600 shadow-sm' : tone === 'orange' ? 'border-orange-500 bg-orange-50 text-orange-700 shadow-sm' : 'border-indigo-600 bg-indigo-50 text-indigo-700 shadow-sm'
  return <button type="button" onClick={onClick} className={`${cardBase} ${active ? selected : 'border-slate-100 text-slate-400 hover:border-slate-300'}`}>{active && <CheckCircle2 className="absolute right-4 top-3" size={16} />} {children}</button>
}

export default function CapturePage() {
  const [options, setOptions] = useState([])
  const [routeId, setRouteId] = useState('ruta-1')
  const [unit, setUnit] = useState('')
  const [direction, setDirection] = useState('ida')
  const [stopName, setStopName] = useState('')
  const [schedule, setSchedule] = useState('')
  const [boardings, setBoardings] = useState(0)
  const [alightings, setAlightings] = useState(0)
  const [realDate, setRealDate] = useState(nowForInput())
  const [notes, setNotes] = useState('')
  const [status, setStatus] = useState('')
  const [error, setError] = useState('')

  useEffect(() => { getCaptureOptions().then(({ rutas }) => { setOptions(rutas); const first = rutas[0]; if (first) { setRouteId(first.id); setUnit(first.unidades[0] || '') } }).catch(() => setError('No fue posible cargar las opciones de captura.')) }, [])
  const route = useMemo(() => options.find((item) => item.id === routeId), [options, routeId])
  const stops = route?.sentidos?.[direction] || []
  const selectedStop = stops.find((item) => item.nombre === stopName)
  const schedules = selectedStop?.horarios || []
  const chooseRoute = (id) => { const selected = options.find((item) => item.id === id); setRouteId(id); setUnit(selected?.unidades?.[0] || ''); setStopName(''); setSchedule(''); setStatus('') }
  const chooseDirection = (value) => { setDirection(value); setStopName(''); setSchedule(''); setStatus('') }
  const selectStop = (value) => { setStopName(value); setSchedule(''); setStatus('') }
  const save = async (event) => {
    event.preventDefault(); setError(''); setStatus('')
    if (!route || !unit || !stopName || !schedule || !realDate) { setError('Selecciona ruta, camión, sentido, paradero, horario y fecha real.'); return }
    try {
      const result = await saveCapture({ ruta_csv: route.ruta_csv, unidad: unit, sentido: direction === 'ida' ? 'Ida' : 'Regreso', paradero: stopName, horario_programado: schedule, ascensos: boardings, descensos: alightings, fecha_hora_real: realDate, observaciones: notes })
      setStatus(result.message); setBoardings(0); setAlightings(0); setNotes(''); setRealDate(nowForInput())
    } catch (requestError) { setError(requestError.response?.data?.detail || 'No fue posible guardar el registro.') }
  }
  if (error && !options.length) return <div className="rounded-2xl bg-rose-50 p-6 text-rose-700">{error}</div>
  if (!options.length) return <div className="py-24 text-center font-semibold text-slate-500">Cargando formulario de captura…</div>
  return <form onSubmit={save} className="space-y-7 rounded-[2rem] bg-white p-5 shadow-sm ring-1 ring-slate-100 md:p-8"><header className="text-center"><h1 className="text-2xl font-extrabold text-indigo-700">Captura de Ruta</h1><p className="mt-1 text-sm text-slate-400">Selecciona las opciones y registra el movimiento de pasajeros.</p></header>
    <section><h2 className="mb-3 font-bold text-slate-600">1. Ruta asignada</h2><div className="grid gap-3 sm:grid-cols-2">{options.map((item) => <SelectCard key={item.id} active={routeId === item.id} onClick={() => chooseRoute(item.id)}><BusFront size={25} /><b className="mt-1">{item.nombre}</b></SelectCard>)}</div></section>
    <section><h2 className="mb-3 font-bold text-slate-600">2. Camión asignado</h2><div className="grid gap-3 sm:grid-cols-2">{route.unidades.map((item, index) => <SelectCard key={item} active={unit === item} tone="pink" onClick={() => setUnit(item)}><strong className="text-2xl">{index + 1}</strong><b className="mt-1">{item}</b></SelectCard>)}</div></section>
    <section><h2 className="mb-3 font-bold text-slate-600">3. Sentido</h2><div className="grid gap-3 sm:grid-cols-2"><SelectCard active={direction === 'ida'} onClick={() => chooseDirection('ida')}><ArrowRight size={25} /><b className="mt-1">IDA</b></SelectCard><SelectCard active={direction === 'regreso'} tone="orange" onClick={() => chooseDirection('regreso')}><ArrowLeft size={25} /><b className="mt-1">REGRESO</b></SelectCard></div></section>
    <section><h2 className="mb-3 font-bold text-slate-600">4. Paradero actual</h2><div className="grid max-h-72 gap-2 overflow-y-auto pr-2 sm:grid-cols-2">{stops.map((item) => <button type="button" key={item.nombre} onClick={() => selectStop(item.nombre)} className={`rounded-xl border px-4 py-3 text-sm font-medium ${stopName === item.nombre ? 'border-emerald-500 bg-emerald-50 text-emerald-800' : 'border-slate-200 text-slate-600 hover:border-slate-400'}`}>{item.nombre}</button>)}</div></section>
    <section><h2 className="mb-3 font-bold text-slate-600">5. Horario programado</h2><div className="grid gap-3 sm:grid-cols-3">{schedules.length ? schedules.map((item) => <button type="button" key={item} onClick={() => setSchedule(item)} className={`rounded-xl border px-4 py-3 font-bold ${schedule === item ? 'border-pink-500 bg-cyan-50 text-pink-600' : 'border-slate-200 text-slate-500'}`}>{item}</button>) : <p className="col-span-full rounded-xl bg-slate-50 p-4 text-sm text-slate-400">Selecciona un paradero para ver sus horarios.</p>}</div></section>
    <div className="border-t border-slate-200 pt-7"><div className="grid gap-5 md:grid-cols-2"><Counter label="Suben" value={boardings} setValue={setBoardings} tone="green" /><Counter label="Bajan" value={alightings} setValue={setAlightings} tone="orange" /></div></div>
    <section className="space-y-5"><label className="block text-sm font-bold text-slate-600">Fecha y hora real<input required type="datetime-local" value={realDate} onChange={(event) => setRealDate(event.target.value)} className="mt-2 w-full rounded-xl border border-slate-300 px-4 py-3 font-mono text-slate-700 outline-none focus:border-indigo-600" /></label><label className="block text-sm font-bold text-slate-600">¿Alguna observación?<textarea value={notes} maxLength="500" onChange={(event) => setNotes(event.target.value)} placeholder="Ej. Tráfico pesado en la entrada, lluvia intensa…" className="mt-2 min-h-24 w-full rounded-xl border border-slate-300 px-4 py-3 text-slate-700 outline-none focus:border-indigo-600" /></label></section>
    {error && <p className="rounded-xl bg-rose-50 p-4 text-sm font-medium text-rose-700">{error}</p>}{status && <p className="rounded-xl bg-emerald-50 p-4 text-sm font-medium text-emerald-700">{status}</p>}<button type="submit" className="flex w-full items-center justify-center gap-2 rounded-xl bg-indigo-700 px-5 py-4 font-bold text-white shadow-sm transition hover:bg-indigo-800"><Save size={19} /> GUARDAR REGISTRO</button>
  </form>
}

function Counter({ label, value, setValue, tone }) { const color = tone === 'green' ? 'border-emerald-100 bg-emerald-50 text-emerald-600' : 'border-orange-100 bg-orange-50 text-orange-600'; return <section className={`rounded-[1.5rem] border p-5 text-center ${color}`}><h2 className="text-sm font-bold">{label}</h2><div className="mt-3 flex items-center justify-center gap-5"><button type="button" onClick={() => setValue(Math.max(0, value - 1))} className="rounded-full bg-white p-2 shadow-sm" aria-label={`Reducir ${label}`}><Minus size={18} /></button><output className="min-w-14 text-3xl font-extrabold">{value}</output><button type="button" onClick={() => setValue(value + 1)} className="rounded-full bg-white p-2 shadow-sm" aria-label={`Aumentar ${label}`}><Plus size={18} /></button></div></section> }
