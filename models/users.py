from typing import List, Optional


class User:
    """Класс, описывающий пользователя."""

    def __init__(self, user_id: int, name: str, phone: str) -> None:
        self.id: int = user_id
        self.name: str = name
        self.phone: str = phone

    def __str__(self) -> str:
        return f"[{self.id}] {self.name} (тел: {self.phone})"


def find_user_by_id(users: List[User], user_id: int) -> Optional[User]:
    for u in users:
        if u.id == user_id:
            return u
    return None


def show_users(users: List[User]) -> None:
    if not users:
        print("Список пользователей пуст.")
        return
    print("\n--- Список пользователей ---")
    for u in users:
        print(u)
