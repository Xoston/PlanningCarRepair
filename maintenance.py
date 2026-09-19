from datetime import date
from typing import List, Dict, Any


def is_service_due(current_mileage: int, last_service_mileage: int, interval: int = 10000) -> bool:
    """Проверить, превышен ли интервал между ТО."""
    return (current_mileage - last_service_mileage) >= interval


def get_service_status(is_due: bool) -> str:
    """Вернуть текстовый статус необходимости прохождения ТО (функция из ПР1)."""
    if is_due:
        return "Требуется проведение технического обслуживания!"
    return "Автомобиль обслужен, прохождение ТО не требуется."


def create_maintenance_record(
    records: List[Dict[str, Any]],
    vehicle_id: int,
    work_name: str,
    service_date: date,
    cost: float
) -> Dict[str, Any]:
    """Создать новую запись о проведенном или запланированном ТО."""
    record_id = max([r["id"] for r in records], default=0) + 1
    new_record = {
        "id": record_id,
        "vehicle_id": vehicle_id,
        "work_name": work_name,
        "service_date": service_date.isoformat(),
        "cost": cost
    }
    records.append(new_record)
    return new_record


def cancel_maintenance_record(records: List[Dict[str, Any]], record_id: int) -> bool:
    """Удалить запись о ТО по идентификатору."""
    for idx, rec in enumerate(records):
        if rec["id"] == record_id:
            del records[idx]
            return True
    return False
