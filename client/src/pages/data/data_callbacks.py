import requests
from dash import Input, Output, State, dash_table
import pandas as pd
from app import app
from src.core.settings import settings


def get_data(token):
    url = f'{settings.backend_url}/ml/data'
    response = requests.get(url, headers={
        'Authorization': f'Bearer {token}'
    })

    if response.status_code == 200:
        return pd.read_json(response.json(), orient='split')
    elif response.status_code == 401:
        raise Exception('Unauthorized')
    else:
        return None


@app.callback(Output('data-output', 'children'),
              [Input('get-data-button', 'n_clicks')],
              [State('token-store', 'data')])
def get_data_callback(n_clicks, token):
    data = get_data(token)
    
    if data is None:
        return 'Error'
    
    table = dash_table.DataTable(
        data=data.to_dict('records'),
        columns=[{'name': str(col), 'id': str(col)} for col in data.columns]
    )
    
    return table
