from vehicles import add_vehicle, find_vehicles, filter_vehicles_by_mileage


def test_add_vehicle():
    vehicles = {}
    v_id = add_vehicle(vehicles, "BMW", "M8", 2023, 15000)
    assert v_id == 1
    assert len(vehicles) == 1
    assert vehicles[1]["brand"] == "BMW"


def test_find_vehicles():
    vehicles = {}
    add_vehicle(vehicles, "Audi", "R8", 2021, 45000)
    add_vehicle(vehicles, "BMW", "M5", 2022, 12000)

    results = find_vehicles(vehicles, "audi")
    assert len(results) == 1
    assert results[0]["model"] == "R8"


def test_filter_vehicles_by_mileage():
    vehicles = {}
    add_vehicle(vehicles, "Car1", "M1", 2020, 10000)
    add_vehicle(vehicles, "Car2", "M2", 2020, 50000)

    filtered = filter_vehicles_by_mileage(vehicles, 20000)
    assert len(filtered) == 1
    assert filtered[0]["brand"] == "Car1"
