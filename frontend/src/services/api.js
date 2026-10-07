import axios from 'axios'

const runtimeApiUrl = window.__RUTAMAR_CONFIG__?.apiUrl
const api = axios.create({ baseURL: runtimeApiUrl || import.meta.env.VITE_API_URL || 'http://localhost:8000/api' })

export const getDashboard = (params) => api.get('/dashboard', { params }).then(({ data }) => {
  if (!data || typeof data !== 'object' || !data.summary) {
    throw new Error('La URL configurada no corresponde a la API de RUTAMAR.')
  }
  return data
})
export const getRouteMap = (params) => api.get('/map/routes', { params }).then(({ data }) => data)
export const getCaptureOptions = () => api.get('/capture/options').then(({ data }) => data)
export const saveCapture = (record) => api.post('/capture', record).then(({ data }) => data)
export const downloadCaptureExcel = () => api.get('/capture/export', { responseType: 'blob' }).then(({ data }) => {
  const url = URL.createObjectURL(data)
  const link = document.createElement('a')
  link.href = url
  link.download = 'RUTAMAR-Registros.xlsx'
  document.body.appendChild(link)
  link.click()
  link.remove()
  window.setTimeout(() => URL.revokeObjectURL(url), 1000)
})
