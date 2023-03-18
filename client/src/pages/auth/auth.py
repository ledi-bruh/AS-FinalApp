from dash import html, dcc
import dash_bootstrap_components as dbc
from src.pages.auth import auth_callbacks


layout = dbc.Container(
    [
        dcc.Input(id='username-input', type='text', placeholder='Username'),
        dcc.Input(id='password-input', type='password', placeholder='Password'),
        html.Button('Sign In', id='sign-in-button'),
        html.Div(id='auth-output'),
    ]
)
