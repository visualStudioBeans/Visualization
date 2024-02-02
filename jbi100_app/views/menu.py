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
            html.H5("Soccer formation manager"),
        ],
    )


def generate_control_card(all_formations):
    """

    :return: A Div containing controls for graphs.
    """
    return html.Div(
        id="control-card",
        children=[
            html.Label("Tool Explanation:", style={'margin-top': '15px', 'margin-bottom': '10px'}),
            dcc.Markdown(
            """
            This is the Soccer formation manager. Here you can find information about how well a formation performs. In this menu you can select 
            your formation, the opponents formation, the minimum number of matches a formation has to have to be shown in the graphs, and the color scheme of the tool.
            """
            ),
            html.Label("Select formation:", style={'margin-bottom': '10px', 'margin-top' : '15px'}),
            dcc.Dropdown(
                id="select-team-formation",
                options=[{'label': formation, 'value': formation} for formation in all_formations],
                value=all_formations['Unique_Formation'].tolist()[0],
                persistence=True, 
                ),
            html.Label("Select opponent formation:", style={'margin-top': '15px','margin-bottom': '10px'}),
            dcc.Dropdown(
                id="select-opponent-team-formation",
                options=[{'label': formation, 'value': formation} for formation in all_formations],
                value=all_formations['Unique_Formation'].tolist()[0],
                persistence=True,
                ),
            html.Label("Select minimum matches played by formations:", style={'margin-top': '15px', 'margin-bottom': '10px'}),
            html.Div(
                id="slider",
                className="slider",
                children=dcc.Slider(0, 2000, 50,
                    id="select-minimum-matches-played",
                    marks={
                        0: {'label': '0'},
                        500: {'label': '500'},
                        1000: {'label': '1000'},
                        2000: {'label': '2000'},
                    },
                    value=500,
                    updatemode='mouseup',
                    persistence=True, 
                    tooltip={"placement": "bottom", "always_visible": True},
                    ),
                ),
            html.Label("Select color:", style={'margin-top': '15px', 'margin-bottom': '10px'}),
            dcc.Dropdown(
                id="select-color",
                options=colorscales,
                value=colorscales[0],
                persistence=True,
            ),
        ], style={"textAlign": "float-left"}
    )


def make_menu_layout(all_formations):
    return [generate_description_card(), generate_control_card(all_formations)]
