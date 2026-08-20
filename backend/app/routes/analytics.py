from fastapi import APIRouter, Query

from app.services.rutamar_data import (
    filter_data,
    economic_savings,
    hourly_demand,
    occupancy,
    stop_summary,
    summary,
    transition,
    travel_times,
    trend,
)

router = APIRouter(tags=["analytics"])


@router.get("/dashboard")
def dashboard(route: str | None = Query(None), period: str | None = Query(None)) -> dict:
    data = filter_data(route, period)
    return {
        "summary": summary(data),
        "ahorro_economico": economic_savings(data),
        "tendencia": trend(data),
        "demanda_horaria": hourly_demand(data),
        "paraderos": stop_summary(data),
        "ocupacion": occupancy(data),
        "tiempos": travel_times(data),
        "transicion_ruta_1": transition(data),
    }


@router.get("/filters")
def filters() -> dict:
    return {"rutas": ["Ruta 1", "Ruta 2"], "periodos": ["Torito", "Rancho Viejo"]}
