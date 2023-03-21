from dash import html, dcc
import dash_bootstrap_components as dbc
from src.pages.ml import ml_callbacks


layout = dbc.Container(
    [
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Выберите файл'),
            ]),
            accept='text/csv',
            style={
                'width': '100%',
                'height': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'margin': '0 0 3vh',
                'display': 'flex',
                'justify-content': 'center',
                'align-items': 'center',
            },
            multiple=False,
        ),
        html.Div(className='col', children=[
            html.Div(className='col', children=[
                html.Button(
                    'Обучить модель на не предобработанных данных',
                    id='fit-prepare-button',
                ),
                html.Button(
                    'Получить предсказания на не предобработанных данных',
                    id='predict-prepare-button',
                ),
                html.Button(
                    'Узнать качество модели по не предобработанным данным',
                    id='quality-prepare-button',
                ),
            ]),
            html.Div(className='col', children=[
                html.Button(
                    'Обучить модель на предобработанных данных',
                    id='fit-button',
                ),
                html.Button(
                    'Получить предсказания на предобработанных данных',
                    id='predict-button',
                ),
                html.Button(
                    'Узнать качество модели по предобработанным данным',
                    id='quality-button',
                ),
            ]),
            html.Button(
                'Предобработать данные',
                id='prepare-button',
            ),
        ]),

        html.Div(
            id='ml-status-output',
            style={'margin-top': '1vh'},
        ),
        html.Div([
            html.Pre(
                id='quality-status-output',
                style={'margin-top': '1vh', 'height': 'auto'}
            ),
        ]),
        dcc.Download(
            id='ml-file-download',
        ),
    ]
)
