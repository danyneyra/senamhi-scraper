import settings
from src.models import Station
import json
from urllib.parse import urlencode
from typing import List, Optional

def load_stations(path: str) -> list[Station]:
    with open(path, 'r', encoding=settings.CSV_ENCODING) as file:
        data_json = json.load(file)
    return [Station(**item) for item in data_json]

stations = load_stations(settings.STATIONS_FILE)

def find_station_by_code(code: str) -> Optional[Station]:
    """Busca una estación por su código"""
    for est in stations:
        if est.code == code:
            return est
    return None

def get_headers_for_station(station: Station) -> List[str]:
    """Obtiene los headers CSV apropiados para una estación"""
    return station.get_csv_headers()

def create_station_url(station: Station) -> str:
    """Crea la URL para acceder a los datos de una estación"""
    url_base = settings.BASE_URL
    params = {
        "cod": station.code,
        "estado": station.status,
        "tipo_esta": station.station_type,
        "cate": station.category,
        "cod_old": station.legacy_code
    }
    return f"{url_base}?{urlencode(params)}"
