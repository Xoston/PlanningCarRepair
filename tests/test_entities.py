from models.users import User
from models.vehicles import Vehicle
from models.indicators import Indicator
from models.dates import ServiceDate


def test_user_creation():
    """Тест сущности Пользователь (User)."""
    user = User(1, "Иван", "+79991112233")
    assert user.id == 1
    assert user.name == "Иван"
    assert user.phone == "+79991112233"


def test_vehicle_creation():
    """Тест сущности Автомобиль (Vehicle)."""
    user = User(1, "Иван", "+79991112233")
    vehicle = Vehicle(1, "Toyota", "Camry", 2020, 50000, user)
    assert vehicle.id == 1
    assert vehicle.make == "Toyota"
    assert vehicle.owner is user
    assert vehicle.update_mileage(55000) is True
    assert vehicle.mileage == 55000


def test_indicator_creation():
    """Тест сущности Показатель (Indicator)."""
    indicator = Indicator(1, "Замена масла", 10000, 5000.0)
    assert indicator.id == 1
    assert indicator.title == "Замена масла"
    assert indicator.target_value == 10000
    assert indicator.cost == 5000.0


def test_service_date_creation():
    """Тест сущности Дата обслуживания (ServiceDate)."""
    user = User(1, "Иван", "+79991112233")
    vehicle = Vehicle(1, "Toyota", "Camry", 2020, 50000, user)
    indicator = Indicator(1, "Замена масла", 10000, 5000.0)
    service_date = ServiceDate(1, vehicle, indicator, "2026-10-01")

    assert service_date.id == 1
    assert service_date.vehicle is vehicle
    assert service_date.indicator is indicator
    assert not service_date.is_completed

    service_date.complete()
    assert service_date.is_completed
