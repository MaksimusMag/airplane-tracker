
from typing import Any

import requests

from src.api_connector import BaseAPIConnector


class OpenSkyAPIConnector(BaseAPIConnector):
    """Конкретная реализация коннектора для OpenSky Network и Nominatim."""

    NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
    OPENSKY_URL = "https://opensky-network.org/api/states/all"

    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.headers.update(
            {"User-Agent": "AirplaneTrackerCourseProject/1.0 (capitanrb-107@yandex.ru)"}
        )

    def get_country_bbox(self, country_name: str) -> dict[str, float]:
        """Получить bounding box страны через Nominatim API."""
        params = {
            "q": country_name,
            "format": "json",
            "limit": 1,
        }
        response = self.session.get(self.NOMINATIM_URL, params=params)
        response.raise_for_status()
        data = response.json()

        if not data:
            raise ValueError(f"Страна '{country_name}' не найдена.")

        bbox = data[0]["boundingbox"]
        return {
            "min_lat": float(bbox[0]),
            "max_lat": float(bbox[1]),
            "min_lon": float(bbox[2]),
            "max_lon": float(bbox[3]),
        }

    def get_aeroplanes_in_bbox(
            self, min_lat: float, max_lat: float, min_lon: float, max_lon: float
    ) -> list[dict[str, Any]]:
        """Получить самолёты в bounding box через OpenSky API."""
        params = {
            "lamin": min_lat,
            "lamax": max_lat,
            "lomin": min_lon,
            "lomax": max_lon,
        }
        response = self.session.get(self.OPENSKY_URL, params=params)
        response.raise_for_status()
        json_data = response.json()

        if not json_data.get("states"):
            return []

        result = []
        # Индексы полей согласно документации OpenSky Network
        for state in json_data["states"]:
            aeroplane_dict = {
                "icao24": state[0],
                "callsign": state[1],
                "origin_country": state[2],
                "velocity": state[9] if len(state) > 9 else 0.0,
                "baro_altitude": state[7] if len(state) > 7 else 0.0,
            }
            result.append(aeroplane_dict)

        return result
