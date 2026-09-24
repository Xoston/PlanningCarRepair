from typing import List
from models.vehicles import Vehicle
from models.indicators import Indicator


class ServiceDate:
    """Класс, описывающий запланированную дату и статус ТО."""

    def __init__(
        self,
        date_id: int,
        vehicle: Vehicle,
        indicator: Indicator,
        scheduled_date: str,
        is_completed: bool = False
    ) -> None:
        self.id: int = date_id
        self.vehicle: Vehicle = vehicle
        self.indicator: Indicator = indicator
        self.scheduled_date: str = scheduled_date
        self.is_completed: bool = is_completed

    def complete(self) -> None:
        self.is_completed = True

    def __str__(self) -> str:
        status = "Выполнено" if self.is_completed else "Запланировано"
        return (
            f"Запись даты #{self.id} [{status}]\n"
            f"  Дата: {self.scheduled_date}\n"
            f"  Владелец: {self.vehicle.owner.name}\n"
            f"  Авто: {self.vehicle.make} {self.vehicle.model}\n"
            f"  Показатель: {self.indicator.title}"
        )


def show_dates(dates: List[ServiceDate]) -> None:
    if not dates:
        print("Записи дат отсутствуют.")
        return
    print("\n=== Плановые даты ТО ===")
    for d in dates:
        print(d)
        print("-" * 30)
