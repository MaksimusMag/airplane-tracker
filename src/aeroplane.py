from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Aeroplane:
    """Модель самолёта с инкапсуляцией и валидацией данных."""

    callsign: str
    country: str
    velocity: float
    altitude: float
    _icao24: str = field(default="", repr=False)
    _origin_country: str = field(default="", repr=False)

    def __post_init__(self) -> None:
        """Валидация атрибутов при создании экземпляра."""
        if not isinstance(self.callsign, str) or not self.callsign.strip():
            raise ValueError("Callsign должен быть непустой строкой.")
        if not isinstance(self.country, str) or not self.country.strip():
            raise ValueError("Country должен быть непустой строкой.")
        if not isinstance(self.velocity, (int, float)) or self.velocity < 0:
            raise ValueError("Velocity должна быть неотрицательным числом.")
        if not isinstance(self.altitude, (int, float)):
            raise ValueError("Altitude должна быть числом.")

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> Aeroplane:
        """Фабричный метод для создания объекта из ответа API OpenSky.

        Args:
            data: Словарь с данными самолёта из API.

        Returns:
            Экземпляр Aeroplane.
        """
        # Безопасное получение значений: если None или отсутствует — берём дефолт
        raw_callsign = data.get("callsign")
        raw_country = data.get("origin_country")
        raw_velocity = data.get("velocity")
        raw_altitude = data.get("baro_altitude")

        return cls(
            callsign=(raw_callsign or "UNKNOWN").strip(),
            country=(raw_country or "Unknown").strip(),
            velocity=float(raw_velocity or 0.0),
            altitude=float(raw_altitude or 0.0),
            _icao24=data.get("icao24", ""),
            _origin_country=raw_country or "",
        )

    def __lt__(self, other: Aeroplane) -> bool:
        """Сравнение по высоте (для сортировки)."""
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self.altitude < other.altitude

    def __gt__(self, other: Aeroplane) -> bool:
        """Сравнение по высоте (единый критерий с __lt__)."""
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self.altitude > other.altitude

    def __eq__(self, other: object) -> bool:
        """Равенство по высоте (единый критерий с < и >)."""
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self.altitude == other.altitude
