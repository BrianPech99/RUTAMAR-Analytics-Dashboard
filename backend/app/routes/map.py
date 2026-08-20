from copy import deepcopy

from fastapi import APIRouter, Query

from app.services.map_data import ROUTES, RUTA_1_SENTIDOS, RUTA_2_SENTIDOS
from app.services.rutamar_data import filter_data, filter_time

router = APIRouter(tags=["map"])


STOP_NAMES = {
    "Rancho Viejo": "Base Rancho Viejo",
    "Tres Reyes": "Base de 3 Reyes",
    "Paseo Kusamil": "Parada Paseos Kusamil",
    "Bodega Aurrera Tierra Maya": "Parada Bodega Aurrera Tierra Maya",
    "Playa Forum": "Base Forum",
}


def _with_stop_metrics(route_data: dict, data) -> dict:
    enriched = deepcopy(route_data)
    for direction, route in enriched.items():
        direction_rows = data[data["Sentido"].astype(str).str.casefold().eq(direction)]
        for stop in route["paradas"]:
            source_name = STOP_NAMES.get(stop["nombre"], f"Paradero {stop['nombre']}")
            rows = direction_rows[direction_rows["Paradero"].eq(source_name)]
            stop["ascensos"] = int(rows["Ascensos (Suben)"].sum())
            stop["descensos"] = int(rows["Descensos (Bajan)"].sum())
            stop["registros"] = int(len(rows))
    return enriched


@router.get("/map/routes")
def route_map(
    route: str | None = Query(None),
    period: str | None = Query(None),
    timeframe: str | None = Query(None),
    time_value: str | None = Query(None),
) -> dict:
    data = filter_time(filter_data(route, period), timeframe, time_value)
    return {
        "routes": ROUTES,
        "ruta_1_sentidos": _with_stop_metrics(RUTA_1_SENTIDOS, data),
        "ruta_2_sentidos": _with_stop_metrics(RUTA_2_SENTIDOS, data),
    }
