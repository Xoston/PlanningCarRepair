from typing import Dict, List, Any


def add_vehicle(
    vehicles: Dict[int, Dict[str, Any]],
    brand: str,
    model: str,
    year: int,
    mileage: int
) -> int:
    """Добавить новый автомобиль в словарь vehicles."""
    vehicle_id = max(vehicles.keys(), default=0) + 1
    vehicles[vehicle_id] = {
        "id": vehicle_id,
        "brand": brand,
        "model": model,
        "year": year,
        "mileage": mileage
    }
    return vehicle_id


def find_vehicles(
    vehicles: Dict[int, Dict[str, Any]],
    query: str
) -> List[Dict[str, Any]]:
    """Найти автомобили по подстроке марки или модели."""
    query_lower = query.lower()
    return [
        v for v in vehicles.values()
        if query_lower in v["brand"].lower() or query_lower in v["model"].lower()
    ]


def filter_vehicles_by_mileage(
    vehicles: Dict[int, Dict[str, Any]],
    max_mileage: int
) -> List[Dict[str, Any]]:
    """Отобрать автомобили с пробегом не более max_mileage (использует генератор)."""
    return [v for v in vehicles.values() if v["mileage"] <= max_mileage]


def sort_vehicles_by_mileage(
    vehicles: Dict[int, Dict[str, Any]],
    descending: bool = False
) -> List[Dict[str, Any]]:
    """Отсортировать список автомобилей по пробегу с помощью lambda."""
    return sorted(
        vehicles.values(),
        key=lambda v: v["mileage"],
        reverse=descending
    )
