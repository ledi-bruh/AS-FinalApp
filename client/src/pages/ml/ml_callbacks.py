import json
import base64
import requests
from dash import Input, Output, State, callback_context, no_update
from app import app
from src.core.settings import settings


def send_file(contents, token, sub_url):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    url = f'{settings.backend_url}/ml/{sub_url}'
    
    response = requests.post(url,
        headers={'Authorization': f'Bearer {token}'},
        files={'file': decoded},
    )
    
    return response


@app.callback(Output('ml-status-output', 'children'),
              [Input('fit-prepare-button', 'n_clicks'),
               Input('predict-prepare-button', 'n_clicks'),
               Input('fit-button', 'n_clicks'),
               Input('predict-button', 'n_clicks'),
               Input('prepare-button', 'n_clicks'),],
              [State('upload-data', 'contents'),
               State('token-store', 'data')])
def ml_callback(clicks1, clicks2, clicks3, clicks4, clicks5, content, token):
    ctx = callback_context
    if not ctx.triggered:
        return no_update
    
    if content is None:
        return 'Сначала необходимо выбрать файл.'
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    info = {
        'fit-prepare-button': {
            'sub_url': 'fit/prepare',
            'ok_msg': 'Данные успешно предобработаны. Модель обучена.',
        },
        'predict-prepare-button': {
            'sub_url': 'predict/prepare',
            'ok_msg': 'Данные успешно предобработаны и предсказаны.',
        },
        'fit-button': {
            'sub_url': 'fit',
            'ok_msg': 'Модель успешно обучена.',
        },
        'predict-button': {
            'sub_url': 'predict',
            'ok_msg': '3',
        },
        'prepare-button': {
            'sub_url': 'prepare',
            'ok_msg': '5',
        },
    }
    
    if (btn := info.get(button_id, False)):
        sub_url, ok_msg = btn['sub_url'], btn['ok_msg']
    else:
        return 'Ошибка'

    response = send_file(content, token, sub_url)
    
    
    if response.status_code == 200:
        print(response.json() is None)
        print(response.content.decode() is None)
        return ok_msg
        return {'ok_msg': ok_msg, 'json': response.json(), 'content': response.content}
    elif response.status_code == 401:
        return 'Необходимо авторизоваться'
    return f'{response.status_code}'


@app.callback(Output('quality-status-output', 'children'),
              [Input('quality-prepare-button', 'n_clicks'),
               Input('quality-button', 'n_clicks'),],
              [State('upload-data', 'contents'),
               State('token-store', 'data')])
def ml_callback(clicks1, clicks2, content, token):
    ctx = callback_context
    if not ctx.triggered:
        return no_update
    
    if content is None:
        return 'Сначала необходимо выбрать файл.'
    
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
        return 'Ошибка'

    response = send_file(content, token, sub_url)
    
    if response.status_code == 200:
        return json.dumps(dict(map(lambda x: (x[0], float(f'{x[1]:.4f}')), response.json().items())))
    elif response.status_code == 401:
        return 'Необходимо авторизоваться'
    
    return f'{response.status_code}'
