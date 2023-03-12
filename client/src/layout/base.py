from dash import dcc, html

base_layout = html.Div([
    html.H1('Hello Dash'),
    html.Div([
        html.P('Dash converts Python classes into HTML'),
        html.P("This conversion happens behind the scenes by Dash's JavaScript front-end")
    ], style={'color': 'blue', 'fontSize': 14})
])
