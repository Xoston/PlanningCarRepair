from vehicles import (
    add_vehicle,
    find_vehicles,
    sort_vehicles_by_mileage,
)
from maintenance import (
    is_service_due,
    get_service_status,
    create_maintenance_record,
    cancel_maintenance_record,
)
from storage import (
    load_vehicles,
    save_vehicles,
    load_maintenance,
    save_maintenance,
)
from utils import input_int, input_float, input_date

VEHICLES_FILE = "data/vehicles.json"
MAINTENANCE_FILE = "data/maintenance.json"


def show_vehicles_list(vehicles_list: list) -> None:
    """Вывести список автомобилей в консоль."""
    if not vehicles_list:
        print("Список автомобилей пуст.")
        return
    header = (
        f"\n{'ID':<4} | {'Марка и Модель':<20} | "
        f"{'Год':<6} | {'Пробег (км)':<10}"
    )
    print(header)
    print("-" * 50)
    for v in vehicles_list:
        title = f"{v['brand']} {v['model']}"
        print(
            f"{v['id']:<4} | {title:<20} | "
            f"{v['year']:<6} | {v['mileage']:<10}"
        )


def main() -> None:
    vehicles = load_vehicles(VEHICLES_FILE)
    records = load_maintenance(MAINTENANCE_FILE)

    while True:
        print("\n=== Система планирования ТО автомобиля ===")
        print("1. Показать все автомобили")
        print("2. Добавить автомобиль")
        print("3. Найти автомобиль по марке/модели")
        print("4. Проверить необходимость ТО")
        print("5. Запланировать/Добавить запись о ТО")
        print("6. Отменить запись о ТО")
        print("7. Показать все записи ТО")
        print("8. Сортировать автомобили по пробегу")
        print("0. Выход")

        choice = input("Выберите действие: ").strip()

        if choice == "1":
            show_vehicles_list(list(vehicles.values()))
        elif choice == "2":
            brand = input("Марка: ").strip()
            model = input("Модель: ").strip()
            year = input_int("Год выпуска: ")
            mileage = input_int("Текущий пробег (км): ")
            v_id = add_vehicle(vehicles, brand, model, year, mileage)
            save_vehicles(VEHICLES_FILE, vehicles)
            print(f"Автомобиль успешно добавлен под ID #{v_id}")
        elif choice == "3":
            q = input("Введите марку или модель для поиска: ")
            found = find_vehicles(vehicles, q)
            show_vehicles_list(found)
        elif choice == "4":
            v_id = input_int("Введите ID автомобиля: ")
            if v_id not in vehicles:
                print("Автомобиль с таким ID не найден.")
                continue
            last_s = input_int("Введите пробег на последнем ТО (км): ")
            due = is_service_due(vehicles[v_id]["mileage"], last_s)
            print(get_service_status(due))
        elif choice == "5":
            v_id = input_int("Введите ID автомобиля: ")
            if v_id not in vehicles:
                print("Автомобиль с таким ID не найден.")
                continue
            work = input("Наименование работы: ").strip()
            s_date = input_date("Дата выполнения (ДД.ММ.ГГГГ): ")
            cost = input_float("Стоимость (руб): ")
            rec = create_maintenance_record(
                records, v_id, work, s_date, cost
            )
            save_maintenance(MAINTENANCE_FILE, records)
            print(f"Запись о ТО #{rec['id']} добавлена.")
        elif choice == "6":
            r_id = input_int("Введите ID записи ТО для отмены: ")
            if cancel_maintenance_record(records, r_id):
                save_maintenance(MAINTENANCE_FILE, records)
                print("Запись о ТО успешно отменена.")
            else:
                print("Запись с таким ID не найдена.")
        elif choice == "7":
            if not records:
                print("Записи ТО отсутствуют.")
            else:
                for r in records:
                    print(
                        f"Запись #{r['id']} | Авто ID: {r['vehicle_id']} | "
                        f"Работа: {r['work_name']} | "
                        f"Дата: {r['service_date']} | "
                        f"Цена: {r['cost']} руб."
                    )
        elif choice == "8":
            sorted_v = sort_vehicles_by_mileage(vehicles)
            show_vehicles_list(sorted_v)
        elif choice == "0":
            print("Сохранение данных и завершение работы...")
            save_vehicles(VEHICLES_FILE, vehicles)
            save_maintenance(MAINTENANCE_FILE, records)
            break
        else:
            print("Неверный ввод. Попробуйте снова.")


if __name__ == "__main__":
    main()
