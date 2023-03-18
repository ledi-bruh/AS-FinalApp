import requests
from dash import Input, Output, State
from dash.exceptions import PreventUpdate
from app import app
from src.core.settings import settings


def authenticate_user(username: str, password: str):
    url = f'{settings.backend_url}/auth/login'
    data = {
        'username': username,
        'password': password
    }
    response = requests.post(url, data=data)
    response_json: dict = response.json()

    if response.status_code == 200:
        return response_json.get('access_token')
    else:
        return None


@app.callback([Output('access-response', 'children'),
               Output('token-store', 'data')],
              [Input('sign-in-button', 'n_clicks')],
              [State('username-input', 'value'),
               State('password-input', 'value')],
              prevent_initial_call=True)
def authenticate_user_callback(n_clicks, username: str, password: str):
    if n_clicks is None:
        raise PreventUpdate
    token = authenticate_user(username, password)
    if token:
        return 'Successful', token
    else:
        return 'Authentication error', None
