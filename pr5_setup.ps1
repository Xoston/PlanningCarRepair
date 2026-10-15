# ============================================================================
#  ПР5: PlanningCarRepair — переход на Django (веб-интерфейс)
#  Запускать из корня репозитория (рядом с main.py):
#      powershell -ExecutionPolicy Bypass -File .\pr5_setup.ps1
# ============================================================================
$ErrorActionPreference = "Stop"
$scriptDir = $PSScriptRoot
if (-not $scriptDir) { $scriptDir = (Get-Location).Path }
Set-Location $scriptDir
$root = (Get-Location).Path
$venvPython = Join-Path $root "venv\Scripts\python.exe"

$C_gitignore = @"
venv/
__pycache__/
*.pyc
.pytest_cache/
.mypy_cache/
db.sqlite3
"@

$C_settings = @"
"""
Настройки Django-проекта carrepair (ПР5).
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-pr5-development-key"
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "homepage",
    "cars",
    "indicators",
    "dates",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "carrepair.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "carrepair.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator"
        ),
    },
]

LANGUAGE_CODE = "ru-RU"
TIME_ZONE = "Europe/Moscow"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
"@

$C_project_urls = @"
"""Корневая конфигурация маршрутов проекта carrepair (ПР5)."""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("cars/", include("cars.urls")),
    path("indicators/", include("indicators.urls")),
    path("dates/", include("dates.urls")),
]

handler404 = "homepage.views.page_not_found"
"@

$C_homepage_views = @"
"""View-функции приложения homepage (главная страница и каркас HTML)."""

from django.http import HttpResponse


def page(title, content):
    """Собрать HTML-документ с общим каркасом всех страниц проекта."""
    bootstrap = (
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3"
        "/dist/css/bootstrap.min.css"
    )
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <link rel="stylesheet" href="{bootstrap}">
</head>
<body>
    <nav class="nav">
        <a class="nav-link" href="/">Главная</a>
        <a class="nav-link" href="/cars/">Автомобили</a>
        <a class="nav-link" href="/indicators/">Показатели</a>
        <a class="nav-link" href="/dates/">Даты ТО</a>
    </nav>
    <main class="container">{content}</main>
</body>
</html>"""


def index(request):
    """Главная страница /."""
    content = """
    <h1 class="display-4">PlanningCarRepair</h1>
    <p class="lead">
        Система планирования технического обслуживания автомобиля.
    </p>
    <p>Основные разделы:</p>
    <a href="/cars/" class="btn btn-primary me-2">Автомобили</a>
    <a href="/indicators/" class="btn btn-primary me-2">Показатели</a>
    <a href="/dates/" class="btn btn-secondary">Даты ТО</a>
    """
    return HttpResponse(page("PlanningCarRepair", content))


def page_not_found(request, exception):
    """Собственная страница ошибки 404 для всего проекта."""
    content = """
    <h1 class="text-danger">404 — страница не найдена</h1>
    <p>Проверьте адрес или вернитесь на главную.</p>
    <a href="/" class="btn btn-primary">На главную</a>
    """
    return HttpResponse(
        page("404 — страница не найдена", content),
        status=404,
    )
"@

$C_homepage_urls = @"
"""Маршруты приложения homepage."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
]
"@

$C_cars_views = @"
"""View-функции приложения cars (автомобили)."""

from django.http import HttpResponse

from dates.views import date_status
from homepage.views import page
from models.vehicles import find_vehicle_by_id
from storage import (
    load_dates,
    load_indicators,
    load_users,
    load_vehicles,
)

USERS_FILE = "data/users.json"
VEHICLES_FILE = "data/vehicles.json"
INDICATORS_FILE = "data/indicators.json"
DATES_FILE = "data/dates.json"


def cars(request):
    """Страница /cars/ — список автомобилей из data/vehicles.json."""
    users = load_users(USERS_FILE)
    vehicles = load_vehicles(VEHICLES_FILE, users)
    items = ""
    for vehicle in vehicles:
        text = (
            f"{vehicle.make} {vehicle.model} ({vehicle.year} г.) "
            f"— {vehicle.mileage} км"
        )
        items += (
            f'<li class="list-group-item d-flex '
            f'justify-content-between align-items-center">'
            f'<a href="/cars/{vehicle.id}/">{text}</a>'
            f'<span class="badge bg-primary rounded-pill">'
            f"ID: {vehicle.id}</span></li>"
        )
    content = f"""
    <h1>Автомобили</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("PlanningCarRepair — автомобили", content))


def car_detail(request, vehicle_id):
    """Страница /cars/<int:vehicle_id>/ — информация об автомобиле."""
    users = load_users(USERS_FILE)
    vehicles = load_vehicles(VEHICLES_FILE, users)
    vehicle = find_vehicle_by_id(vehicles, vehicle_id)
    if vehicle is None:
        content = """
        <h1 class="text-danger">Автомобиль не найден</h1>
        <a href="/cars/" class="btn btn-outline-secondary">
            ← к списку автомобилей
        </a>
        """
        return HttpResponse(
            page("Автомобиль не найден", content),
            status=404,
        )

    indicators = load_indicators(INDICATORS_FILE)
    dates_list = load_dates(DATES_FILE, vehicles, indicators)
    planned = [d for d in dates_list if d.vehicle.id == vehicle.id]
    dates_html = ""
    if planned:
        rows = ""
        for item in planned:
            status, badge = date_status(item)
            rows += f"""
            <li class="list-group-item d-flex justify-content-between">
                <span>
                    {item.indicator.title} — {item.scheduled_date}
                </span>
                <span class="badge {badge}">{status}</span>
            </li>
            """
        dates_html = f"""
        <h5 class="mt-4">Запланированное ТО</h5>
        <ul class="list-group">{rows}</ul>
        """

    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">
                {vehicle.make} {vehicle.model}
            </h5>
            <p class="card-text">
                <strong>ID:</strong> {vehicle.id}
            </p>
            <p class="card-text">
                <strong>Год выпуска:</strong> {vehicle.year}
            </p>
            <p class="card-text">
                <strong>Пробег:</strong> {vehicle.mileage} км
            </p>
            <p class="card-text">
                <strong>Владелец:</strong> {vehicle.owner.name}
                (тел: {vehicle.owner.phone})
            </p>
            {dates_html}
            <a href="/cars/" class="btn btn-outline-secondary">
                ← к списку автомобилей
            </a>
        </div>
    </div>
    """
    return HttpResponse(
        page(f"{vehicle.make} {vehicle.model}", content),
        status=200,
    )
"@

$C_cars_urls = @"
"""Маршруты приложения cars."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.cars, name="cars"),
    path("<int:vehicle_id>/", views.car_detail, name="car_detail"),
]
"@

$C_indicators_views = @"
"""View-функции приложения indicators (показатели обслуживания)."""

from django.http import HttpResponse

from homepage.views import page
from models.indicators import find_indicator_by_id
from storage import load_indicators

INDICATORS_FILE = "data/indicators.json"


def indicators(request):
    """Страница /indicators/ — список показателей обслуживания."""
    items = ""
    for indicator in load_indicators(INDICATORS_FILE):
        text = (
            f"{indicator.title} (норма: {indicator.target_value} км) "
            f"— {indicator.cost:.2f} руб."
        )
        items += (
            f'<li class="list-group-item">'
            f'<a href="/indicators/{indicator.id}/">{text}</a></li>'
        )
    content = f"""
    <h1>Показатели обслуживания</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("PlanningCarRepair — показатели", content))


def indicator_detail(request, indicator_id):
    """Страница /indicators/<int:indicator_id>/ — информация о показателе."""
    indicator = find_indicator_by_id(
        load_indicators(INDICATORS_FILE), indicator_id
    )
    if indicator is None:
        content = """
        <h1 class="text-danger">Показатель не найден</h1>
        <a href="/indicators/" class="btn btn-outline-secondary">
            ← к списку показателей
        </a>
        """
        return HttpResponse(
            page("Показатель не найден", content),
            status=404,
        )
    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">{indicator.title}</h5>
            <p class="card-text">
                <strong>ID:</strong> {indicator.id}
            </p>
            <p class="card-text">
                <strong>Целевой пробег:</strong>
                {indicator.target_value} км
            </p>
            <p class="card-text">
                <strong>Стоимость:</strong> {indicator.cost:.2f} руб.
            </p>
            <a href="/indicators/" class="btn btn-outline-secondary">
                ← к списку показателей
            </a>
        </div>
    </div>
    """
    return HttpResponse(page(indicator.title, content), status=200)
"@

$C_indicators_urls = @"
"""Маршруты приложения indicators."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.indicators, name="indicators"),
    path(
        "<int:indicator_id>/",
        views.indicator_detail,
        name="indicator_detail",
    ),
]
"@

$C_dates_views = @"
"""View-функции приложения dates (плановые даты ТО)."""

from datetime import date

from django.http import HttpResponse

from homepage.views import page
from models.dates import find_date_by_id
from storage import load_dates, load_indicators, load_users, load_vehicles

DATES_FILE = "data/dates.json"
INDICATORS_FILE = "data/indicators.json"
USERS_FILE = "data/users.json"
VEHICLES_FILE = "data/vehicles.json"


def load_all_dates():
    """Загрузить данные проекта и вернуть список записей дат ТО."""
    users = load_users(USERS_FILE)
    vehicles = load_vehicles(VEHICLES_FILE, users)
    indicators = load_indicators(INDICATORS_FILE)
    return load_dates(DATES_FILE, vehicles, indicators)


def date_status(item):
    """Вернуть текст статуса и класс бейджа Bootstrap для записи ТО."""
    if item.is_completed:
        return "выполнено", "bg-secondary"
    if item.scheduled_date < str(date.today()):
        return "просрочено", "bg-danger"
    return "запланировано", "bg-success"


def dates(request):
    """Страница /dates/ — список плановых дат ТО."""
    items = ""
    for item in load_all_dates():
        status, badge = date_status(item)
        items += f"""
        <li class="list-group-item d-flex justify-content-between">
            <a href="/dates/{item.id}/">
                {item.vehicle.make} {item.vehicle.model}
                — {item.indicator.title} — {item.scheduled_date}
            </a>
            <span class="badge {badge}">{status}</span>
        </li>
        """
    content = f"""
    <h1>Плановые даты ТО</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("PlanningCarRepair — даты ТО", content))


def date_detail(request, date_id):
    """Страница /dates/<int:date_id>/ — информация о записи ТО."""
    item = find_date_by_id(load_all_dates(), date_id)
    if item is None:
        content = """
        <h1 class="text-danger">Запись ТО не найдена</h1>
        <a href="/dates/" class="btn btn-outline-secondary">
            ← к списку дат ТО
        </a>
        """
        return HttpResponse(
            page("Запись ТО не найдена", content),
            status=404,
        )
    status, badge = date_status(item)
    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">Запись ТО #{item.id}</h5>
            <p class="card-text">
                <strong>Автомобиль:</strong>
                {item.vehicle.make} {item.vehicle.model}
            </p>
            <p class="card-text">
                <strong>Показатель:</strong> {item.indicator.title}
            </p>
            <p class="card-text">
                <strong>Плановая дата:</strong> {item.scheduled_date}
            </p>
            <p class="card-text">
                <strong>Статус:</strong>
                <span class="badge {badge}">{status}</span>
            </p>
            <a href="/dates/" class="btn btn-outline-secondary">
                ← к списку дат ТО
            </a>
        </div>
    </div>
    """
    return HttpResponse(page(f"Запись ТО #{item.id}", content), status=200)
"@

$C_dates_urls = @"
"""Маршруты приложения dates."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.dates, name="dates"),
    path("<int:date_id>/", views.date_detail, name="date_detail"),
]
"@

$C_admin_stub = @"
# Админ-панель Django.
# Модели будут зарегистрированы после перехода на Django ORM (следующие ПР).
"@

$C_models_stub = @"
# Django-модели приложения.
# Предметные классы User, Vehicle, Indicator, ServiceDate пока находятся
# в пакете models/ корня проекта (ПР3) и загружаются из JSON-файлов.
# Django-модели будут добавлены после перехода на Django ORM.
"@

$C_tests_stub = @"
# Тесты Django-приложения.
# Автоматизированные тесты предметной области (ПР3) находятся
# в каталоге tests/ корня проекта и запускаются командой pytest.
"@

$C_flake8 = @"
[flake8]
exclude =
    .git,
    venv,
    __pycache__,
    .pytest_cache,
    .mypy_cache,
    */migrations/*
"@

$C_readme = @"
# PlanningCarRepair — система планирования ТО автомобиля

## Назначение
PlanningCarRepair — приложение для планирования технического обслуживания
автомобиля. Консольная версия приложения (ПР3) дополнена веб-интерфейсом
на Django (ПР5).

## Используемые технологии
- Python 3
- Django 5.2 — веб-фреймворк
- HTML — разметка веб-страниц
- CSS и Bootstrap 5.3 — оформление страниц
- pytest — автоматизированные тесты
- flake8 — проверка качества кода

## Целевая аудитория
Автовладельцы, желающие своевременно проходить техническое обслуживание
и отслеживать сервисные показатели автомобиля.

## Предметная область
Техническое обслуживание автотранспорта (замена масла, фильтров,
тормозных колодок, плановые осмотры).

## Основные сущности

### User — пользователь
Атрибуты: `id`, `name`, `phone`.

### Vehicle — автомобиль
Атрибуты: `id`, `make` (марка), `model` (модель), `year` (год выпуска),
`mileage` (пробег), `owner` (объект `User`).
Методы: `update_mileage()`, `__str__()`.

### Indicator — показатель обслуживания
Атрибуты: `id`, `title`, `target_value` (целевой пробег), `cost` (стоимость).
Методы: `__str__()`.

### ServiceDate — запланированная дата ТО
Атрибуты: `id`, `vehicle` (объект `Vehicle`), `indicator` (объект
`Indicator`), `scheduled_date`, `is_completed`.
Методы: `complete()`, `__str__()`.

## Страницы веб-интерфейса
- `/` — главная страница (view-функция `index()`)
- `/cars/` — список автомобилей (view-функция `cars()`)
- `/cars/<int:vehicle_id>/` — страница автомобиля (view-функция `car_detail()`)
- `/indicators/` — список показателей (view-функция `indicators()`)
- `/indicators/<int:indicator_id>/` — страница показателя
  (view-функция `indicator_detail()`)
- `/dates/` — список плановых дат ТО (view-функция `dates()`)
- `/dates/<int:date_id>/` — страница записи ТО (view-функция `date_detail()`)

Если объект с указанным идентификатором не найден, страница возвращает
код статуса 404. Для любого несуществующего адреса настроена собственная
страница ошибки 404 (`handler404`).

## Хранение данных
Данные хранятся в JSON-файлах каталога `data/`:
- `data/users.json`
- `data/vehicles.json`
- `data/indicators.json`
- `data/dates.json`

При загрузке JSON преобразуется в объекты `User`, `Vehicle`, `Indicator`,
`ServiceDate` (модуль `storage.py`).

## Структура проекта
- `carrepair/` — пакет конфигурации Django-проекта (`settings.py`, `urls.py`)
- `homepage/` — главная страница и общий HTML-каркас `page()`
- `cars/` — автомобили
- `indicators/` — показатели обслуживания
- `dates/` — плановые даты ТО
- `models/` — предметные классы ПР3
- `storage.py` — загрузка и сохранение JSON
- `main.py` — консольное приложение (сохранено из ПР3)
- `tests/` — автоматизированные тесты

## Запуск приложения
Веб-версия (Django):
```
venv\Scripts\python.exe manage.py runserver
```
Адрес: http://127.0.0.1:8000/

Консольная версия (сохранена):
```
venv\Scripts\python.exe main.py
```

## Тестирование и проверка кода
```
venv\Scripts\python.exe -m pytest -v
venv\Scripts\python.exe -m flake8
```

## Текущее состояние и план развития
Реализовано (ПР5):
- Django-проект `carrepair` и приложения `homepage`, `cars`,
  `indicators`, `dates`
- маршрутизация URL двух уровней
- view-функции и страницы на основе данных ПР3
- проверка статуса записи ТО (выполнено / запланировано / просрочено)
- обработка ошибки 404
- оформление Bootstrap 5.3

Планируется:
- перенос сущностей в Django ORM и подключение базы данных
- переход на шаблоны (`templates/`) и отказ от функции `page()`
- формы создания и редактирования объектов
- регистрация и авторизация пользователей
- разработка API, контейнеризация, CI/CD
"@

$C_find_date_by_id = @"


def find_date_by_id(
    dates: List[ServiceDate], date_id: int
) -> Optional[ServiceDate]:
    """Найти запись даты ТО по идентификатору."""
    for item in dates:
        if item.id == date_id:
            return item
    return None
"@

function Write-Utf8([string]$RelativePath, [string]$Content) {
    $full = Join-Path $root $RelativePath
    $dir = Split-Path $full -Parent
    if ($dir -and -not (Test-Path $dir)) {
        New-Item -ItemType Directory -Force -Path $dir | Out-Null
    }
    [System.IO.File]::WriteAllText(
        $full, $Content, (New-Object System.Text.UTF8Encoding($false)))
    Write-Host "  создан: $RelativePath" -ForegroundColor Green
}

# ---------------------------------------------------------------- шаг 1: .gitignore
Write-Host "== Шаг 1: .gitignore ==" -ForegroundColor Cyan
Write-Utf8 ".gitignore" $C_gitignore

# -------------------------------------------------- шаг 2: контрольная точка Git
Write-Host "== Шаг 2: контрольная точка Git ==" -ForegroundColor Cyan
try {
    $dirty = git status --porcelain
    if ($dirty) {
        git add .
        git commit -m "PR5: подготовка проекта к переходу на Django"
        Write-Host "  контрольная точка создана" -ForegroundColor Green
    } else {
        Write-Host "  изменений нет, коммит не требуется"
    }
} catch {
    Write-Host "  (git пропущен: $($_.Exception.Message))" -ForegroundColor Yellow
}

# ------------------------------------------------------- шаг 3: виртуальное окружение
Write-Host "== Шаг 3: виртуальное окружение и зависимости ==" -ForegroundColor Cyan
if (-not (Test-Path $venvPython)) {
    try { py -m venv venv } catch { python -m venv venv }
    Write-Host "  venv создан"
} else {
    Write-Host "  venv уже существует"
}
$req = Join-Path $root "requirements.txt"
if (-not (Select-String -Path $req -Pattern "Django" -Quiet)) {
    [System.IO.File]::AppendAllText(
        $req, "Django==5.2.*`r`n",
        (New-Object System.Text.UTF8Encoding($false)))
    Write-Host "  в requirements.txt добавлено: Django==5.2.*"
}
& $venvPython -m pip install -r requirements.txt
& $venvPython -m django --version

# ------------------------------------------------------------- шаг 4: Django-проект
Write-Host "== Шаг 4: создание Django-проекта carrepair ==" -ForegroundColor Cyan
if (-not (Test-Path (Join-Path $root "manage.py"))) {
    & $venvPython -m django startproject carrepair .
    Write-Host "  проект carrepair создан"
} else {
    Write-Host "  manage.py уже существует, пропуск"
}

# ------------------------------------------------------------- шаг 5: приложения
Write-Host "== Шаг 5: создание Django-приложений ==" -ForegroundColor Cyan
foreach ($app in @("homepage", "cars", "indicators", "dates")) {
    if (-not (Test-Path (Join-Path $root $app))) {
        & $venvPython -m django startapp $app
        Write-Host "  приложение $app создано"
    } else {
        Write-Host "  приложение $app уже существует, пропуск"
    }
}

# ------------------------------------------------------------- шаг 6: файлы проекта
Write-Host "== Шаг 6: запись файлов ==" -ForegroundColor Cyan
Write-Utf8 "carrepair\settings.py" $C_settings
Write-Utf8 "carrepair\urls.py" $C_project_urls
Write-Utf8 "homepage\views.py" $C_homepage_views
Write-Utf8 "homepage\urls.py" $C_homepage_urls
Write-Utf8 "cars\views.py" $C_cars_views
Write-Utf8 "cars\urls.py" $C_cars_urls
Write-Utf8 "indicators\views.py" $C_indicators_views
Write-Utf8 "indicators\urls.py" $C_indicators_urls
Write-Utf8 "dates\views.py" $C_dates_views
Write-Utf8 "dates\urls.py" $C_dates_urls
foreach ($app in @("homepage", "cars", "indicators", "dates")) {
    Write-Utf8 "$app\admin.py" $C_admin_stub
    Write-Utf8 "$app\models.py" $C_models_stub
    Write-Utf8 "$app\tests.py" $C_tests_stub
}
Write-Utf8 ".flake8" $C_flake8
Write-Utf8 "README.md" $C_readme

# ------------------------- шаг 7: find_date_by_id в models/dates.py (логика ПР3)
Write-Host "== Шаг 7: доработка models/dates.py ==" -ForegroundColor Cyan
$datesPath = Join-Path $root "models\dates.py"
$text = [System.IO.File]::ReadAllText($datesPath)
if ($text -notmatch "find_date_by_id") {
    if ($text -notmatch "Optional") {
        $text = $text -replace
            "from typing import List", "from typing import List, Optional"
    }
    $text = $text.TrimEnd() + "`r`n`r`n" + $C_find_date_by_id.TrimStart()
    [System.IO.File]::WriteAllText(
        $datesPath, $text, (New-Object System.Text.UTF8Encoding($false)))
    Write-Host "  в models/dates.py добавлена find_date_by_id()"
} else {
    Write-Host "  find_date_by_id уже есть, пропуск"
}

# ------------------------------------------------------------- шаг 8: проверка
Write-Host "== Шаг 8: миграции и проверка проекта ==" -ForegroundColor Cyan
& $venvPython manage.py migrate
& $venvPython manage.py check

Write-Host "== Шаг 9: flake8 и pytest (предупреждения не прерывают скрипт) ==" -ForegroundColor Cyan
try { & $venvPython -m flake8 } catch {
    Write-Host "  flake8: есть замечания, исправьте их вручную" -ForegroundColor Yellow
}
try { & $venvPython -m pytest -v } catch {
    Write-Host "  pytest: есть падения, проверьте вручную" -ForegroundColor Yellow
}

# ------------------------------------------------------------- шаг 10: Git
Write-Host "== Шаг 10: фиксация результата в Git ==" -ForegroundColor Cyan
try {
    git add .
    git commit -m "PR5: add Django project and web pages"
    Write-Host "  коммит PR5 создан" -ForegroundColor Green
} catch {
    Write-Host "  (git пропущен: $($_.Exception.Message))" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "ГОТОВО! Запуск веб-приложения:" -ForegroundColor Green
Write-Host "  venv\Scripts\python.exe manage.py runserver" -ForegroundColor White
Write-Host "Затем откройте в браузере: http://127.0.0.1:8000/" -ForegroundColor White
Write-Host "Проверьте: /  /cars/  /cars/1/  /indicators/  /indicators/1/  /dates/  /dates/1/  /nonexistent/" -ForegroundColor White
