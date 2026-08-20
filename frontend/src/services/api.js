import axios from 'axios'

const runtimeApiUrl = window.__RUTAMAR_CONFIG__?.apiUrl
const api = axios.create({ baseURL: runtimeApiUrl || import.meta.env.VITE_API_URL || 'http://localhost:8000/api' })

export const getDashboard = (params) => api.get('/dashboard', { params }).then(({ data }) => {
  if (!data || typeof data !== 'object' || !data.summary) {
    throw new Error('La URL configurada no corresponde a la API de RUTAMAR.')
  }
  return data
})
export const getRouteMap = () => api.get('/map/routes').then(({ data }) => data)
