import json
from pathlib import Path
from django.http import HttpResponse
from homepage.views import page

BASE_DIR = Path(__file__).resolve().parent.parent


def get_all_vehicles():
    file_path = BASE_DIR / "data" / "vehicles.json"
    if file_path.exists():
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return []


def find_vehicle_by_id(vehicles, vehicle_id):
    for v in vehicles:
        vid = v.get("id") if isinstance(v, dict) else getattr(v, "id", None)
        if vid == vehicle_id:
            return v
    return None


def vehicles_list(request):
    vehicles = get_all_vehicles()
    items = ""
    for v in vehicles:
        vid = v.get("id")
        brand = v.get("brand") or v.get("make") or v.get("name") or "Автомобиль"
        model = v.get("model", "")
        year = v.get("year", "—")
        plate = v.get("license_plate") or v.get("vin") or ""
        text = f"{brand} {model} ({year})"
        if plate:
            text += f" – {plate}"
        items += f"""
        <li class="list-group-item d-flex justify-content-between align-items-center py-3">
            <div>
                <span class="badge badge-purple me-2">ID: {vid}</span>
                <a href="/vehicles/{vid}/" class="text-decoration-none fw-semibold text-purple fs-5">{text}</a>
            </div>
            <a href="/vehicles/{vid}/" class="btn btn-sm btn-outline-purple">Карточка авто →</a>
        </li>
        """
    if not items:
        items = '<li class="list-group-item text-muted">Список автомобилей пуст</li>'

    content = f"""
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1 class="text-purple fw-bold">Автомобили автопарка</h1>
        <span class="badge badge-purple fs-6 px-3 py-2">{len(vehicles)} авто</span>
    </div>
    <ul class="list-group shadow">
        {items}
    </ul>
    """
    return HttpResponse(page("Автомобили – PlanningCarRepair", content))


def vehicle_detail(request, vehicle_id):
    vehicles = get_all_vehicles()
    vehicle = find_vehicle_by_id(vehicles, vehicle_id)
    if vehicle is None:
        content = """
        <div class="card p-4 my-4 border-danger shadow">
            <h3 class="text-danger">Помещение / Автомобиль не найден</h3>
            <p class="text-muted">Транспортное средство с указанным идентификатором отсутствует.</p>
            <hr>
            <a href="/vehicles/" class="btn btn-outline-purple">← к списку автомобилей</a>
        </div>
        """
        return HttpResponse(page("Автомобиль не найден", content), status=404)

    brand = vehicle.get("brand") or vehicle.get("make") or vehicle.get("name") or "Автомобиль"
    model = vehicle.get("model", "")
    year = vehicle.get("year", "—")
    plate = vehicle.get("license_plate") or vehicle.get("vin") or "—"
    mileage = vehicle.get("mileage", "—")
    status = vehicle.get("status", "исправен")
    badge_color = "bg-success" if status == "исправен" else "bg-warning text-dark"

    content = f"""
    <div class="card shadow my-4">
        <div class="card-header d-flex justify-content-between align-items-center py-3">
            <h4 class="mb-0 fw-bold">{brand} {model}</h4>
            <span class="badge {badge_color} fs-6 px-3">{status}</span>
        </div>
        <div class="card-body p-4">
            <p class="card-text fs-5"><strong>Идентификатор:</strong> <span class="text-purple">#{vehicle.get('id')}</span></p>
            <p class="card-text fs-5"><strong>Год выпуска:</strong> {year}</p>
            <p class="card-text fs-5"><strong>Гос. номер / VIN:</strong> <span class="badge badge-purple">{plate}</span></p>
            <p class="card-text fs-5"><strong>Текущий пробег:</strong> {mileage} км</p>
            <hr class="my-4">
            <a href="/vehicles/" class="btn btn-outline-purple me-2">← К списку автомобилей</a>
            <a href="/maintenance/" class="btn btn-purple">Журнал обслуживания →</a>
        </div>
    </div>
    """
    return HttpResponse(page(f"{brand} {model}", content), status=200)
