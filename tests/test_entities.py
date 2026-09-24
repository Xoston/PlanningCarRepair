from models.users import User
from models.vehicles import Vehicle
from models.indicators import Indicator
from models.dates import ServiceDate


def test_entities_creation():
    user = User(1, "Иван", "+79991112233")
    vehicle = Vehicle(1, "Toyota", "Camry", 2020, 50000, user)
    indicator = Indicator(1, "Замена масла", 10000, 5000.0)
    service_date = ServiceDate(1, vehicle, indicator, "2026-10-01")

    assert user.name == "Иван"
    assert vehicle.owner is user
    assert indicator.target_value == 10000
    assert service_date.scheduled_date == "2026-10-01"
    assert not service_date.is_completed
