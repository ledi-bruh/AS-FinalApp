from dash import html, dcc
import dash_bootstrap_components as dbc
from src.pages.data import data_callbacks


layout = dbc.Container(
    [
        html.Button('Обновить', id='get-data-button'),
        html.Div(id='data-output', style={'margin-top': '1vh'}),
    ]
)
