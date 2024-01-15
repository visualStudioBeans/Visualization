from jbi100_app.main import app
from jbi100_app.views.menu import make_menu_layout
from jbi100_app.views.scatterplot import Scatterplot
from jbi100_app.views.heatmap import DensityHeatmap

from dash import dcc, html
import plotly.express as px
from dash.dependencies import Input, Output
from jbi100_app import data

if __name__ == '__main__':
    # Create data
    df = px.data.iris()
    df2 = px.data.medals_wide(indexed=True)
    formation_ratios = data.get_data()
    
    # Instantiate custom views
    scatterplot1 = Scatterplot("Scatterplot 1", 'sepal_length', 'sepal_width', df)
    heatmap1 = DensityHeatmap(name='Formation Ratios Heatmap',df=formation_ratios,feature_y="winning_formation",feature_x= "losing_formation")

    app.layout = html.Div(
        id="app-container",
        children=[
            # Left column
            html.Div(
                id="left-column",
                className="three columns",
                children=make_menu_layout()
            ),

            # Right column
            html.Div(
                id="right-column",
                className="nine columns",
                children=[
                    heatmap1
                ],
            ),
        ],
    )

    # Define interactions
    @app.callback(
        Output(scatterplot1.html_id, "figure"), [
        Input("select-color-scatter-1", "value"),
        Input(scatterplot1.html_id, 'selectedData')
    ])
    def update_scatter_1(selected_color, selected_data):
        return scatterplot1.update(selected_color, selected_data)

    app.run_server(debug=False, dev_tools_ui=False)