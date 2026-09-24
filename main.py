from typing import List
from models import Vehicle, ServiceTask, MaintenanceRecord
from models.vehicles import add_vehicle, find_vehicle_by_id, show_vehicles
from models.tasks import add_task, show_tasks, find_task_by_id
from models.records import create_record, show_records
from storage import (
    load_vehicles,
    save_vehicles,
    load_tasks,
    save_tasks,
    load_records,
    save_records,
)
from utils import input_int

VEHICLES_FILE = "data/vehicles.json"
TASKS_FILE = "data/tasks.json"
RECORDS_FILE = "data/records.json"


def create_new_record_flow(
    records: List[MaintenanceRecord],
    vehicles: List[Vehicle],
    tasks: List[ServiceTask]
) -> None:
    if not vehicles or not tasks:
        print(
            "Ошибка: Для создания записи должны быть зарегистрированы "
            "авто и работы."
        )
        return

    show_vehicles(vehicles)
    v_id = input_int("Введите ID автомобиля: ")
    vehicle = find_vehicle_by_id(vehicles, v_id)
    if not vehicle:
        print("Автомобиль не найден!")
        return

    show_tasks(tasks)
    t_id = input_int("Введите ID работы: ")
    task = find_task_by_id(tasks, t_id)
    if not task:
        print("Работа не найдена!")
        return

    rec_id = len(records) + 1
    date_str = input("Введите планируемую дату (ГГГГ-ММ-ДД): ")
    target_mileage = vehicle.mileage + task.interval_km

    rec = create_record(
        records, rec_id, vehicle, task, date_str, target_mileage
    )
    print(f"\nЗапись успешно создана!\n{rec}")


def main() -> None:
    vehicles = load_vehicles(VEHICLES_FILE)
    tasks = load_tasks(TASKS_FILE)
    records = load_records(RECORDS_FILE, vehicles, tasks)

    while True:
        print("\n=== Система планирования ТО автомобиля ===")
        print("1. Показать список авто")
        print("2. Добавить авто")
        print("3. Показать виды ТО")
        print("4. Добавить вид ТО")
        print("5. Запланировать ТО")
        print("6. Показать все записи ТО")
        print("0. Выход")

        choice = input("Выберите действие: ")
        if choice == "1":
            show_vehicles(vehicles)
        elif choice == "2":
            v_id = len(vehicles) + 1
            make = input("Марка: ")
            model = input("Модель: ")
            year = input_int("Год выпуска: ")
            mileage = input_int("Текущий пробег: ")
            add_vehicle(vehicles, Vehicle(v_id, make, model, year, mileage))
            print("Автомобиль добавлен.")
        elif choice == "3":
            show_tasks(tasks)
        elif choice == "4":
            t_id = len(tasks) + 1
            title = input("Название работы: ")
            interval = input_int("Интервал (км): ")
            cost = float(input_int("Стоимость (руб): "))
            add_task(tasks, ServiceTask(t_id, title, interval, cost))
            print("Вид работы добавлен.")
        elif choice == "5":
            create_new_record_flow(records, vehicles, tasks)
        elif choice == "6":
            show_records(records)
        elif choice == "0":
            save_vehicles(VEHICLES_FILE, vehicles)
            save_tasks(TASKS_FILE, tasks)
            save_records(RECORDS_FILE, records)
            print("Данные сохранены. Выход из программы.")
            break


if __name__ == "__main__":
    main()
