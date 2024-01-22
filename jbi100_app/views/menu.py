from dash import dcc, html
import plotly.express as px
colorscales = px.colors.named_colorscales()

def generate_description_card():
    """

    :return: A Div containing dashboard title & descriptions.
    """
    return html.Div(
        id="description-card",
        children=[
            html.H5("Football manager 2024"),
            html.Div(
                id="intro",
                children="Use these visualizations so your team wins!",
            ),
        ],
    )


def generate_control_card():
    """

    :return: A Div containing controls for graphs.
    """
    return html.Div(
        id="control-card",
        children=[
            html.Label("Color heatmap"),
            dcc.Dropdown(
                id="select-color-heatmap",
                options=colorscales,
                value='viridis',
            ),
            html.Br(),
            html.Label("Color scatterplot 2"),
            dcc.Dropdown(
                id="select-color-scatter-2",
                options=   1,
                value=colorscales[0],
            ),
        ], style={"textAlign": "float-left"}
    )


def make_menu_layout():
    return [generate_description_card(), generate_control_card()]
