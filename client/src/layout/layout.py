from dash import html, dcc

from layout.sidebar.sidebar import sidebar


content = html.Div(id="page-content")

layout = html.Div([
    dcc.Location(id="url"),
    dcc.Store(id='token-store', storage_type='session'),
    sidebar,
    content
])
