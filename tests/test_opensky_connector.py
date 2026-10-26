import pytest

from src.opensky_connector import OpenSkyAPIConnector


class TestOpenSkyAPIConnector:
    """Тесты для коннектора OpenSky API."""

    def test_connector_initialization(self) -> None:
        """Проверка успешной инициализации коннектора."""
        connector = OpenSkyAPIConnector()
        assert connector is not None
        assert hasattr(connector, "session")

    @pytest.mark.skip(reason="Интеграционный тест: требует сеть")
    def test_get_country_bbox_integration(self) -> None:
        """Интеграционный тест получения bbox (требует интернет)."""
        connector = OpenSkyAPIConnector()
        bbox = connector.get_country_bbox("Spain")
        assert "min_lat" in bbox
        assert "max_lat" in bbox
        assert "min_lon" in bbox
        assert "max_lon" in bbox

    @pytest.mark.skip(reason="Интеграционный тест: требует сеть")
    def test_get_aeroplanes_in_bbox_integration(self) -> None:
        """Интеграционный тест получения самолётов (требует интернет)."""
        connector = OpenSkyAPIConnector()
        planes = connector.get_aeroplanes_in_bbox(36.0, 44.0, -10.0, 5.0)
        assert isinstance(planes, list)
