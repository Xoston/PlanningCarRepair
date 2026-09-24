from typing import List, Optional


class Vehicle:
    """Класс, описывающий автомобиль."""

    def __init__(
        self,
        vehicle_id: int,
        make: str,
        model: str,
        year: int,
        mileage: int
    ) -> None:
        self.id: int = vehicle_id
        self.make: str = make
        self.model: str = model
        self.year: int = year
        self.mileage: int = mileage

    def update_mileage(self, new_mileage: int) -> bool:
        """Обновить пробег автомобиля."""
        if new_mileage >= self.mileage:
            self.mileage = new_mileage
            return True
        return False

    def __str__(self) -> str:
        return f"[{self.id}] {self.make} {self.model} ({self.year} г.) — {self.mileage} км"


def add_vehicle(vehicles: List[Vehicle], vehicle: Vehicle) -> None:
    vehicles.append(vehicle)


def find_vehicle_by_id(vehicles: List[Vehicle], vehicle_id: int) -> Optional[Vehicle]:
    for v in vehicles:
        if v.id == vehicle_id:
            return v
    return None


def show_vehicles(vehicles: List[Vehicle]) -> None:
    if not vehicles:
        print("Список автомобилей пуст.")
        return
    print("\n--- Список автомобилей ---")
    for v in vehicles:
        print(v)
