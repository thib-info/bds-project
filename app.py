"""
Template for BDS Visualization Lab 2022. 
Run with 
$ python app.py

and open http://127.0.0.1:8051/

If you have problems because there is a warning that port 8051 is still in use, just change the port in run_server

"""

import dash
from dash import html
import dash_bootstrap_components as dbc
from src.layout import get_app_layout
from src.callbacks import register_callbacks

# choose your own theme here: https://bootswatch.com/default/
app = dash.Dash(external_stylesheets=[dbc.themes.MINTY])
app.title = "Big Data Science final project"
app.layout = html.Div(get_app_layout())
register_callbacks(app)


if __name__ == "__main__":
    app.run_server(
        debug=True, port=8051, dev_tools_hot_reload=True, use_reloader=True
    )

