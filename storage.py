import json
import os
from typing import Dict, List, Any


def load_vehicles(filepath: str) -> Dict[int, Dict[str, Any]]:
    """Загрузить словарь автомобилей из JSON-файла."""
    if not os.path.exists(filepath):
        return {}
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
            return {item["id"]: item for item in raw_data}
    except (json.JSONDecodeError, KeyError):
        print(f"Предупреждение: Файл {filepath} поврежден или имеет неверный формат.")
        return {}


def save_vehicles(filepath: str, vehicles: Dict[int, Dict[str, Any]]) -> None:
    """Сохранить словарь автомобилей в JSON-файл."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(list(vehicles.values()), f, ensure_ascii=False, indent=2)


def load_maintenance(filepath: str) -> List[Dict[str, Any]]:
    """Загрузить список записей ТО из JSON-файла."""
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Предупреждение: Файл {filepath} поврежден.")
        return []


def save_maintenance(filepath: str, records: List[Dict[str, Any]]) -> None:
    """Сохранить список записей ТО в JSON-файл."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
