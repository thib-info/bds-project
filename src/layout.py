from dash import dcc
import dash_bootstrap_components as dbc
from dash import html
import src.charts as charts


def get_app_description():
    description_text = """
    Add the description of the project here
    """
    return dcc.Markdown(children=description_text)


def get_data_insights():
    insights = """
    Write potential conclusion here
    """
    return dcc.Markdown(children=insights)


def get_source_text():
    # TODO: Insert the real source here
    source_text = """
    Data from [Inside Airbnb](http://insideairbnb.com/get-the-data.html),
    licensed under [Creative Commons Attribution 4.0 International
    License](https://creativecommons.org/licenses/by/4.0/).
    """
    return dcc.Markdown(children=source_text)


def get_exercise1_charts():
    row = html.Div(
        [
            dbc.Row(
                dbc.Col(html.H2("Data Exploration", style={"margin-top": "1em"})),
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [charts.get_chart_a()],
                    ),
                    dbc.Col(
                        [charts.get_chart_b()],
                    ),
                ],
            ),
        ]
    )

    return row


def get_app_layout():
    return dbc.Container(
        [
            html.H1(children="Inside Airbnb Gent", style={"margin-top": "1rem"}),
            get_app_description(),
            get_exercise1_charts(),
            html.H2(children="Conclusion", style={"margin-top": "1rem"}),
            get_data_insights(),
            dbc.Row(
                [
                    dbc.Col(html.P("Created by Khaled Khaled and Thibault Buze")),
                    dbc.Col(get_source_text(), width="auto"),
                ],
                justify="between",
                style={"margin-top": "3rem"},
            ),
        ],
        fluid=True,
    )
