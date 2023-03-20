from dash import html, Input, Output
import dash_bootstrap_components as dbc
from app import app
from src.utils.constants import home_page_location, auth_page_location, data_page_location, ml_page_location
from src.pages.home import home
from src.pages.auth import auth
from src.pages.data import data
from src.pages.ml import ml


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    path_map = {
        home_page_location: home.layout,
        auth_page_location: auth.layout,
        data_page_location: data.layout,
        ml_page_location: ml.layout,
    }

    if (layout := path_map.get(pathname)):
        return layout

    return dbc.Container(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognized..."),
        ]
    )
