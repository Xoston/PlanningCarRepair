from datetime import datetime, date


def input_int(prompt: str) -> int:
    """Запросить у пользователя целое число с валидацией ввода."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Ошибка: введите корректное целое число.")


def input_float(prompt: str) -> float:
    """Запросить у пользователя число с плавающей точкой."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Ошибка: введите числовое значение.")


def input_date(prompt: str) -> date:
    """Запросить дату в формате ДД.ММ.ГГГГ и вернуть объект date."""
    while True:
        raw_val = input(prompt).strip()
        try:
            return datetime.strptime(raw_val, "%d.%m.%Y").date()
        except ValueError:
            print("Ошибка: введите дату в формате ДД.ММ.ГГГГ (например, 15.09.2026).")
