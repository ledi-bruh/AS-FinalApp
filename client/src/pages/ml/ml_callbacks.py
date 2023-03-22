import json
import base64
import requests
import pandas as pd
from io import StringIO
from datetime import datetime
from dash import dcc, Input, Output, State, callback_context, no_update
from app import app
from src.core.settings import settings


def now():
    time = datetime.now()
    return time.strftime('%Y:%m:%d %H:%M:%S')


def at_time(func): 
    def wrapper(*args, **kwargs):
        if type(f := func(*args, **kwargs)) is str:
            return f'{now()}: {f}'
        else:
            return f
    return wrapper


def send_file(contents, token, sub_url):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    url = f'{settings.backend_url}/ml/{sub_url}'

    response = requests.post(
        url,
        headers={'Authorization': f'Bearer {token}'},
        files={'file': decoded},
    )

    return response


@app.callback(Output('ml-status-output', 'children'),
              [Input('fit-prepare-button', 'n_clicks'),
               Input('fit-button', 'n_clicks'),],
              [State('upload-data', 'contents'),
               State('token-store', 'data')])
@at_time
def ml_fit_callback(clicks1, clicks2, content, token):
    ctx = callback_context
    if not ctx.triggered:
        return no_update

    if content is None:
        return f'Сначала необходимо выбрать файл с тренировочной выборкой.'

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    info = {
        'fit-prepare-button': {
            'sub_url': 'fit/prepare',
            'ok_msg': 'Данные успешно предобработаны. Модель обучена.',
        },
        'fit-button': {
            'sub_url': 'fit',
            'ok_msg': 'Модель успешно обучена.',
        },
    }

    if (btn := info.get(button_id, False)):
        sub_url, ok_msg = btn['sub_url'], btn['ok_msg']
    else:
        return 'Ошибка.'

    response = send_file(content, token, sub_url)

    if response.status_code == 200:
        return ok_msg
    elif response.status_code == 401:
        return 'Необходимо авторизоваться.'

    return f'Ошибка {response.status_code}.'


@app.callback(Output('quality-status-output', 'children'),
              [Input('quality-prepare-button', 'n_clicks'),
               Input('quality-button', 'n_clicks'),],
              [State('upload-data', 'contents'),
               State('token-store', 'data')])
@at_time
def ml_quality_callback(clicks1, clicks2, content, token):
    ctx = callback_context
    if not ctx.triggered:
        return no_update

    if content is None:
        return 'Загрузить файл с тестовой выборкой можно выше.'

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    info = {
        'quality-prepare-button': {
            'sub_url': 'quality/prepare',
        },
        'quality-button': {
            'sub_url': 'quality',
        },
    }

    if (btn := info.get(button_id, False)):
        sub_url = btn['sub_url']
    else:
        return 'Ошибка.'

    response = send_file(content, token, sub_url)

    if response.status_code == 200:
        return json.dumps(dict(map(lambda x: (x[0], float(f'{x[1]:.4f}')), response.json().items())))
    elif response.status_code == 401:
        return 'Необходимо авторизоваться.'

    return f'Ошибка {response.status_code}.'


@app.callback(Output('ml-file-download', 'data'),
              [Input('predict-prepare-button', 'n_clicks'),
               Input('predict-button', 'n_clicks'),
               Input('prepare-button', 'n_clicks'),],
              [State('upload-data', 'contents'),
               State('token-store', 'data')])
@at_time
def ml_predict_prepare_callback(clicks1, clicks2, clicks3, content, token):
    ctx = callback_context
    if not ctx.triggered:
        return no_update

    if content is None:
        return no_update

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    info = {
        'predict-prepare-button': {
            'sub_url': 'predict/prepare',
            'filename': 'predicted_data',
        },
        'predict-button': {
            'sub_url': 'predict',
            'filename': 'predicted_data',
        },
        'prepare-button': {
            'sub_url': 'prepare',
            'filename': 'prepared_data',
        },
    }

    if (btn := info.get(button_id, False)):
        sub_url, filename = btn['sub_url'], btn['filename']
    else:
        return 'Ошибка.'

    response = send_file(content, token, sub_url)

    if response.status_code == 200:
        df = pd.read_csv(StringIO(response.content.decode(response.encoding)), header=None)
        return dcc.send_data_frame(df.to_csv, filename=f'{filename}.csv', index=False, header=None)
    elif response.status_code == 401:
        return 'Необходимо авторизоваться.'

    return f'Ошибка {response.status_code}.'
