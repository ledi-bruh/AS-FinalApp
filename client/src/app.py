import dash
import dash_bootstrap_components as dbc

from src.utils.external_assets import FONT_AWESOME, CUSTOM_STYLE
from src.layout.layout import layout


app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True, 
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        FONT_AWESOME,
        CUSTOM_STYLE
    ],
    # meta_tags=[
    #     {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    # ]
)

app.layout = layout
