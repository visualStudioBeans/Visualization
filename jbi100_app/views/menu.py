from dash import dcc, html
import plotly.express as px
colorscales = ['Color', 'Grayscale']
thresholds = [10, 50, 100, 500, 750, 1000, 1500]

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


def generate_control_card(all_formations):
    """

    :return: A Div containing controls for graphs.
    """
    return html.Div(
        id="control-card",
        children=[
            html.Label("Select formation:", style={'margin-bottom': '10px'}),
            dcc.Dropdown(
                id="select-team-formation",
                options=[{'label': formation, 'value': formation} for formation in all_formations],
                value=all_formations['Unique_Formation'].tolist()[0],
                ),
            html.Label("Select minimum matches played by formation:", style={'margin-top': '15px', 'margin-bottom': '10px'}),
            dcc.Slider(0, 2000, 50,
                id="select-minimum-matches-played",
                marks={
                    0: {'label': '0'},
                    100: {'label': '100'},
                    500: {'label': '500'},
                    1000: {'label': '1000'},
                    2000: {'label': '2000'},
                },
                value=100,
                updatemode='mouseup',
                tooltip={"placement": "bottom", "always_visible": True}
            ),
            html.Label("Select color:", style={'margin-top': '15px', 'margin-bottom': '10px'}),
            dcc.Dropdown(
                id="select-color",
                options=colorscales,
                value=colorscales[0],
            ),
        ], style={"textAlign": "float-left"}
    )


def make_menu_layout(all_formations):
    return [generate_description_card(), generate_control_card(all_formations)]
