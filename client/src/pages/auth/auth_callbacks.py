import requests
from dash import Input, Output, State, callback_context, no_update
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

    if response.ok:
        return response_json.get('access_token')
    return None


@app.callback([Output('auth-output', 'children'),
               Output('token-store', 'data'),],
              [Input('sign-in-button', 'n_clicks'),
               Input('sign-out-button', 'n_clicks')],
              [State('username-input', 'value'),
               State('password-input', 'value'),
               State('token-store', 'data'),],
              prevent_initial_call=True)
def authenticate_user_callback(clicks1, clicks2, username, password, token):
    if clicks1 is None and clicks2 is None:
        raise PreventUpdate
    
    ctx = callback_context
    if not ctx.triggered:
        return no_update
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if button_id == 'sign-out-button':
        return 'Вы вышли из аккаунта', None
    
    if (token := authenticate_user(username, password)):
        return 'Вы вошли в аккаунт.', token
    else:
        return 'Ошибка при авторизации.', None


@app.callback(Output('auth-status-output', 'children'),
              Input('auth-status-interval', 'n_intervals'),
              State('token-store', 'data'),)
def authenticate_status_callback(n,  token):
    if token is None:
        return '❌'
    return '✅'
