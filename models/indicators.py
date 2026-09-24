from typing import List, Optional


class Indicator:
    """Класс, описывающий показатель обслуживания."""

    def __init__(
        self,
        indicator_id: int,
        title: str,
        target_value: int,
        cost: float
    ) -> None:
        self.id: int = indicator_id
        self.title: str = title
        self.target_value: int = target_value
        self.cost: float = cost

    def __str__(self) -> str:
        return (
            f"[{self.id}] Показатель: {self.title} "
            f"(норма: {self.target_value} км) — {self.cost:.2f} руб."
        )


def find_indicator_by_id(
    indicators: List[Indicator], indicator_id: int
) -> Optional[Indicator]:
    for ind in indicators:
        if ind.id == indicator_id:
            return ind
    return None


def show_indicators(indicators: List[Indicator]) -> None:
    if not indicators:
        print("Список показателей пуст.")
        return
    print("\n--- Список показателей ---")
    for ind in indicators:
        print(ind)
