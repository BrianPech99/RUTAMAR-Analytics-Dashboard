from fastapi import APIRouter

from app.services.map_data import ROUTES, RUTA_1_SENTIDOS, RUTA_2_SENTIDOS

router = APIRouter(tags=["map"])


@router.get("/map/routes")
def route_map() -> dict:
    return {"routes": ROUTES, "ruta_1_sentidos": RUTA_1_SENTIDOS, "ruta_2_sentidos": RUTA_2_SENTIDOS}
