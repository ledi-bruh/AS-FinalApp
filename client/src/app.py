from dash import Dash
from src.layout.base import base_layout


app = Dash(__name__)

app.layout = base_layout
