import json
import os
from typing import List
from models.vehicles import Vehicle
from models.tasks import ServiceTask
from models.records import MaintenanceRecord


def load_vehicles(filepath: str) -> List[Vehicle]:
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r", encoding="utf-8-sig") as f:
        data = json.load(f)
        return [
            Vehicle(
                item["id"],
                item["make"],
                item["model"],
                item["year"],
                item["mileage"]
            )
            for item in data
        ]


def save_vehicles(filepath: str, vehicles: List[Vehicle]) -> None:
    data = [
        {
            "id": v.id,
            "make": v.make,
            "model": v.model,
            "year": v.year,
            "mileage": v.mileage
        }
        for v in vehicles
    ]
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def load_tasks(filepath: str) -> List[ServiceTask]:
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r", encoding="utf-8-sig") as f:
        data = json.load(f)
        return [ServiceTask.from_data(item) for item in data]


def save_tasks(filepath: str, tasks: List[ServiceTask]) -> None:
    data = [
        {
            "id": t.id,
            "title": t.title,
            "interval_km": t.interval_km,
            "cost": t.cost
        }
        for t in tasks
    ]
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def load_records(
    filepath: str,
    vehicles: List[Vehicle],
    tasks: List[ServiceTask]
) -> List[MaintenanceRecord]:
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r", encoding="utf-8-sig") as f:
        data = json.load(f)

    v_map = {v.id: v for v in vehicles}
    t_map = {t.id: t for t in tasks}
    records = []

    for item in data:
        vehicle = v_map.get(item["vehicle_id"])
        task = t_map.get(item["task_id"])
        if vehicle and task:
            rec = MaintenanceRecord(
                record_id=item["id"],
                vehicle=vehicle,
                task=task,
                scheduled_date=item["scheduled_date"],
                mileage_at_service=item["mileage_at_service"],
                is_completed=item["is_completed"]
            )
            records.append(rec)
    return records


def save_records(filepath: str, records: List[MaintenanceRecord]) -> None:
    data = [
        {
            "id": r.id,
            "vehicle_id": r.vehicle.id,
            "task_id": r.task.id,
            "scheduled_date": r.scheduled_date,
            "mileage_at_service": r.mileage_at_service,
            "is_completed": r.is_completed
        }
        for r in records
    ]
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
