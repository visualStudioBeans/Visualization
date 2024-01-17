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
    formation_ratios = data.get_data()
    
    # Instantiate custom views
    heatmap1 = DensityHeatmap(name='Formation Ratios Heatmap',df=formation_ratios,feature_y="Winning formation",feature_x= "Losing formation")

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

    app.run_server(debug=False, dev_tools_ui=False)