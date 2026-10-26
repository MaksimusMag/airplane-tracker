from abc import ABC, abstractmethod
from typing import Any


class BaseAPIConnector(ABC):
    """Абстрактный базовый класс для коннекторов к внешним API."""

    @abstractmethod
    def get_country_bbox(self, country_name: str) -> dict[str, float]:
        """Получить bounding box страны по её названию.

        Args:
            country_name: Название страны на английском языке.

        Returns:
            Словарь с ключами 'min_lat', 'max_lat', 'min_lon', 'max_lon'.
        """
        pass

    @abstractmethod
    def get_aeroplanes_in_bbox(
        self, min_lat: float, max_lat: float, min_lon: float, max_lon: float
    ) -> list[dict[str, Any]]:
        """Получить список самолётов в заданном bounding box.

        Args:
            min_lat: Минимальная широта.
            max_lat: Максимальная широта.
            min_lon: Минимальная долгота.
            max_lon: Максимальная долгота.

        Returns:
            Список словарей с данными о самолётах.
        """
        pass
