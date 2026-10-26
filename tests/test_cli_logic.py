
from src.aeroplane import Aeroplane


class TestSortingAndFiltering:
    """Тесты логики сортировки и фильтрации (из CLI)."""

    def test_sort_by_altitude_desc(self) -> None:
        """Сортировка по высоте DESC."""
        planes = [
            Aeroplane("A", "US", 100, 5000),
            Aeroplane("B", "US", 200, 15000),
            Aeroplane("C", "US", 150, 10000),
        ]
        sorted_planes = sorted(planes, key=lambda p: p.altitude, reverse=True)
        assert sorted_planes[0].callsign == "B"
        assert sorted_planes[1].callsign == "C"
        assert sorted_planes[2].callsign == "A"

    def test_filter_by_country(self) -> None:
        """Фильтрация по стране регистрации."""
        planes = [
            Aeroplane("A", "USA", 100, 5000),
            Aeroplane("B", "UK", 200, 15000),
            Aeroplane("C", "USA", 150, 10000),
        ]
        filtered = [p for p in planes if p.country == "USA"]
        assert len(filtered) == 2
        assert all(p.country == "USA" for p in filtered)

    def test_top_n_extraction(self) -> None:
        """Извлечение топ-N элементов."""
        planes = [Aeroplane(f"P{i}", "US", i * 10, i * 1000) for i in range(1, 6)]
        sorted_planes = sorted(planes, key=lambda p: p.altitude, reverse=True)
        top_3 = sorted_planes[:3]
        assert len(top_3) == 3
        assert top_3[0].altitude > top_3[1].altitude > top_3[2].altitude
