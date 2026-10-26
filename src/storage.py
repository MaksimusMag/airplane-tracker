from abc import ABC, abstractmethod
from typing import Any

from src.aeroplane import Aeroplane


class BaseStorage(ABC):
    """Абстрактный базовый класс для хранилищ данных о самолётах."""

    @abstractmethod
    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Добавить информацию о самолёте в хранилище.

        Args:
            aeroplane: Объект самолёта для сохранения.
        """
        pass

    @abstractmethod
    def get_aeroplanes(self, **criteria: Any) -> list[Aeroplane]:
        """Получить список самолётов по критериям.

        Args:
            **criteria: Критерии фильтрации (например, country='USA').

        Returns:
            Список объектов Aeroplane.
        """
        pass

    @abstractmethod
    def delete_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Удалить информацию о самолёте из хранилища.

        Args:
            aeroplane: Объект самолёта для удаления.
        """
        pass
