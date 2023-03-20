from dash import html, dcc
import dash_bootstrap_components as dbc
from src.pages.ml import ml_callbacks


layout = dbc.Container(
    [
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Выберите файл')
            ]),
            accept='text/csv',
            style={
                'width': '100%',
                'height': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'margin': '1%',
                'display': 'flex',
                'justify-content': 'center',
                'align-items': 'center',
            },
            multiple=False,
        ),
        html.Button(
            'Обучить модель на не предобработанных данных',
            id='fit-prepare-button'
        ),
        html.Div(
            id='ml-status-output',
            style={'margin-top': '1vh'},
        ),
    ]
)
