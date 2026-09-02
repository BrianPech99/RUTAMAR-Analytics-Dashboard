from fastapi import APIRouter, Query

from app.services.rutamar_data import (
    filter_data,
    filter_time,
    economic_savings,
    hourly_demand,
    occupancy,
    stop_summary,
    summary,
    transition,
    travel_times,
    trend,
    time_options,
    user_profiles,
)

router = APIRouter(tags=["analytics"])


@router.get("/dashboard")
def dashboard(
    route: str | None = Query(None),
    period: str | None = Query(None),
    timeframe: str | None = Query(None),
    time_value: str | None = Query(None),
) -> dict:
    base_data = filter_data(route, period)
    data = filter_time(base_data, timeframe, time_value)
    return {
        "summary": summary(data),
        "ahorro_economico": economic_savings(data),
        "tendencia": trend(data),
        "demanda_horaria": hourly_demand(data),
        "paraderos": stop_summary(data),
        "ocupacion": occupancy(data),
        "perfiles_usuario": user_profiles(data),
        "tiempos": travel_times(data),
        "transicion_ruta_1": transition(data),
        "opciones_tiempo": time_options(base_data, timeframe),
    }


@router.get("/filters")
def filters() -> dict:
    return {"rutas": ["Ruta 1 (Torito)", "Ruta 1 (Rancho Viejo)", "Ruta 2 (con Playa Caracol)"], "periodos": ["Torito", "Rancho Viejo"]}
