import json
from pathlib import Path
from typing import Any

from src.aeroplane import Aeroplane
from src.storage import BaseStorage


class JSONStorage(BaseStorage):
    """Хранилище самолётов в JSON-файле."""

    def __init__(self, file_path: str = "aeroplanes.json") -> None:
        self._file_path = Path(file_path)
        self._data: list[dict[str, Any]] = self._load()

    def _load(self) -> list[dict[str, Any]]:
        """Загрузить данные из файла или вернуть пустой список."""
        if self._file_path.exists():
            with open(self._file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def _save(self) -> None:
        """Сохранить текущее состояние данных в файл."""
        with open(self._file_path, "w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=2, ensure_ascii=False)

    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Добавить самолёт в хранилище."""
        entry = {
            "callsign": aeroplane.callsign,
            "country": aeroplane.country,
            "velocity": aeroplane.velocity,
            "altitude": aeroplane.altitude,
        }
        # Проверка на дубликаты по callsign
        if not any(item["callsign"] == entry["callsign"] for item in self._data):
            self._data.append(entry)
            self._save()

    def get_aeroplanes(self, **criteria: Any) -> list[Aeroplane]:
        """Получить самолёты по критериям."""
        result = []
        for item in self._data:
            match = True
            for key, value in criteria.items():
                if item.get(key) != value:
                    match = False
                    break
            if match:
                result.append(Aeroplane(**item))
        return result

    def delete_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Удалить самолёт по callsign."""
        initial_len = len(self._data)
        self._data = [
            item for item in self._data if item["callsign"] != aeroplane.callsign
        ]
        if len(self._data) < initial_len:
            self._save()
