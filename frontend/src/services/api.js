import axios from 'axios'

const api = axios.create({ baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api' })
export const getDashboard = (params) => api.get('/dashboard', { params }).then(({ data }) => data)
export const getRouteMap = () => api.get('/map/routes').then(({ data }) => data)
