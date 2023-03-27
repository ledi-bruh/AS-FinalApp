import numpy as np
import pandas as pd
import plotly.express as px
import requests
from dash import Input, Output, State, dcc, dash_table
from app import app
from src.core.settings import settings


def get_data(token):
    url = f'{settings.backend_url}/ml/train_data'
    response = requests.get(url, headers={'Authorization': f'Bearer {token}'})

    if response.ok:
        return pd.read_json(response.json(), orient='records')
    elif response.status_code == 401:
        return 401
    else:
        return None


@app.callback([Output('train-data-output', 'children'),
               Output('fig-container', 'children')],
              Input('get-train-data-button', 'n_clicks'),
              State('token-store', 'data'))
def get_data_callback(n_clicks, token):
    data = get_data(token)

    if type(data) is int and data == 401:
        return 'Необходимо авторизоваться.', None
    elif data is None:
        return 'Ошибка при загрузке данных. Необходим датасет, для этого обучите модель.', None

    table = dash_table.DataTable(
        data=data.to_dict('records'),
        columns=[{'name': str(col), 'id': str(col)} for col in data.columns],
        style_table={'height': '75vh'},
        style_header={'fontWeight': 'bold'},
        style_cell={
            'textAlign': 'center',
            'min-width': '100px',
            'whiteSpace': 'normal',
        },
        fixed_rows={'headers': True},
    )

    labels, counts = np.unique(data['Borough'], return_counts=True)
    fig_pie = px.pie(
        title='Район, в котором находится застройка',
        values=counts,
        names=labels,
        hole=.3,
    )

    fig_hist = px.histogram(
        data,
        x='TDS #',
        y='Borough',
        color='Borough',
        histfunc='avg',
        labels={'x': 'TDS', 'y': 'Район'},
        title="Средний показатель TDS по районам застройки",
    )

    fig_box = px.box(data['Consumption (GAL)'], y="Consumption (GAL)")

    return table, [dcc.Graph(figure=fig) for fig in (fig_pie, fig_hist, fig_box)]
