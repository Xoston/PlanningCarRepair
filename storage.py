import json
import os
from typing import List
from models.users import User
from models.vehicles import Vehicle
from models.indicators import Indicator
from models.dates import ServiceDate


def load_users(filepath: str) -> List[User]:
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r", encoding="utf-8-sig") as f:
        data = json.load(f)
        return [User(i["id"], i["name"], i["phone"]) for i in data]


def save_users(filepath: str, users: List[User]) -> None:
    data = [{"id": u.id, "name": u.name, "phone": u.phone} for u in users]
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def load_vehicles(filepath: str, users: List[User]) -> List[Vehicle]:
    if not os.path.exists(filepath):
        return []
    u_map = {u.id: u for u in users}
    with open(filepath, "r", encoding="utf-8-sig") as f:
        data = json.load(f)
        vehicles = []
        for item in data:
            owner = u_map.get(item["user_id"])
            if owner:
                v = Vehicle(
                    item["id"],
                    item["make"],
                    item["model"],
                    item["year"],
                    item["mileage"],
                    owner
                )
                vehicles.append(v)
        return vehicles


def save_vehicles(filepath: str, vehicles: List[Vehicle]) -> None:
    data = [
        {
            "id": v.id,
            "make": v.make,
            "model": v.model,
            "year": v.year,
            "mileage": v.mileage,
            "user_id": v.owner.id
        }
        for v in vehicles
    ]
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def load_indicators(filepath: str) -> List[Indicator]:
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r", encoding="utf-8-sig") as f:
        data = json.load(f)
        return [
            Indicator(i["id"], i["title"], i["target_value"], float(i["cost"]))
            for i in data
        ]


def save_indicators(filepath: str, indicators: List[Indicator]) -> None:
    data = [
        {
            "id": ind.id,
            "title": ind.title,
            "target_value": ind.target_value,
            "cost": ind.cost
        }
        for ind in indicators
    ]
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def load_dates(
    filepath: str, vehicles: List[Vehicle], indicators: List[Indicator]
) -> List[ServiceDate]:
    if not os.path.exists(filepath):
        return []
    v_map = {v.id: v for v in vehicles}
    i_map = {ind.id: ind for ind in indicators}
    with open(filepath, "r", encoding="utf-8-sig") as f:
        data = json.load(f)
        dates = []
        for item in data:
            v = v_map.get(item["vehicle_id"])
            ind = i_map.get(item["indicator_id"])
            if v and ind:
                dates.append(
                    ServiceDate(
                        item["id"],
                        v,
                        ind,
                        item["scheduled_date"],
                        item["is_completed"]
                    )
                )
        return dates


def save_dates(filepath: str, dates: List[ServiceDate]) -> None:
    data = [
        {
            "id": d.id,
            "vehicle_id": d.vehicle.id,
            "indicator_id": d.indicator.id,
            "scheduled_date": d.scheduled_date,
            "is_completed": d.is_completed
        }
        for d in dates
    ]
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
