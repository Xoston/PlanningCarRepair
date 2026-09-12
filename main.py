from datetime import date

# 1. Входные данные (простые типы)
car_brand: str = "Toyota"
car_model: str = "Camry"
current_mileage: int = 60000
target_mileage: int = 65000

current_date: date = date(2026, 9, 12)
target_date: date = date(2026, 10, 1)


# 2. Функция 1: Расчет оставшегося пробега
def calculate_remaining_mileage(current_km: int, target_km: int) -> int:
    """Вычисляет оставшийся пробег до обслуживания."""
    remaining_km: int = target_km - current_km
    return remaining_km


# 3. Функция 2: Проверка необходимости ТО
def check_maintenance_status(
    current_km: int, target_km: int, now_date: date, due_date: date
) -> str:
    """Проверяет превышение лимитов по пробегу или дате."""
    is_mileage_exceeded: bool = current_km >= target_km
    is_date_exceeded: bool = now_date >= due_date

    if is_mileage_exceeded or is_date_exceeded:
        return "ВНИМАНИЕ: Требуется срочное техническое обслуживание!"
    else:
        return "Обслуживание не требуется. Автомобиль в норме."


# 4. Функция 3: Формирование отчета
def format_car_report(brand: str, model: str, mileage: int, status: str) -> str:
    """Формирует текстовый отчет о состоянии ТС."""
    report: str = (
        f"=== Отчет о состоянии ТС ===\n"
        f"Автомобиль: {brand} {model}\n"
        f"Текущий пробег: {mileage} км\n"
        f"Статус: {status}"
    )
    return report


def main() -> None:
    # Вызовы функций и операции
    remaining_km = calculate_remaining_mileage(current_mileage, target_mileage)
    status_msg = check_maintenance_status(
        current_mileage, target_mileage, current_date, target_date
    )

    report_text = format_car_report(car_brand, car_model, current_mileage, status_msg)

    # Вывод результатов
    print(report_text)
    print(f"Остаток пробега до ТО: {remaining_km} км")


if __name__ == "__main__":
    main()