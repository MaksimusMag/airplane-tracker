from src.aeroplane import Aeroplane
from src.json_storage import JSONStorage
from src.opensky_connector import OpenSkyAPIConnector


def user_interaction() -> None:
    """Основная функция взаимодействия с пользователем через консоль."""
    connector = OpenSkyAPIConnector()
    storage = JSONStorage()

    print("=== Трекер самолётов ===")
    country = input("Введите название страны (на английском): ").strip()

    try:
        bbox = connector.get_country_bbox(country)
        planes_data = connector.get_aeroplanes_in_bbox(
            bbox["min_lat"], bbox["max_lat"], bbox["min_lon"], bbox["max_lon"]
        )

        # Сохранение в хранилище
        for data in planes_data:
            plane = Aeroplane.from_api_response(data)
            storage.add_aeroplane(plane)

        print(f"Получено {len(planes_data)} самолётов для '{country}'.")

        # Меню действий
        while True:
            print("\n1. Топ N по высоте\n2. Фильтр по стране регистрации\n3. Выход")
            choice = input("Выберите действие: ").strip()

            if choice == "1":
                n = int(input("Введите количество (N): "))
                all_planes = storage.get_aeroplanes()
                sorted_planes = sorted(all_planes, key=lambda p: p.altitude, reverse=True)
                top_n = sorted_planes[:n]
                for p in top_n:
                    print(
                        f"{p.callsign} | {p.country} | Alt: {p.altitude}m | "
                        f"Vel: {p.velocity}m/s"
                    )

            elif choice == "2":
                filter_country = input("Введите страну для фильтрации: ").strip()
                filtered = storage.get_aeroplanes(country=filter_country)
                for p in filtered:
                    print(f"{p.callsign} | Alt: {p.altitude}m | Vel: {p.velocity}m/s")

            elif choice == "3":
                print("Выход.")
                break
            else:
                print("Неверный выбор.")

    except Exception as e:
        print(f"Ошибка: {e}")
