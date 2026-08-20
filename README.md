# RUTAMAR Dashboard

Base del proyecto de titulación para analizar datos del sistema de transporte público gratuito RUTAMAR hacia las playas de Cancún. Esta primera etapa prepara la arquitectura, navegación y API; aún no incluye datos, métricas, gráficas ni análisis.

## Tecnologías

- Frontend: React, Vite, JavaScript, Tailwind CSS, React Router, Recharts, Leaflet, React Leaflet, Axios y Lucide React.
- Backend: Python, FastAPI, Uvicorn, Pandas y NumPy.
- Datos iniciales: archivos CSV en `backend/data/` (no se incluyen datos de ejemplo).

## Estructura

```text
frontend/                 Aplicación React/Vite
  src/components/         Componentes reutilizables
  src/pages/              Vistas, por ahora placeholders
  src/layouts/            Layout principal y navegación
  src/services/           Cliente/API futuro
  src/hooks/              Hooks futuros
  src/utils/              Utilidades futuras
backend/
  app/routes/             Endpoints FastAPI
  app/services/           Lectura y transformación futura de CSV
  app/utils/              Utilidades futuras
  data/                   CSV reales futuros
  .venv/                  Entorno virtual local (ignorado por Git)
```

## Instalación

### Frontend

```powershell
cd frontend
npm install
```

### Backend

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Si el entorno virtual aún no existe, créalo desde la raíz con un Python 3.12 o posterior:

```powershell
python -m venv backend\.venv
```

## Ejecución local

En una terminal, inicia el backend desde `backend/`:

```powershell
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --port 8000
```

En otra, inicia el frontend desde `frontend/`:

```powershell
npm run dev
```

- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- Estado de la API: http://localhost:8000/api/health
- Documentación interactiva: http://localhost:8000/docs

`GET /api/health` responde:

```json
{"status":"ok","service":"RUTAMAR API"}
```

## Variables de entorno

Se incluyen `frontend/.env.example` y `backend/.env.example` como plantilla. Copia cada uno a `.env` cuando haga falta configurar valores locales; esos archivos se ignoran en Git.

## Despliegue en Railway

El repositorio está preparado para dos servicios Railway desde el mismo repositorio privado:

1. **API**: establece `backend` como *Root Directory*. Railway detectará `backend/Dockerfile`. Genera un dominio público y usa `/api/health` como Healthcheck Path.
2. **Frontend**: establece `frontend` como *Root Directory*. Railway detectará `frontend/Dockerfile`. En sus variables de compilación configura `VITE_API_URL` con la URL del servicio API seguida de `/api`, por ejemplo `https://rutamar-api.up.railway.app/api`.

El CSV se copia dentro de la imagen del backend. Al ser un repositorio privado, Railway puede acceder al archivo durante el despliegue.
