from unittest.mock import MagicMock, patch

import pytest

from src.opensky_connector import OpenSkyAPIConnector


class TestOpenSkyConnectorUnit:
    """Юнит-тесты для OpenSkyAPIConnector с моками."""

    @patch("src.opensky_connector.requests.Session")
    def test_get_country_bbox_success(self, mock_session_cls: MagicMock) -> None:
        """Успешное получение bbox."""
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {"boundingbox": ["40.0", "44.0", "-10.0", "5.0"]}
        ]
        mock_session_instance = MagicMock()
        mock_session_instance.get.return_value = mock_response
        mock_session_cls.return_value = mock_session_instance

        connector = OpenSkyAPIConnector()
        result = connector.get_country_bbox("Spain")

        assert result == {
            "min_lat": 40.0,
            "max_lat": 44.0,
            "min_lon": -10.0,
            "max_lon": 5.0,
        }

    @patch("src.opensky_connector.requests.Session")
    def test_get_country_bbox_not_found(self, mock_session_cls: MagicMock) -> None:
        """Страна не найдена — ValueError."""
        mock_response = MagicMock()
        mock_response.json.return_value = []
        mock_session_instance = MagicMock()
        mock_session_instance.get.return_value = mock_response
        mock_session_cls.return_value = mock_session_instance

        connector = OpenSkyAPIConnector()
        with pytest.raises(ValueError, match="не найдена"):
            connector.get_country_bbox("NonExistentCountry")

    @patch("src.opensky_connector.requests.Session")
    def test_get_aeroplanes_empty(self, mock_session_cls: MagicMock) -> None:
        """Пустой ответ от API."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"states": None}
        mock_session_instance = MagicMock()
        mock_session_instance.get.return_value = mock_response
        mock_session_cls.return_value = mock_session_instance

        connector = OpenSkyAPIConnector()
        result = connector.get_aeroplanes_in_bbox(0, 10, 0, 10)
        assert result == []

    @patch("src.opensky_connector.requests.Session")
    def test_get_aeroplanes_with_data(self, mock_session_cls: MagicMock) -> None:
        """Корректный парсинг данных о самолётах."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "columns": [
                "icao24",
                "callsign",
                "origin_country",
                "velocity",
                "baro_altitude",
            ],
            "states": [["abc123", "TEST1 ", " United States ", 200.0, 10000.0]],
        }
        mock_session_instance = MagicMock()
        mock_session_instance.get.return_value = mock_response
        mock_session_cls.return_value = mock_session_instance

        connector = OpenSkyAPIConnector()
        result = connector.get_aeroplanes_in_bbox(0, 10, 0, 10)

        assert len(result) == 1
        assert result[0]["callsign"] == "TEST1 "
        assert result[0]["origin_country"] == " United States "
