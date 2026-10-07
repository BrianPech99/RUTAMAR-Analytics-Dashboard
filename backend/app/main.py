from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware

from app.routes.health import router as health_router
from app.routes.analytics import router as analytics_router
from app.routes.map import router as map_router
from app.routes.capture import router as capture_router

app = FastAPI(title="RUTAMAR API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_origin_regex=r"https://.*\.up\.railway\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/api")
app.include_router(analytics_router, prefix="/api")
app.include_router(map_router, prefix="/api")
app.include_router(capture_router, prefix="/api")


@app.get("/", tags=["root"])
def root() -> dict[str, str]:
    return {
        "service": "RUTAMAR API",
        "status": "ok",
        "docs": "/docs",
        "health": "/api/health",
    }


@app.get("/favicon.ico", include_in_schema=False)
def favicon() -> Response:
    return Response(status_code=204)
