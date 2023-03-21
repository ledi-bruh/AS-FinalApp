import numpy as np
import pandas as pd
import plotly.express as px
import requests
from dash import Input, Output, State, dash_table
from dash.exceptions import PageError
from app import app
from src.core.settings import settings


def get_data(token):
    url = f'{settings.backend_url}/ml/train_data'
    response = requests.get(url, headers={'Authorization': f'Bearer {token}'})

    if response.status_code == 200:
        return pd.read_json(response.json(), orient='records')
    elif response.status_code == 401:
        raise PageError('Unauthorized')
    else:
        return None


@app.callback([Output('train-data-output', 'children'),
               Output('pie', 'figure'),
               Output('hist', 'figure'),
               Output('box', 'figure'),],
              Input('get-train-data-button', 'n_clicks'),
              State('token-store', 'data'))
def get_data_callback(n_clicks, token):
    data = get_data(token)
    
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
    fig_pie = px.pie(title='Район, в котором находится застройка', values=counts, names=labels, hole=.3)
    
    labels, counts = np.unique(data['TDS #'], return_counts=True)
    fig_hist = px.histogram(
        title='Распределение TDS (Общее количество растворенных твердых веществ)',
        x=labels,
        y=counts,
        labels={'x':'TDS'},
        # histfunc='avg',
    )
    
    fig_box = px.box(data['Consumption (GAL)'], y="Consumption (GAL)")
    
    return table, fig_pie, fig_hist, fig_box
