from typing import List
from models import User, Vehicle, Indicator, ServiceDate
from models.users import find_user_by_id, show_users
from models.vehicles import find_vehicle_by_id, show_vehicles
from models.indicators import find_indicator_by_id, show_indicators
from models.dates import show_dates
from storage import (
    load_users, save_users,
    load_vehicles, save_vehicles,
    load_indicators, save_indicators,
    load_dates, save_dates
)
from utils import input_int

USERS_FILE = "data/users.json"
VEHICLES_FILE = "data/vehicles.json"
INDICATORS_FILE = "data/indicators.json"
DATES_FILE = "data/dates.json"


def add_user_flow(users: List[User]) -> None:
    u_id = len(users) + 1
    name = input("Имя пользователя: ")
    phone = input("Телефон: ")
    users.append(User(u_id, name, phone))
    print("Пользователь добавлен.")


def add_vehicle_flow(vehicles: List[Vehicle], users: List[User]) -> None:
    if not users:
        print("Сначала добавьте хотя бы одного пользователя!")
        return
    show_users(users)
    u_id = input_int("Введите ID владельца: ")
    owner = find_user_by_id(users, u_id)
    if not owner:
        print("Пользователь не найден!")
        return

    v_id = len(vehicles) + 1
    make = input("Марка: ")
    model = input("Модель: ")
    year = input_int("Год выпуска: ")
    mileage = input_int("Пробег (км): ")
    vehicles.append(Vehicle(v_id, make, model, year, mileage, owner))
    print("Автомобиль добавлен.")


def add_indicator_flow(indicators: List[Indicator]) -> None:
    i_id = len(indicators) + 1
    title = input("Название показателя: ")
    target = input_int("Целевой пробег/норма (км): ")
    cost = float(input_int("Стоимость (руб): "))
    indicators.append(Indicator(i_id, title, target, cost))
    print("Показатель добавлен.")


def add_date_flow(
    dates: List[ServiceDate],
    vehicles: List[Vehicle],
    indicators: List[Indicator]
) -> None:
    if not vehicles or not indicators:
        print("Для назначения даты требуются добавленные авто и показатели!")
        return
    show_vehicles(vehicles)
    v_id = input_int("Введите ID авто: ")
    vehicle = find_vehicle_by_id(vehicles, v_id)
    if not vehicle:
        print("Автомобиль не найден!")
        return

    show_indicators(indicators)
    ind_id = input_int("Введите ID показателя: ")
    indicator = find_indicator_by_id(indicators, ind_id)
    if not indicator:
        print("Показатель не найден!")
        return

    d_id = len(dates) + 1
    date_str = input("Введите плановую дату (ГГГГ-ММ-ДД): ")
    dates.append(ServiceDate(d_id, vehicle, indicator, date_str))
    print("Дата обслуживания успешно запланирована.")


def main() -> None:
    users = load_users(USERS_FILE)
    vehicles = load_vehicles(VEHICLES_FILE, users)
    indicators = load_indicators(INDICATORS_FILE)
    dates = load_dates(DATES_FILE, vehicles, indicators)

    while True:
        print("\n=== Управление ТО (Пользователь, Авто, Показатель, Дата) ===")
        print("1. Показать пользователей")
        print("2. Добавить пользователя")
        print("3. Показать автомобили")
        print("4. Добавить автомобиль")
        print("5. Показать показатели")
        print("6. Добавить показатель")
        print("7. Показать запланированные даты ТО")
        print("8. Назначить дату ТО")
        print("0. Выход")

        choice = input("Выберите действие: ")
        if choice == "1":
            show_users(users)
        elif choice == "2":
            add_user_flow(users)
        elif choice == "3":
            show_vehicles(vehicles)
        elif choice == "4":
            add_vehicle_flow(vehicles, users)
        elif choice == "5":
            show_indicators(indicators)
        elif choice == "6":
            add_indicator_flow(indicators)
        elif choice == "7":
            show_dates(dates)
        elif choice == "8":
            add_date_flow(dates, vehicles, indicators)
        elif choice == "0":
            save_users(USERS_FILE, users)
            save_vehicles(VEHICLES_FILE, vehicles)
            save_indicators(INDICATORS_FILE, indicators)
            save_dates(DATES_FILE, dates)
            print("Данные сохранены. Выход.")
            break


if __name__ == "__main__":
    main()
