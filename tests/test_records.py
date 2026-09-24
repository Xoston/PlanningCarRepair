from models.vehicles import Vehicle
from models.tasks import ServiceTask
from models.records import MaintenanceRecord


def test_maintenance_record_creation():
    vehicle = Vehicle(1, "Toyota", "Camry", 2020, 50000)
    task = ServiceTask(1, "Замена масла", 10000, 5000.0)

    record = MaintenanceRecord(1, vehicle, task, "2026-10-01", 60000)

    assert record.id == 1
    assert record.vehicle is vehicle
    assert record.task is task
    assert not record.is_completed


def test_complete_service():
    vehicle = Vehicle(1, "Toyota", "Camry", 2020, 50000)
    task = ServiceTask(1, "Замена масла", 10000, 5000.0)
    record = MaintenanceRecord(1, vehicle, task, "2026-10-01", 60000)

    record.complete_service()
    assert record.is_completed


def test_is_due():
    vehicle = Vehicle(1, "Toyota", "Camry", 2020, 50000)
    task = ServiceTask(1, "Замена масла", 10000, 5000.0)
    record = MaintenanceRecord(1, vehicle, task, "2026-10-01", 60000)

    assert not record.is_due(55000)
    assert record.is_due(60000)
    assert record.is_due(65000)
