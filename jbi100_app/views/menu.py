from dash import dcc, html
import plotly.express as px
colorscales = ['ice', 'gray']
thresholds = [1, 10, 25, 50, 100, 250, 500, 1000]

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
            html.Label("Select formation:"),
            dcc.Dropdown(
                id="select-team-formation",
                options=[{'label': formation, 'value': formation} for formation in all_formations],
                value=all_formations['Unique_Formation'].tolist()[0],
                ),
            html.Label("Select minimum matches played by formation:", style={'margin-top': '15px'}),
            dcc.Dropdown(
                id="select-minimum-matches-played",
                options=[{'label': str(threshold), 'value': threshold} for threshold in thresholds],
                value=thresholds[4],
            ),
            html.Label("Color heatmap", style={'margin-top': '15px'}),
            dcc.Dropdown(
                id="select-color-heatmap",
                options=colorscales,
                value=colorscales[0],
            ),
        ], style={"textAlign": "float-left"}
    )


def make_menu_layout(all_formations):
    return [generate_description_card(), generate_control_card(all_formations)]
