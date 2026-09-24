from typing import List, Optional


class ServiceTask:
    """Класс регламентной работы по ТО."""

    def __init__(
        self,
        task_id: int,
        title: str,
        interval_km: int,
        cost: float
    ) -> None:
        self.id: int = task_id
        self.title: str = title
        self.interval_km: int = interval_km
        self.cost: float = cost

    @classmethod
    def from_data(cls, data: dict) -> "ServiceTask":
        """Фабричный метод создания объекта из словаря."""
        return cls(
            task_id=data["id"],
            title=data["title"],
            interval_km=data["interval_km"],
            cost=float(data["cost"])
        )

    def __str__(self) -> str:
        return f"[{self.id}] {self.title} (каждые {self.interval_km} км) — {self.cost:.2f} руб."


def add_task(tasks: List[ServiceTask], task: ServiceTask) -> None:
    tasks.append(task)


def find_task_by_id(tasks: List[ServiceTask], task_id: int) -> Optional[ServiceTask]:
    for t in tasks:
        if t.id == task_id:
            return t
    return None


def show_tasks(tasks: List[ServiceTask]) -> None:
    if not tasks:
        print("Список регламентных работ пуст.")
        return
    print("\n--- Регламентные работы ТО ---")
    for t in tasks:
        print(t)
