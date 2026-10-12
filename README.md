# RUTAMAR Dashboard

Proyecto de titulación para analizar datos del sistema de transporte público gratuito RUTAMAR hacia las playas de Cancún.

## Tecnologías

- Frontend: React, Vite, JavaScript, Tailwind CSS, React Router, Recharts, Leaflet, React Leaflet, Axios y Lucide React.
- Backend: Python, FastAPI, Uvicorn, Pandas y NumPy.
- Datos: archivos CSV en `backend/data/`.

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

## Despliegue en Railway

El monorepo se despliega como dos servicios, ambos conectados al mismo repositorio de GitHub. Railway usará el Dockerfile que está en la raíz de cada servicio.

### 1. Crear el servicio de API

1. En Railway crea un proyecto y agrega un servicio desde el repositorio de GitHub.
2. En **Settings → Source → Root Directory** establece `/backend`.
3. Verifica que Railway detecte `Dockerfile` automáticamente.
4. En **Settings → Networking**, genera un dominio público.
5. En **Settings → Deploy**, establece el Healthcheck Path en `/api/health`.

Puedes nombrar el servicio `backend` para usar la referencia de variable de los siguientes pasos. No se requiere `.env`, contraseña de base de datos ni secreto para este backend.

### 2. Crear el servicio del dashboard

1. Agrega otro servicio desde el mismo repositorio.
2. En **Settings → Source → Root Directory** establece `/frontend`.
3. Verifica que Railway detecte el `frontend/Dockerfile` y genera un dominio público en **Settings → Networking**.
4. En **Variables**, agrega `VITE_API_URL` con esta referencia (si nombraste el servicio de API `backend`):

   ```text
   https://${{backend.RAILWAY_PUBLIC_DOMAIN}}/api
   ```

   Si usaste otro nombre, sustituye `backend` por el nombre exacto del servicio de API.

5. Despliega el dashboard. El contenedor usa el puerto `PORT` que Railway le asigna y sirve la configuración de API en tiempo de ejecución.

### 3. Comprobar

- Abre `https://<dominio-de-la-api>/api/health`; debe responder `{"status":"ok","service":"RUTAMAR API"}`.
- Abre el dominio público del dashboard desde el teléfono u otro dispositivo.
- La documentación de la API está en `https://<dominio-de-la-api>/docs`.

El CORS del backend acepta los dominios `*.up.railway.app`. Si usas un dominio personalizado para el frontend, agrega su origen completo (sin ruta final) a `CORS_ALLOW_ORIGINS` en las variables del servicio `backend`, por ejemplo `https://dashboard.ejemplo.com`.
