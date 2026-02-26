import dash
from dash import Dash, dcc, html, Input, Output, State
from dash.dash_table import DataTable
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import os


# ---------- Sample data ----------
projects_data = [
    # فناوری اطلاعات
    {
        "department": "فناوری اطلاعات",
        "manager": "علی رضایی",
        "project_name": "راه‌اندازی پلتفرم ابری داخلی",
        "start_date": "2025-01-15",
        "status": "در حال انجام",
        "score": 89,
    },
    {
        "department": "فناوری اطلاعات",
        "manager": "علی رضایی",
        "project_name": "اتوماسیون فرایندهای اداری",
        "start_date": "2025-03-02",
        "status": "در حال انجام",
        "score": 92,
    },
    {
        "department": "فناوری اطلاعات",
        "manager": "مریم کریمی",
        "project_name": "به‌روزرسانی زیرساخت شبکه",
        "start_date": "2024-11-20",
        "status": "نزدیک به اتمام",
        "score": 85,
    },
    {
        "department": "فناوری اطلاعات",
        "manager": "مریم کریمی",
        "project_name": "پیاده‌سازی سیستم مانیتورینگ",
        "start_date": "2025-02-10",
        "status": "در حال انجام",
        "score": 81,
    },
    # مالی
    {
        "department": "مالی",
        "manager": "حسین موسوی",
        "project_name": "سیستم مدیریت بودجه",
        "start_date": "2025-01-05",
        "status": "در حال انجام",
        "score": 78,
    },
    {
        "department": "مالی",
        "manager": "حسین موسوی",
        "project_name": "دیجیتالی‌سازی اسناد مالی",
        "start_date": "2024-12-10",
        "status": "در حال انجام",
        "score": 83,
    },
    {
        "department": "مالی",
        "manager": "نگار احمدی",
        "project_name": "بازطراحی ساختار گزارش‌دهی مالی",
        "start_date": "2025-03-12",
        "status": "در حال انجام",
        "score": 80,
    },
    # منابع انسانی
    {
        "department": "منابع انسانی",
        "manager": "سارا محمدی",
        "project_name": "پیاده‌سازی سیستم ارزیابی عملکرد",
        "start_date": "2025-01-25",
        "status": "در حال انجام",
        "score": 90,
    },
    {
        "department": "منابع انسانی",
        "manager": "سارا محمدی",
        "project_name": "برنامه توسعه مهارت مدیران",
        "start_date": "2025-02-18",
        "status": "در حال انجام",
        "score": 88,
    },
    {
        "department": "منابع انسانی",
        "manager": "مجتبی نوری",
        "project_name": "سیستم جذب و استخدام آنلاین",
        "start_date": "2024-12-01",
        "status": "نزدیک به اتمام",
        "score": 86,
    },
    # بازاریابی
    {
        "department": "بازاریابی",
        "manager": "الهام صادقی",
        "project_name": "کمپین دیجیتال برندینگ",
        "start_date": "2025-01-10",
        "status": "در حال انجام",
        "score": 91,
    },
    {
        "department": "بازاریابی",
        "manager": "الهام صادقی",
        "project_name": "تحلیل رفتار مشتریان",
        "start_date": "2025-02-05",
        "status": "در حال انجام",
        "score": 87,
    },
    {
        "department": "بازاریابی",
        "manager": "امیر تقوی",
        "project_name": "طراحی باشگاه مشتریان",
        "start_date": "2024-11-30",
        "status": "در حال انجام",
        "score": 84,
    },
    # تحقیق و توسعه
    {
        "department": "تحقیق و توسعه",
        "manager": "رضا کاظمی",
        "project_name": "پروژه هوش مصنوعی پیش‌بینی فروش",
        "start_date": "2025-01-20",
        "status": "در حال انجام",
        "score": 94,
    },
    {
        "department": "تحقیق و توسعه",
        "manager": "رضا کاظمی",
        "project_name": "تحقیق بازار محصولات جدید",
        "start_date": "2025-03-01",
        "status": "در حال انجام",
        "score": 89,
    },
    {
        "department": "تحقیق و توسعه",
        "manager": "نسیم رستگار",
        "project_name": "آزمایش نمونه اولیه محصول",
        "start_date": "2024-12-15",
        "status": "نزدیک به اتمام",
        "score": 88,
    },
]

df = pd.DataFrame(projects_data)


# ---------- Aggregations for level 1 ----------
dept_summary = (
    df.groupby("department")
    .agg(
        active_projects=("project_name", "count"),
        avg_score=("score", "mean"),
    )
    .reset_index()
)

dept_summary["avg_score"] = dept_summary["avg_score"].round(1)

bar_fig = px.bar(
    dept_summary,
    x="department",
    y="active_projects",
    labels={"department": "واحد سازمانی", "active_projects": "تعداد پروژه‌های فعال"},
)
bar_fig.update_layout(
    template="plotly_white",
    title=None,
    xaxis_title=None,
    yaxis_title="تعداد پروژه‌های فعال",
    margin=dict(l=40, r=40, t=20, b=80),
    xaxis_tickangle=-25,
    autosize=True,
)

line_fig = px.line(
    dept_summary,
    x="department",
    y="avg_score",
    markers=True,
    labels={"department": "واحد سازمانی", "avg_score": "میانگین امتیاز"},
)
line_fig.update_layout(
    template="plotly_white",
    title=None,
    xaxis_title=None,
    yaxis_title="میانگین امتیاز",
    margin=dict(l=40, r=40, t=20, b=80),
    xaxis_tickangle=-25,
    autosize=True,
)


# ---------- App setup ----------
external_stylesheets = [dbc.themes.BOOTSTRAP]
app: Dash = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
app.title = "داشبورد پروژه‌های سازمانی"

# Render/Gunicorn entrypoint
server = app.server


def make_table_style():
    return {
        "style_header": {
            "backgroundColor": "#f5f5f5",
            "fontWeight": "bold",
            "border": "1px solid #ddd",
        },
        "style_cell": {
            "textAlign": "right",
            "padding": "8px",
            "border": "1px solid #eee",
            "fontFamily": "IRANSans, Vazirmatn, Segoe UI, sans-serif",
            "fontSize": "13px",
        },
        "style_table": {
            "width": "100%",
            "overflowX": "auto",
        },
        "style_data_conditional": [
            {
                "if": {"row_index": "odd"},
                "backgroundColor": "#fafafa",
            }
        ],
    }


base_table_style = make_table_style()


app.layout = html.Div(
    className="app-bg",
    children=[
        dcc.Store(id="selected-department"),
        dbc.Container(
            fluid=True,
            className="app-shell",
            children=[
                dbc.Row(
                    className="g-0 app-row",
                    children=[
                        # Sidebar
                        dbc.Col(
                            className="sidebar-wrapper",
                            md=2,
                            children=[
                                html.Div(
                                    className="sidebar-card",
                                    children=[
                                        html.Div(
                                            className="sidebar-logo mb-4",
                                            children=html.Div("DP", className="logo-circle"),
                                        ),
                                        html.Div(
                                            className="sidebar-nav",
                                            children=[
                                                html.Button(
                                                    "نمای کلی",
                                                    id="nav-overview",
                                                    n_clicks=0,
                                                    className="sidebar-item active",
                                                ),
                                                html.Button(
                                                    "پروژه‌ها",
                                                    id="nav-projects",
                                                    n_clicks=0,
                                                    className="sidebar-item",
                                                ),
                                                html.Button(
                                                    "تسک‌ها",
                                                    id="nav-tasks",
                                                    n_clicks=0,
                                                    className="sidebar-item",
                                                ),
                                                html.Button(
                                                    "اعضا",
                                                    id="nav-members",
                                                    n_clicks=0,
                                                    className="sidebar-item",
                                                ),
                                                html.Button(
                                                    "تنظیمات",
                                                    id="nav-settings",
                                                    n_clicks=0,
                                                    className="sidebar-item",
                                                ),
                                            ],
                                        ),
                                    ],
                                )
                            ],
                        ),
                        # Main content
                        dbc.Col(
                            md=10,
                            className="main-wrapper",
                            children=[
                                # Overview page (default)
                                html.Div(
                                    id="overview-content",
                                    className="main-card",
                                    children=[
                                        # Top bar
                                        html.Div(
                                            className="topbar",
                                            children=[
                                                html.Div(
                                                    className="topbar-title",
                                                    children=[
                                                        html.H2(
                                                            "نمای کلی",
                                                            className="topbar-heading",
                                                        ),
                                                        html.P(
                                                            "مروری بر پروژه‌های فعال سازمان و عملکرد واحدها",
                                                            className="topbar-subtitle",
                                                        ),
                                                    ],
                                                ),
                                                html.Div(
                                                    className="topbar-actions",
                                                    children=[
                                                        dbc.Input(
                                                            type="search",
                                                            placeholder="جستجو در پروژه‌ها...",
                                                            className="search-input",
                                                        ),
                                                        dbc.Button(
                                                            "گزارش این هفته",
                                                            color="primary",
                                                            className="topbar-btn",
                                                        ),
                                                    ],
                                                ),
                                            ],
                                        ),
                                        # Charts row
                                        dbc.Row(
                                            className="charts-row gy-3 mb-4",
                                            children=[
                                                dbc.Col(
                                                    md=7,
                                                    children=html.Div(
                                                        className="chart-card",
                                                        children=[
                                                            html.Div(
                                                                className="card-header-line",
                                                                children=[
                                                                    html.Div(
                                                                        [
                                                                            html.H5(
                                                                                "پروژه‌های فعال",
                                                                                className="card-title",
                                                                            ),
                                                                            html.P(
                                                                                "تعداد پروژه‌ها به تفکیک واحد سازمانی",
                                                                                className="card-caption",
                                                                            ),
                                                                        ]
                                                                    ),
                                                                ],
                                                            ),
                                                            dcc.Graph(
                                                                id="projects-per-dept-bar",
                                                                figure=bar_fig,
                                                                responsive=True,
                                                                config={"displayModeBar": False, "responsive": True},
                                                            ),
                                                        ],
                                                    ),
                                                ),
                                                dbc.Col(
                                                    md=5,
                                                    children=html.Div(
                                                        className="chart-card",
                                                        children=[
                                                            html.Div(
                                                                className="card-header-line",
                                                                children=[
                                                                    html.Div(
                                                                        [
                                                                            html.H5(
                                                                                "میانگین امتیاز",
                                                                                className="card-title",
                                                                            ),
                                                                            html.P(
                                                                                "امتیاز کیفی پروژه‌ها در هر واحد",
                                                                                className="card-caption",
                                                                            ),
                                                                        ]
                                                                    ),
                                                                ],
                                                            ),
                                                            dcc.Graph(
                                                                id="avg-score-line",
                                                                figure=line_fig,
                                                                responsive=True,
                                                                config={"displayModeBar": False, "responsive": True},
                                                            ),
                                                        ],
                                                    ),
                                                ),
                                            ],
                                        ),
                                        # Managers table (level 2)
                                        html.Div(
                                            id="dept-managers-section",
                                            className="section-card",
                                            children=[
                                                html.Div(
                                                    className="section-header",
                                                    children=[
                                                        html.H5(
                                                            "مدیران پروژه در واحد انتخاب‌شده",
                                                            className="card-title mb-1",
                                                        ),
                                                        html.P(
                                                            "برای مشاهده جزئیات، ابتدا روی نوار واحد سازمانی در نمودار بالا کلیک کنید.",
                                                            id="dept-hint-text",
                                                            className="card-caption",
                                                        ),
                                                    ],
                                                ),
                                                DataTable(
                                                    id="dept-managers-table",
                                                    columns=[
                                                        {"name": "مدیر پروژه", "id": "manager"},
                                                        {"name": "تعداد پروژه‌ها", "id": "project_count"},
                                                        {"name": "میانگین امتیاز", "id": "avg_score"},
                                                    ],
                                                    data=[],
                                                    row_selectable=False,
                                                    cell_selectable=True,
                                                    **base_table_style,
                                                ),
                                            ],
                                            style={"display": "none"},
                                        ),
                                        # Manager projects table (level 3)
                                        html.Div(
                                            id="manager-projects-section",
                                            className="section-card",
                                            children=[
                                                html.Div(
                                                    className="section-header",
                                                    children=[
                                                        html.H5(
                                                            "جزئیات پروژه‌های مدیر انتخاب‌شده",
                                                            className="card-title mb-1",
                                                        ),
                                                        html.P(
                                                            "برای مشاهده جزئیات یک مدیر، روی نام او در جدول بالا کلیک کنید.",
                                                            id="manager-hint-text",
                                                            className="card-caption",
                                                        ),
                                                    ],
                                                ),
                                                DataTable(
                                                    id="manager-projects-table",
                                                    columns=[
                                                        {"name": "نام پروژه", "id": "project_name"},
                                                        {"name": "تاریخ شروع", "id": "start_date"},
                                                        {"name": "وضعیت", "id": "status"},
                                                        {"name": "امتیاز", "id": "score"},
                                                    ],
                                                    data=[],
                                                    row_selectable=False,
                                                    cell_selectable=False,
                                                    **base_table_style,
                                                ),
                                            ],
                                            style={"display": "none"},
                                        ),
                                    ],
                                ),
                                # Projects page
                                html.Div(
                                    id="projects-content",
                                    className="main-card",
                                    style={"display": "none"},
                                    children=[
                                        html.Div(
                                            className="topbar",
                                            children=[
                                                html.Div(
                                                    className="topbar-title",
                                                    children=[
                                                        html.H2(
                                                            "پروژه‌ها",
                                                            className="topbar-heading",
                                                        ),
                                                        html.P(
                                                            "لیست همه پروژه‌ها به همراه واحد، مدیر و وضعیت.",
                                                            className="topbar-subtitle",
                                                        ),
                                                    ],
                                                ),
                                            ],
                                        ),
                                        html.Div(
                                            className="section-card",
                                            children=DataTable(
                                                id="all-projects-table",
                                                columns=[
                                                    {"name": "واحد سازمانی", "id": "department"},
                                                    {"name": "مدیر پروژه", "id": "manager"},
                                                    {"name": "نام پروژه", "id": "project_name"},
                                                    {"name": "تاریخ شروع", "id": "start_date"},
                                                    {"name": "وضعیت", "id": "status"},
                                                    {"name": "امتیاز", "id": "score"},
                                                ],
                                                data=df.to_dict("records"),
                                                row_selectable=False,
                                                cell_selectable=False,
                                                **base_table_style,
                                            ),
                                        ),
                                    ],
                                ),
                                # Tasks page (status-focused)
                                html.Div(
                                    id="tasks-content",
                                    className="main-card",
                                    style={"display": "none"},
                                    children=[
                                        html.Div(
                                            className="topbar",
                                            children=[
                                                html.Div(
                                                    className="topbar-title",
                                                    children=[
                                                        html.H2(
                                                            "وضعیت پروژه‌ها",
                                                            className="topbar-heading",
                                                        ),
                                                        html.P(
                                                            "نمایی از تعداد پروژه‌ها بر اساس وضعیت اجرا.",
                                                            className="topbar-subtitle",
                                                        ),
                                                    ],
                                                ),
                                            ],
                                        ),
                                        html.Div(
                                            className="section-card",
                                            children=DataTable(
                                                id="status-summary-table",
                                                columns=[
                                                    {"name": "وضعیت", "id": "status"},
                                                    {"name": "تعداد پروژه‌ها", "id": "project_count"},
                                                ],
                                                data=(
                                                    df.groupby("status")
                                                    .agg(project_count=("project_name", "count"))
                                                    .reset_index()
                                                ).to_dict("records"),
                                                row_selectable=False,
                                                cell_selectable=False,
                                                **base_table_style,
                                            ),
                                        ),
                                    ],
                                ),
                                # Members page
                                html.Div(
                                    id="members-content",
                                    className="main-card",
                                    style={"display": "none"},
                                    children=[
                                        html.Div(
                                            className="topbar",
                                            children=[
                                                html.Div(
                                                    className="topbar-title",
                                                    children=[
                                                        html.H2(
                                                            "مدیران پروژه",
                                                            className="topbar-heading",
                                                        ),
                                                        html.P(
                                                            "لیست مدیران پروژه به همراه واحد و عملکرد آن‌ها.",
                                                            className="topbar-subtitle",
                                                        ),
                                                    ],
                                                ),
                                            ],
                                        ),
                                        html.Div(
                                            className="section-card",
                                            children=DataTable(
                                                id="managers-summary-table",
                                                columns=[
                                                    {"name": "مدیر پروژه", "id": "manager"},
                                                    {"name": "واحد سازمانی", "id": "department"},
                                                    {"name": "تعداد پروژه‌ها", "id": "project_count"},
                                                    {"name": "میانگین امتیاز", "id": "avg_score"},
                                                ],
                                                data=(
                                                    df.groupby(["manager", "department"])
                                                    .agg(
                                                        project_count=("project_name", "count"),
                                                        avg_score=("score", "mean"),
                                                    )
                                                    .reset_index()
                                                    .assign(avg_score=lambda d: d["avg_score"].round(1))
                                                ).to_dict("records"),
                                                row_selectable=False,
                                                cell_selectable=False,
                                                **base_table_style,
                                            ),
                                        ),
                                    ],
                                ),
                                # Settings page (simple visual settings description)
                                html.Div(
                                    id="settings-content",
                                    className="main-card",
                                    style={"display": "none"},
                                    children=[
                                        html.Div(
                                            className="topbar",
                                            children=[
                                                html.Div(
                                                    className="topbar-title",
                                                    children=[
                                                        html.H2(
                                                            "تنظیمات داشبورد",
                                                            className="topbar-heading",
                                                        ),
                                                        html.P(
                                                            "برخی تنظیمات پیشنهادی ظاهری و نمایشی برای این داشبورد نمونه.",
                                                            className="topbar-subtitle",
                                                        ),
                                                    ],
                                                ),
                                            ],
                                        ),
                                        html.Div(
                                            className="section-card",
                                            children=[
                                                html.P(
                                                    "این نسخه‌ی نمونه است؛ در یک نسخه‌ی واقعی، می‌توانید از این بخش برای تغییر بازه‌ی زمانی پیش‌فرض، فیلتر واحدها، و تنظیمات تم گراف‌ها استفاده کنید.",
                                                    className="card-caption mb-2",
                                                ),
                                                html.Ul(
                                                    [
                                                        html.Li("بازه‌ی زمانی پیش‌فرض نمودارها: «هفته جاری»."),
                                                        html.Li("حالت نمایش: راست‌به‌چپ برای زبان فارسی."),
                                                        html.Li("تم رنگی ملایم برای نمودارها و کارت‌ها."),
                                                    ],
                                                    style={"fontSize": "13px", "color": "#4b5563"},
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                )
            ],
        ),
    ],
)


# ---------- Callbacks ----------
@app.callback(
    Output("nav-overview", "className"),
    Output("nav-projects", "className"),
    Output("nav-tasks", "className"),
    Output("nav-members", "className"),
    Output("nav-settings", "className"),
    Output("overview-content", "style"),
    Output("projects-content", "style"),
    Output("tasks-content", "style"),
    Output("members-content", "style"),
    Output("settings-content", "style"),
    Input("nav-overview", "n_clicks"),
    Input("nav-projects", "n_clicks"),
    Input("nav-tasks", "n_clicks"),
    Input("nav-members", "n_clicks"),
    Input("nav-settings", "n_clicks"),
)
def switch_page(overview_clicks, projects_clicks, tasks_clicks, members_clicks, settings_clicks):
    ctx = dash.callback_context
    active_id = "nav-overview"
    if ctx.triggered:
        active_id = ctx.triggered[0]["prop_id"].split(".")[0] or "nav-overview"

    base_class = "sidebar-item"

    def cls(item_id):
        return f"{base_class} active" if item_id == active_id else base_class

    overview_style = {"display": "block"} if active_id == "nav-overview" else {"display": "none"}
    projects_style = {"display": "block"} if active_id == "nav-projects" else {"display": "none"}
    tasks_style = {"display": "block"} if active_id == "nav-tasks" else {"display": "none"}
    members_style = {"display": "block"} if active_id == "nav-members" else {"display": "none"}
    settings_style = {"display": "block"} if active_id == "nav-settings" else {"display": "none"}

    return (
        cls("nav-overview"),
        cls("nav-projects"),
        cls("nav-tasks"),
        cls("nav-members"),
        cls("nav-settings"),
        overview_style,
        projects_style,
        tasks_style,
        members_style,
        settings_style,
    )


@app.callback(
    Output("dept-managers-section", "style"),
    Output("dept-managers-table", "data"),
    Output("dept-hint-text", "children"),
    Output("selected-department", "data"),
    Input("projects-per-dept-bar", "clickData"),
    State("dept-managers-section", "style"),
)
def update_managers_table(click_data, current_style):
    style = dict(current_style or {})
    if not click_data or "points" not in click_data or not click_data["points"]:
        style["display"] = "none"
        return (
            style,
            [],
            "برای مشاهده مدیران، روی نوار واحد سازمانی در نمودار بالا کلیک کنید.",
            None,
        )

    selected_department = click_data["points"][0]["x"]

    filtered = df[df["department"] == selected_department]
    if filtered.empty:
        style["display"] = "none"
        return (
            style,
            [],
            "برای این واحد، داده‌ای ثبت نشده است.",
            None,
        )

    managers_summary = (
        filtered.groupby("manager")
        .agg(
            project_count=("project_name", "count"),
            avg_score=("score", "mean"),
        )
        .reset_index()
    )
    managers_summary["avg_score"] = managers_summary["avg_score"].round(1)

    data = managers_summary.to_dict("records")
    style["display"] = "block"
    hint = f"واحد انتخاب‌شده: {selected_department} — برای مشاهده جزئیات، روی نام مدیر کلیک کنید."

    return style, data, hint, selected_department


@app.callback(
    Output("manager-projects-section", "style"),
    Output("manager-projects-table", "data"),
    Output("manager-hint-text", "children"),
    Input("dept-managers-table", "active_cell"),
    State("dept-managers-table", "data"),
    State("selected-department", "data"),
    State("manager-projects-section", "style"),
)
def update_manager_projects_table(active_cell, table_data, selected_department, current_style):
    style = dict(current_style or {})

    if not active_cell or table_data is None or selected_department is None:
        style["display"] = "none"
        return (
            style,
            [],
            "برای مشاهده جزئیات یک مدیر، روی نام او در جدول بالا کلیک کنید.",
        )

    row_index = active_cell.get("row")
    if row_index is None or row_index >= len(table_data):
        style["display"] = "none"
        return (
            style,
            [],
            "انتخاب نامعتبر است؛ لطفاً مجدداً یکی از مدیران را انتخاب کنید.",
        )

    selected_manager = table_data[row_index].get("manager")
    if not selected_manager:
        style["display"] = "none"
        return (
            style,
            [],
            "برای مشاهده جزئیات یک مدیر، روی نام او در جدول بالا کلیک کنید.",
        )

    subset = df[
        (df["department"] == selected_department) & (df["manager"] == selected_manager)
    ][["project_name", "start_date", "status", "score"]].copy()

    if subset.empty:
        style["display"] = "none"
        return (
            style,
            [],
            "برای این مدیر در واحد انتخاب‌شده، پروژه فعالی ثبت نشده است.",
        )

    style["display"] = "block"
    hint = f"مدیر انتخاب‌شده: {selected_manager} — تعداد پروژه‌ها: {len(subset)}"

    return style, subset.to_dict("records"), hint


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8050"))
    app.run(host="0.0.0.0", port=port, debug=True)

