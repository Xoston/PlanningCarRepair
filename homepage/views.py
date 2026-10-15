from django.http import HttpResponse


def page(title: str, content: str) -> str:
    bootstrap = "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <link rel="stylesheet" href="{bootstrap}">
    <style>
        :root {{
            --bg-main: #0c0a17;
            --bg-card: #15102a;
            --bg-card-hover: #1e173b;
            --border-purple: #3b2866;
            --border-glow: #6d28d9;
            --accent-purple: #8b5cf6;
            --accent-glow: #7c3aed;
            --text-main: #f1f5f9;
            --text-muted: #94a3b8;
            --text-highlight: #c084fc;
        }}
        body {{
            background: radial-gradient(circle at top right, #1f1145 0%, #0c0a17 55%, #080611 100%);
            color: var(--text-main);
            font-family: system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif;
            min-height: 100vh;
        }}
        .navbar-custom {{
            background: linear-gradient(135deg, #170d36 0%, #271059 100%);
            border-bottom: 1px solid var(--border-purple);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
        }}
        .navbar-brand {{
            color: var(--text-highlight) !important;
            font-weight: 700;
            font-size: 1.35rem;
            letter-spacing: 0.5px;
            text-shadow: 0 0 12px rgba(168, 85, 247, 0.5);
        }}
        .nav-link {{
            color: #cbd5e1 !important;
            font-weight: 500;
            border-radius: 8px;
            padding: 0.5rem 1rem !important;
            transition: all 0.2s ease;
        }}
        .nav-link:hover {{
            color: #ffffff !important;
            background: rgba(139, 92, 246, 0.2);
            text-shadow: 0 0 8px rgba(192, 132, 252, 0.6);
        }}
        .hero-box {{
            background: linear-gradient(145deg, #181135 0%, #261352 100%);
            border: 1px solid var(--border-purple);
            border-radius: 18px;
            box-shadow: 0 12px 32px rgba(0, 0, 0, 0.45);
        }}
        .card {{
            background-color: var(--bg-card) !important;
            border: 1px solid var(--border-purple) !important;
            border-radius: 14px;
            color: var(--text-main) !important;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
        }}
        .card-header {{
            background: linear-gradient(135deg, #2c125e 0%, #4c1d95 100%) !important;
            border-bottom: 1px solid #5b21b6 !important;
            color: #ffffff !important;
            border-top-left-radius: 13px !important;
            border-top-right-radius: 13px !important;
        }}
        .list-group-item {{
            background-color: var(--bg-card) !important;
            border-color: var(--border-purple) !important;
            color: var(--text-main) !important;
            transition: all 0.2s ease;
        }}
        .list-group-item:hover {{
            background-color: var(--bg-card-hover) !important;
            border-color: var(--border-glow) !important;
        }}
        .btn-purple {{
            background: linear-gradient(135deg, #7c3aed 0%, #581c87 100%);
            border: 1px solid #8b5cf6;
            color: #ffffff;
            box-shadow: 0 4px 15px rgba(124, 58, 237, 0.4);
            transition: all 0.2s ease;
        }}
        .btn-purple:hover {{
            background: linear-gradient(135deg, #9333ea 0%, #6b21a8 100%);
            border-color: #a855f7;
            color: #ffffff;
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(168, 85, 247, 0.6);
        }}
        .btn-outline-purple {{
            background: transparent;
            border: 1px solid #8b5cf6;
            color: var(--text-highlight);
            transition: all 0.2s ease;
        }}
        .btn-outline-purple:hover {{
            background: #7c3aed;
            color: #ffffff;
            box-shadow: 0 4px 15px rgba(124, 58, 237, 0.4);
        }}
        .badge-purple {{
            background: #3b1875;
            color: #e9d5ff;
            border: 1px solid #7c3aed;
        }}
        .text-purple {{
            color: var(--text-highlight) !important;
        }}
        hr {{
            border-color: var(--border-purple) !important;
            opacity: 0.6;
        }}
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-custom mb-4">
        <div class="container">
            <a class="navbar-brand d-flex align-items-center" href="/">
                <span class="me-2">🚗</span> PlanningCarRepair
            </a>
            <div class="navbar-nav">
                <a class="nav-link" href="/">Главная</a>
                <a class="nav-link" href="/vehicles/">Автомобили</a>
                <a class="nav-link" href="/maintenance/">Обслуживание и ТО</a>
            </div>
        </div>
    </nav>
    <main class="container">{content}</main>
</body>
</html>"""


def index(request):
    content = """
    <div class="p-5 mb-4 hero-box text-light">
        <div class="container-fluid py-2">
            <h1 class="display-4 fw-bold text-purple">PlanningCarRepair</h1>
            <p class="lead text-light">Интеллектуальная система управления и планирования ремонта автопарка.</p>
            <p style="color: #cbd5e1;">Единый центр мониторинга состояния автомобилей, сервисных интервалов и заказ-нарядов на техническое обслуживание.</p>
            <hr class="my-4">
            <p class="fw-semibold text-purple">Быстрый переход к разделам:</p>
            <a href="/vehicles/" class="btn btn-purple btn-lg me-3">Каталог автомобилей</a>
            <a href="/maintenance/" class="btn btn-outline-purple btn-lg">Журнал обслуживания и ТО</a>
        </div>
    </div>
    """
    return HttpResponse(page("PlanningCarRepair – Главная", content))


def page_not_found(request, exception=None):
    content = """
    <div class="text-center py-5 card p-4">
        <h1 class="display-1 text-danger fw-bold">404</h1>
        <h2 class="mb-3 text-purple">Страница не найдена</h2>
        <p class="text-muted mb-4">Запрашиваемый адрес или автомобиль не существует в базе.</p>
        <div>
            <a href="/" class="btn btn-purple px-4 py-2">Вернуться на главную</a>
        </div>
    </div>
    """
    return HttpResponse(page("404 – страница не найдена", content), status=404)
