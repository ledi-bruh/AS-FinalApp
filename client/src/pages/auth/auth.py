from dash import html, dcc
import dash_bootstrap_components as dbc
from src.pages.auth import auth_callbacks


layout = dbc.Container(
    [
        dcc.Input(id='username-input', type='text', placeholder='Username'),
        dcc.Input(id='password-input', type='password', placeholder='Password'),
        html.Button('Sign in', id='sign-in-button'),
        html.Button('Sign out', id='sign-out-button'),
        html.Div(id='auth-output'),
        html.Div(id='auth-status-output'),
        dcc.Interval(
            id='auth-status-interval',
            interval=1000,
            n_intervals=0
        )
    ]
)
