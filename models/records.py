from typing import List, Optional
from models.vehicles import Vehicle
from models.tasks import ServiceTask


class MaintenanceRecord:
    """Запись о запланированном или выполненном ТО."""

    def __init__(
        self,
        record_id: int,
        vehicle: Vehicle,
        task: ServiceTask,
        scheduled_date: str,
        mileage_at_service: int,
        is_completed: bool = False
    ) -> None:
        self.id: int = record_id
        self.vehicle: Vehicle = vehicle
        self.task: ServiceTask = task
        self.scheduled_date: str = scheduled_date
        self.mileage_at_service: int = mileage_at_service
        self.is_completed: bool = is_completed

    def complete_service(self) -> None:
        """Отметить обслуживание как выполненное."""
        self.is_completed = True

    def is_due(self, current_mileage: int) -> bool:
        """Проверить, наступил ли срок выполнения по пробегу."""
        if self.is_completed:
            return False
        return current_mileage >= self.mileage_at_service

    def __str__(self) -> str:
        status = "Выполнено" if self.is_completed else "Запланировано"
        return (
            f"Запись #{self.id} [{status}]\n"
            f"  Авто: {self.vehicle.make} {self.vehicle.model} (ID: {self.vehicle.id})\n"
            f"  Работа: {self.task.title}\n"
            f"  Дата: {self.scheduled_date} | Пробег ТО: {self.mileage_at_service} км"
        )


def create_record(
    records: List[MaintenanceRecord],
    record_id: int,
    vehicle: Vehicle,
    task: ServiceTask,
    scheduled_date: str,
    mileage_at_service: int
) -> MaintenanceRecord:
    record = MaintenanceRecord(
        record_id=record_id,
        vehicle=vehicle,
        task=task,
        scheduled_date=scheduled_date,
        mileage_at_service=mileage_at_service
    )
    records.append(record)
    return record


def show_records(records: List[MaintenanceRecord]) -> None:
    if not records:
        print("Записи обслуживания отсутствуют.")
        return
    print("\n=== История и план ТО ===")
    for r in records:
        print(r)
        print("-" * 30)
