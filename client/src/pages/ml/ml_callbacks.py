import requests
import base64
from dash import Input, Output, State
from dash.exceptions import PreventUpdate
from app import app
from src.core.settings import settings


def fit_prepare(filename, contents, token):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    url = f'{settings.backend_url}/ml/fit/prepare'
    response = requests.post(url,
        headers={'Authorization': f'Bearer {token}'},
        files={'file': decoded},
    )

    if response.status_code == 200:
        return 'Данные успешно предобработаны. Модель обучена.'
    elif response.status_code == 401:
        return 401
    else:
        return None


@app.callback(Output('ml-status-output', 'children'),
              [Input('fit-prepare-button', 'n_clicks')],
              [State('upload-data', 'filename'),
               State('upload-data', 'contents'),
               State('token-store', 'data')])
def fit_prepare_callback(n_clicks, filename, content, token):
    if n_clicks is None:
        raise PreventUpdate

    answer = fit_prepare(filename, content, token)

    if answer is None:
        return 'Error'
    elif answer == 401:
        return 'Необходимо авторизоваться'

    return answer
