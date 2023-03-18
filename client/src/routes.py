from dash import html, Input, Output
import dash_bootstrap_components as dbc
from app import app
from src.utils.constants import home_page_location, gdp_page_location, iris_page_location, auth_page_location
from src.pages.home import home
from src.pages.gdp import gdp
from src.pages.iris import iris
from src.pages.auth import auth


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    path_map = {
        home_page_location: home.layout,
        gdp_page_location: gdp.layout,
        iris_page_location: iris.layout,
        auth_page_location: auth.layout,
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