from pathlib import Path

import pytest

from src.aeroplane import Aeroplane
from src.json_storage import JSONStorage


class TestJSONStorage:
    """Тесты для JSON-хранилища."""

    @pytest.fixture(autouse=True)
    def setup(self, tmp_path: Path) -> None:
        """Использование временной папки для каждого теста."""
        self.storage = JSONStorage(str(tmp_path / "test_planes.json"))

    def test_add_and_get(self) -> None:
        """Добавление и получение самолёта."""
        plane = Aeroplane("TEST1", "USA", 100.0, 5000.0)
        self.storage.add_aeroplane(plane)
        result = self.storage.get_aeroplanes()
        assert len(result) == 1
        assert result[0].callsign == "TEST1"

    def test_delete(self) -> None:
        """Удаление самолёта."""
        plane = Aeroplane("TEST2", "UK", 200.0, 6000.0)
        self.storage.add_aeroplane(plane)
        self.storage.delete_aeroplane(plane)
        result = self.storage.get_aeroplanes()
        assert len(result) == 0

    def test_filter_by_substring_case_insensitive(self) -> None:
        """Фильтрация по подстроке без учета регистра."""
        p1 = Aeroplane("A", "United States", 100, 1000)
        p2 = Aeroplane("B", "UK", 200, 2000)
        p3 = Aeroplane("C", "UNITED KINGDOM", 150, 1500)
        self.storage.add_aeroplane(p1)
        self.storage.add_aeroplane(p2)
        self.storage.add_aeroplane(p3)

        # Поиск "united" должен найти "United States" и "UNITED KINGDOM"
        results = self.storage.get_aeroplanes(country="united")
        assert len(results) == 2
        callsigns = {p.callsign for p in results}
        assert callsigns == {"A", "C"}

    def test_duplicate_prevention(self) -> None:
        """Запрет дубликатов по callsign."""
        plane = Aeroplane("DUP", "USA", 100, 1000)
        self.storage.add_aeroplane(plane)
        self.storage.add_aeroplane(plane)
        result = self.storage.get_aeroplanes()
        assert len(result) == 1
