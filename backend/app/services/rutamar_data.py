import csv
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd

DATA_FILE = Path(__file__).resolve().parents[2] / "data" / "Reporte-RutaMar.csv"
FARE_REFERENCE_MXN = 12
MONTH_NAMES_ES = ("enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre")
ROUTE_MAP = {
    "Ruta 1": "Ruta 1",
    "Ruta 1 (Rancho Viejo)": "Ruta 1",
    "Ruta 2": "Ruta 2",
    "Ruta 2 (con Playa Caracol)": "Ruta 2",
}
HOTEL_ZONE = {"Paradero Playa Las Perlas", "Paradero Playa Langosta", "Paradero Playa Tortugas", "Paradero Forum", "Base Forum"}
NEW_STOPS = {
    "Base Rancho Viejo",
    "Paradero Chedraui Rancho Viejo",
    "Paradero Oxxo Rancho Nuevo",
    "Paradero Bodega Aurrera Corales",
    "Paradero Pizza Casa Jaguar",
}


def _read_passengers() -> pd.DataFrame:
    with DATA_FILE.open(encoding="utf-8-sig", newline="") as file:
        rows = list(csv.reader(file))
    marker = next(i for i, row in enumerate(rows) if row and row[0].startswith("--- DESGLOSE"))
    headers = rows[marker + 1]
    records, trip_number = [], 0
    for row in rows[marker + 2:]:
        if not any(cell.strip() for cell in row):
            trip_number += 1
            continue
        if len(row) < len(headers):
            row += [""] * (len(headers) - len(row))
        record = dict(zip(headers, row))
        record["trip_sequence"] = trip_number
        records.append(record)
    frame = pd.DataFrame(records)
    # El reporte actual usa ISO (AAAA-MM-DD), mientras que ediciones anteriores
    # pueden usar DD/MM/AAAA. Pandas interpreta ambos formatos sin perder
    # compatibilidad con el histórico.
    frame["Fecha"] = pd.to_datetime(frame["Fecha"], format="mixed", dayfirst=True, errors="coerce")
    for column in ["Ascensos (Suben)", "Descensos (Bajan)"]:
        frame[column] = pd.to_numeric(frame[column], errors="coerce").fillna(0).astype(int)
    for source, target in [("Hora Programada", "programada"), ("Hora Real de Llegada", "real")]:
        time = pd.to_timedelta(frame[source] + ":00", errors="coerce")
        frame[target] = frame["Fecha"] + time
    frame["ruta_original"] = frame["Ruta"].str.strip()
    frame["ruta_principal"] = frame["ruta_original"].map(ROUTE_MAP).fillna(frame["ruta_original"])
    frame["periodo_ruta_1"] = np.select(
        [frame["ruta_original"].eq("Ruta 1"), frame["ruta_original"].eq("Ruta 1 (Rancho Viejo)")],
        ["Torito", "Rancho Viejo"], default="",
    )
    frame["trip_id"] = (frame["Fecha"].dt.strftime("%Y%m%d") + "-" + frame["Ruta"] + "-" + frame["Unidad"] + "-" + frame["Sentido"] + "-" + frame["trip_sequence"].astype(str))
    frame["minutos_desviacion"] = (frame["real"] - frame["programada"]).dt.total_seconds() / 60
    frame.loc[frame["minutos_desviacion"].abs() > 180, "minutos_desviacion"] = np.nan
    frame["hora"] = frame["real"].dt.hour
    return frame


@lru_cache(maxsize=1)
def passengers() -> pd.DataFrame:
    return _read_passengers()


def filter_data(route: str | None = None, period: str | None = None) -> pd.DataFrame:
    data = passengers().copy()
    if route and route != "Todas":
        data = data[data["ruta_principal"] == route]
    if period and period != "Todos":
        data = data[data["periodo_ruta_1"] == period]
    return data


def time_options(data: pd.DataFrame, timeframe: str | None) -> list[dict]:
    if not timeframe or timeframe == "Todos":
        return []
    if timeframe == "Semana":
        weeks = data["Fecha"].dt.to_period("W-SUN")
        return [
            {"value": str(period.start_time.date()), "label": f"Semana del {period.start_time.strftime('%d %b %Y')}"}
            for period in sorted(weeks.dropna().unique(), reverse=True)
        ]
    if timeframe == "Mes":
        months = data["Fecha"].dt.to_period("M")
        return [
            {"value": str(period), "label": f"{MONTH_NAMES_ES[period.start_time.month - 1].capitalize()} {period.start_time.year}"}
            for period in sorted(months.dropna().unique(), reverse=True)
        ]
    if timeframe == "Edición":
        editions = data["Edicion"].dropna().astype(str).str.strip()
        return [{"value": edition, "label": edition} for edition in sorted(editions[editions.ne("")].unique(), reverse=True)]
    return []


def filter_time(data: pd.DataFrame, timeframe: str | None = None, time_value: str | None = None) -> pd.DataFrame:
    if not timeframe or timeframe == "Todos" or not time_value:
        return data
    if timeframe == "Semana":
        week_start = pd.to_datetime(time_value, errors="coerce")
        if pd.isna(week_start):
            return data.iloc[0:0]
        return data[data["Fecha"].dt.to_period("W-SUN").eq(week_start.to_period("W-SUN"))]
    if timeframe == "Mes":
        return data[data["Fecha"].dt.to_period("M").astype(str).eq(time_value)]
    if timeframe == "Edición":
        return data[data["Edicion"].astype(str).str.strip().eq(time_value)]
    return data


def summary(data: pd.DataFrame) -> dict:
    active_days = max(data["Fecha"].nunique(), 1)
    total_boardings = int(data["Ascensos (Suben)"].sum())
    on_time = data["minutos_desviacion"].dropna().abs().le(5)
    return {
        "ascensos_totales": total_boardings,
        "tarifa_referencia": FARE_REFERENCE_MXN,
        "ahorro_estimado": total_boardings * FARE_REFERENCE_MXN,
        "promedio_diario": round(total_boardings / active_days, 1),
        "dias_operados": int(data["Fecha"].nunique()),
        "corridas": int(data["trip_id"].nunique()),
        "puntualidad": round(float(on_time.mean() * 100), 1) if not on_time.empty else 0,
        "desviacion_promedio": round(float(data["minutos_desviacion"].mean()), 1) if data["minutos_desviacion"].notna().any() else 0,
        # Indicador observable con los registros disponibles: corridas que
        # efectivamente transportaron al menos un pasajero.
        "usabilidad_ruta": round(float(data.groupby("trip_id")["Ascensos (Suben)"].sum().gt(0).mean() * 100), 1) if not data.empty else 0,
        "deficiencia_horarios": round(float((~on_time).mean() * 100), 1) if not on_time.empty else 0,
    }


def economic_savings(data: pd.DataFrame) -> list[dict]:
    result = data.groupby("ruta_original", as_index=False)["Ascensos (Suben)"].sum()
    result["ahorro_estimado"] = result["Ascensos (Suben)"] * FARE_REFERENCE_MXN
    return result.rename(columns={"ruta_original": "ruta", "Ascensos (Suben)": "ascensos"}).sort_values("ahorro_estimado", ascending=False).to_dict("records")


def trend(data: pd.DataFrame) -> list[dict]:
    result = data.groupby("Fecha", as_index=False)["Ascensos (Suben)"].sum()
    return [{"fecha": row.Fecha.strftime("%d %b"), "ascensos": int(row._2)} for row in result.itertuples()]


def hourly_demand(data: pd.DataFrame) -> list[dict]:
    result = data.dropna(subset=["hora"]).groupby("hora", as_index=False)["Ascensos (Suben)"].sum()
    return [{"hora": f"{int(row.hora):02d}:00", "ascensos": int(row._2)} for row in result.itertuples()]


def stop_summary(data: pd.DataFrame) -> list[dict]:
    result = data.groupby("Paradero", as_index=False).agg(ascensos=("Ascensos (Suben)", "sum"), descensos=("Descensos (Bajan)", "sum"))
    result["tipo"] = np.where(result.ascensos >= result.descensos, "Generador", "Atraíble")
    result["total"] = result.ascensos + result.descensos
    return result.sort_values("total", ascending=False).head(12).rename(columns={"Paradero": "paradero"}).to_dict("records")


def occupancy(data: pd.DataFrame) -> list[dict]:
    ordered = data.sort_values(["trip_id", "real", "programada"]).copy()
    change = ordered["Ascensos (Suben)"] - ordered["Descensos (Bajan)"]
    ordered["ocupacion"] = change.groupby(ordered["trip_id"]).cumsum()
    # La ocupación se calcula para toda la corrida y después se reporta sólo en
    # paraderos urbanos. Así se conserva la carga real al regresar de la playa.
    urban_stops = ~ordered["Paradero"].str.contains("playa", case=False, na=False)
    urban_stops &= ~ordered["Paradero"].isin(HOTEL_ZONE)
    result = ordered.loc[urban_stops].groupby("Paradero", as_index=False)["ocupacion"].max()
    result = result.sort_values("ocupacion", ascending=False).head(10)
    return result.rename(columns={"Paradero": "paradero"}).to_dict("records")


def user_profiles(data: pd.DataFrame) -> list[dict]:
    profiles = [
        ("Mañana", "Traslado laboral y escolar", 5, 9),
        ("Mediodía", "Trámites y servicios", 10, 15),
        ("Tarde", "Regreso laboral y escolar", 16, 20),
        ("Noche / madrugada", "Otros desplazamientos", 21, 4),
    ]
    total = max(int(data["Ascensos (Suben)"].sum()), 1)
    result = []
    for horario, perfil, start, end in profiles:
        if start <= end:
            rows = data[data["hora"].between(start, end)]
        else:
            rows = data[(data["hora"] >= start) | (data["hora"] <= end)]
        boardings = int(rows["Ascensos (Suben)"].sum())
        result.append({"horario": horario, "perfil": perfil, "ascensos": boardings, "porcentaje": round(boardings / total * 100, 1)})
    return result


def travel_times(data: pd.DataFrame) -> list[dict]:
    trips = data.dropna(subset=["real"]).groupby("trip_id").agg(ruta=("ruta_principal", "first"), inicio=("real", "min"), fin=("real", "max"))
    trips["minutos"] = (trips.fin - trips.inicio).dt.total_seconds() / 60
    trips = trips[trips.minutos.between(1, 240)]
    result = trips.groupby("ruta", as_index=False).minutos.agg(["mean", "median", "min", "max"]).reset_index()
    return [{"ruta": row.ruta, "promedio": round(row.mean, 1), "mediana": round(row.median, 1), "minimo": round(row.min, 1), "maximo": round(row.max, 1)} for row in result.itertuples()]


def transition(data: pd.DataFrame) -> dict:
    route_one = data[data["ruta_principal"] == "Ruta 1"].copy()
    route_one = route_one[route_one["periodo_ruta_1"].isin(["Torito", "Rancho Viejo"])]
    grouped = route_one.groupby("periodo_ruta_1")
    periods = []
    for period, group in grouped:
        days = max(group["Fecha"].nunique(), 1)
        on_time = group["minutos_desviacion"].dropna().abs().le(5)
        periods.append({
            "periodo": period,
            "ruta_historica": "Ruta 1" if period == "Torito" else "Ruta 1 (Rancho Viejo)",
            "ascensos": int(group["Ascensos (Suben)"].sum()),
            "dias": int(group["Fecha"].nunique()),
            "corridas": int(group["trip_id"].nunique()),
            "promedio_diario": round(group["Ascensos (Suben)"].sum() / days, 1),
            "pasajeros_por_corrida": round(group["Ascensos (Suben)"].sum() / max(group["trip_id"].nunique(), 1), 1),
            "puntualidad": round(float(on_time.mean() * 100), 1) if not on_time.empty else 0,
            "desviacion_promedio": round(float(group["minutos_desviacion"].mean()), 1),
        })
    periods.sort(key=lambda item: item["periodo"] != "Torito")
    period_lookup = {item["periodo"]: item for item in periods}
    base = period_lookup.get("Torito", {}).get("promedio_diario", 0)
    current = period_lookup.get("Rancho Viejo", {}).get("promedio_diario", 0)
    variation = round(((current - base) / base) * 100, 1) if base else 0

    daily = route_one.pivot_table(index="Fecha", columns="periodo_ruta_1", values="Ascensos (Suben)", aggfunc="sum", fill_value=0).reset_index()
    daily["fecha"] = daily["Fecha"].dt.strftime("%d %b")

    hotel_trips = route_one[(route_one["Sentido"] == "Ida") & route_one["Paradero"].isin(HOTEL_ZONE)].dropna(subset=["real"])
    hotel = hotel_trips.groupby("periodo_ruta_1", as_index=False).agg(
        desviacion_minutos=("minutos_desviacion", "mean"),
        llegadas=("real", "count"),
    )
    hotel["desviacion_minutos"] = hotel["desviacion_minutos"].round(1)

    new_demand = route_one[(route_one["periodo_ruta_1"] == "Rancho Viejo") & route_one["Paradero"].isin(NEW_STOPS)].groupby("Paradero", as_index=False).agg(ascensos=("Ascensos (Suben)", "sum"), dias=("Fecha", "nunique"))
    new_demand["promedio_diario"] = (new_demand["ascensos"] / new_demand["dias"].clip(lower=1)).round(1)
    new_demand = new_demand.rename(columns={"Paradero": "paradero"}).sort_values("ascensos", ascending=False).to_dict("records")
    return {
        "periodos": periods,
        "variacion_demanda_pct": variation,
        "demanda_diaria": daily.to_dict("records"),
        "nuevos_paraderos": new_demand,
        "puntualidad_zona_hotelera": hotel.to_dict("records"),
    }
