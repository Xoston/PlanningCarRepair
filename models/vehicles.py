from typing import List, Optional
from models.users import User


class Vehicle:
    """Класс, описывающий автомобиль."""

    def __init__(
        self,
        vehicle_id: int,
        make: str,
        model: str,
        year: int,
        mileage: int,
        owner: User
    ) -> None:
        self.id: int = vehicle_id
        self.make: str = make
        self.model: str = model
        self.year: int = year
        self.mileage: int = mileage
        self.owner: User = owner

    def update_mileage(self, new_mileage: int) -> bool:
        if new_mileage >= self.mileage:
            self.mileage = new_mileage
            return True
        return False

    def __str__(self) -> str:
        return (
            f"[{self.id}] {self.make} {self.model} ({self.year} г.) "
            f"— {self.mileage} км | Владелец: {self.owner.name}"
        )


def find_vehicle_by_id(
    vehicles: List[Vehicle], vehicle_id: int
) -> Optional[Vehicle]:
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
