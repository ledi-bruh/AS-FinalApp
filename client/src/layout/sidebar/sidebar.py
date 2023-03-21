import dash_bootstrap_components as dbc
from dash import html
from src.utils.constants import auth_page_location, data_page_location, ml_page_location


sidebar_header = dbc.Row(
    [
        dbc.Col(html.H2("Меню", className="display-4")),
        dbc.Col(
            [
                html.Button(
                    html.Span(className="navbar-toggler-icon"),
                    className="navbar-toggler",
                    id="navbar-toggle",
                ),
                html.Button(
                    html.Span(className="navbar-toggler-icon"),
                    className="navbar-toggler",
                    id="sidebar-toggle",
                ),
            ],
            width="auto",
            align="center",
        ),
    ]
)

sidebar = html.Div(
    [
        sidebar_header,
        html.Hr(),
        dbc.Collapse(
            dbc.Nav(
                [
                    dbc.NavLink("Аккаунт", href=auth_page_location, active="exact"),
                    dbc.NavLink("ML", href=ml_page_location, active="exact"),
                    dbc.NavLink("Датасет", href=data_page_location, active="exact"),
                ],
                vertical=True,
                pills=True,
            ),
            id="collapse",
        ),
    ],
    id="sidebar",
)
