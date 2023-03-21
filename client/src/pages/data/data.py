from dash import html, dcc
import dash_bootstrap_components as dbc
from src.pages.data import data_callbacks


layout = dbc.Container(
    [
        html.Button('Получить данные', id='get-train-data-button'),
        html.Div(id='train-data-output', style={'margin-top': '1vh'}),
        html.Div(
            className='fig-container',
            children=[
                dcc.Graph(id='pie'),
                dcc.Graph(id='hist'),
                dcc.Graph(id='box'),
            ],
        )
    ]
)
