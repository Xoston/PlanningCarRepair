import json
from pathlib import Path
from django.http import HttpResponse
from homepage.views import page

BASE_DIR = Path(__file__).resolve().parent.parent


def get_all_records():
    for fname in ["maintenance.json", "records.json", "tasks.json"]:
        file_path = BASE_DIR / "data" / fname
        if file_path.exists():
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if data:
                        return data
            except Exception:
                pass
    return []


def find_booking_by_id(records, record_id):
    for r in records:
        rid = r.get("id") if isinstance(r, dict) else getattr(r, "id", None)
        if rid == record_id:
            return r
    return None


def maintenance_list(request):
    records = get_all_records()
    items = ""
    for r in records:
        rid = r.get("id")
        date_str = r.get("date") or r.get("maintenance_date") or "—"
        v_info = r.get("vehicle_name") or r.get("vehicle") or f"Авто #{r.get('vehicle_id', '')}"
        desc = r.get("description") or r.get("type") or "Техническое обслуживание"
        is_cancelled = r.get("is_cancelled", False)
        status = "отменено" if is_cancelled else (r.get("status") or "активно")
        badge = "bg-secondary" if is_cancelled else "bg-success"

        items += f"""
        <li class="list-group-item d-flex justify-content-between align-items-center py-3">
            <div>
                <span class="badge badge-purple me-2">#{rid}</span>
                <span class="text-muted me-2">[{date_str}]</span>
                <a href="/maintenance/{rid}/" class="text-decoration-none fw-semibold text-purple fs-5">
                    {v_info} – {desc}
                </a>
            </div>
            <div>
                <span class="badge {badge} me-3">{status}</span>
                <a href="/maintenance/{rid}/" class="btn btn-sm btn-outline-purple">Детали →</a>
            </div>
        </li>
        """
    if not items:
        items = '<li class="list-group-item text-muted">Записи обслуживания отсутствуют</li>'

    content = f"""
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1 class="text-purple fw-bold">Журнал обслуживания и ТО</h1>
        <span class="badge badge-purple fs-6 px-3 py-2">{len(records)} записей</span>
    </div>
    <ul class="list-group shadow">
        {items}
    </ul>
    """
    return HttpResponse(page("Обслуживание – PlanningCarRepair", content))


def maintenance_detail(request, record_id):
    records = get_all_records()
    rec = find_booking_by_id(records, record_id)
    if rec is None:
        content = """
        <div class="card p-4 my-4 border-danger shadow">
            <h3 class="text-danger">Бронирование / Запись не найдена</h3>
            <p class="text-muted">Запись на обслуживание с указанным идентификатором отсутствует.</p>
            <hr>
            <a href="/maintenance/" class="btn btn-outline-purple">← к списку записей</a>
        </div>
        """
        return HttpResponse(page("Запись не найдена", content), status=404)

    date_str = rec.get("date") or rec.get("maintenance_date") or "—"
    v_info = rec.get("vehicle_name") or rec.get("vehicle") or f"Авто #{rec.get('vehicle_id', '')}"
    desc = rec.get("description") or rec.get("type") or rec.get("work_type") or "Техническое обслуживание"
    user_info = rec.get("user") or rec.get("mechanic") or f"Сотрудник #{rec.get('user_id', '')}"
    cost = rec.get("cost", "—")
    is_cancelled = rec.get("is_cancelled", False)
    status = "отменено" if is_cancelled else (rec.get("status") or "активно")
    badge = "bg-secondary" if is_cancelled else "bg-success"

    content = f"""
    <div class="card shadow my-4">
        <div class="card-header d-flex justify-content-between align-items-center py-3">
            <h4 class="mb-0 fw-bold">Заказ-наряд №{rec.get('id')}</h4>
            <span class="badge {badge} fs-6 px-3">{status}</span>
        </div>
        <div class="card-body p-4">
            <p class="card-text fs-5"><strong>Транспортное средство:</strong> <span class="text-purple">{v_info}</span></p>
            <p class="card-text fs-5"><strong>Дата проведения:</strong> {date_str}</p>
            <p class="card-text fs-5"><strong>Вид сервисных работ:</strong> {desc}</p>
            <p class="card-text fs-5"><strong>Ответственный мастер / водитель:</strong> {user_info}</p>
            <p class="card-text fs-5"><strong>Стоимость:</strong> <span class="badge badge-purple fs-6">{cost} ₽</span></p>
            <hr class="my-4">
            <a href="/maintenance/" class="btn btn-outline-purple me-2">← К списку записей</a>
            <a href="/vehicles/" class="btn btn-purple">К списку авто</a>
        </div>
    </div>
    """
    return HttpResponse(page(f"Запись №{rec.get('id')}", content), status=200)
