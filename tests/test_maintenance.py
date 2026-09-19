from datetime import date
from maintenance import (
    is_service_due,
    create_maintenance_record,
    cancel_maintenance_record,
)


def test_is_service_due():
    assert is_service_due(
        current_mileage=25000,
        last_service_mileage=10000,
        interval=10000
    ) is True
    assert is_service_due(
        current_mileage=15000,
        last_service_mileage=10000,
        interval=10000
    ) is False


def test_create_and_cancel_maintenance_record():
    records = []
    rec = create_maintenance_record(
        records,
        vehicle_id=1,
        work_name="Замена свечей",
        service_date=date(2026, 9, 20),
        cost=5000.0,
    )
    assert len(records) == 1
    assert rec["id"] == 1

    success = cancel_maintenance_record(records, record_id=1)
    assert success is True
    assert len(records) == 0
