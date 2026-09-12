from dataclasses import dataclass, field
from datetime import date
from typing import List


@dataclass
class MaintenanceTask:
    """Класс для представления сервисной задачи."""
    title: str
    target_date: date
    target_mileage: int
    is_completed: bool = False

    def check_overdue(self, current_date: date, current_mileage: int) -> bool:
        """Проверка просрочки задачи по дате или пробегу."""
        if self.is_completed:
            return False
        return current_date >= self.target_date or current_mileage >= self.target_mileage


@dataclass
class Car:
    """Класс для хранения данных об автомобиле."""
    make: str
    model: str
    year: int
    current_mileage: int
    tasks: List[MaintenanceTask] = field(default_factory=list)

    def add_task(self, task: MaintenanceTask) -> None:
        """Добавление новой задачи в список обслуживания."""
        self.tasks.append(task)

    def get_overdue_tasks(self, today: date) -> List[MaintenanceTask]:
        """Получение списка просроченных задач."""
        return [
            task for task in self.tasks
            if task.check_overdue(today, self.current_mileage)
        ]


def main() -> None:
    # Инициализация объекта автомобиля
    my_car = Car(
        make="Toyota",
        model="Camry",
        year=2020,
        current_mileage=60000
    )

    # Создание сервисных задач
    task1 = MaintenanceTask(
        title="Замена моторного масла и фильтра",
        target_date=date(2026, 4, 15),
        target_mileage=65000
    )
    task2 = MaintenanceTask(
        title="Замена тормозных колодок",
        target_date=date(2026, 2, 1),
        target_mileage=58000
    )

    # Добавление задач к автомобилю
    my_car.add_task(task1)
    my_car.add_task(task2)

    today = date.today()

    # Вывод информации в консоль
    print(f"Автомобиль: {my_car.make} {my_car.model} ({my_car.year} г.)")
    print(f"Текущий пробег: {my_car.current_mileage} км\n")

    print("--- Список запланированных задач ---")
    for idx, task in enumerate(my_car.tasks, start=1):
        status = "Выполнено" if task.is_completed else "В ожидании"
        print(f"{idx}. {task.title} | Срок: до {task.target_date} или {task.target_mileage} км [{status}]")

    print("\n--- Требуют внимания (просрочены или подошел срок) ---")
    overdue = my_car.get_overdue_tasks(today)
    if overdue:
        for task in overdue:
            print(f"⚠️  {task.title} (Превышен пробег или дата)")
    else:
        print("Все задачи выполняются по графику.")


if __name__ == "__main__":
    main()