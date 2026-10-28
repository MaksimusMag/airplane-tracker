import pytest
from src.aeroplane import Aeroplane


class TestAeroplane:
    """Тесты для модели Aeroplane."""

    def test_valid_creation(self) -> None:
        """Успешное создание валидного объекта."""
        plane = Aeroplane("UAL1621", "United States", 268.79, 10203.18)
        assert plane.callsign == "UAL1621"
        assert plane.country == "United States"
        assert plane.velocity == 268.79
        assert plane.altitude == 10203.18

    def test_invalid_callsign_raises(self) -> None:
        """Пустой callsign вызывает ошибку."""
        with pytest.raises(ValueError, match="Callsign"):
            Aeroplane("", "USA", 0.0, 0.0)

    def test_invalid_velocity_raises(self) -> None:
        """Отрицательная скорость вызывает ошибку."""
        with pytest.raises(ValueError, match="Velocity"):
            Aeroplane("TEST", "USA", -10.0, 0.0)

    def test_from_api_response(self) -> None:
        """Фабричный метод корректно мапит данные API."""
        api_data = {
            "callsign": "BAW123 ",
            "origin_country": " United Kingdom ",
            "velocity": 500.0,
            "baro_altitude": 11000.0,
            "icao24": "abc123",
        }
        plane = Aeroplane.from_api_response(api_data)
        assert plane.callsign == "BAW123"
        assert plane.country == "United Kingdom"
        assert plane._icao24 == "abc123"

    def test_from_api_response_with_none_values(self) -> None:
        """Фабричный метод корректно обрабатывает None значения."""
        api_data = {
            "callsign": None,
            "origin_country": None,
            "velocity": None,
            "baro_altitude": None,
        }
        plane = Aeroplane.from_api_response(api_data)
        assert plane.callsign == "UNKNOWN"
        assert plane.country == "Unknown"
        assert plane.velocity == 0.0
        assert plane.altitude == 0.0

    def test_comparison_by_altitude(self) -> None:
        """Сравнение по высоте через < работает корректно."""
        p1 = Aeroplane("A", "US", 100, 5000)
        p2 = Aeroplane("B", "US", 100, 10000)
        assert p1 < p2

    def test_comparison_by_altitude_gt(self) -> None:
        """Сравнение по высоте через > работает корректно."""
        p1 = Aeroplane("A", "US", 100, 10000)
        p2 = Aeroplane("B", "US", 100, 5000)
        assert p1 > p2

    def test_equality_by_callsign(self) -> None:
        """Равенство определяется по callsign."""
        p1 = Aeroplane("TEST", "US", 100, 100)
        p2 = Aeroplane("TEST", "UK", 200, 200)
        assert p1 == p2
