from jbi100_app.main import app
from jbi100_app.views.menu import make_menu_layout
from jbi100_app.views.scatterplot import Scatterplot
from jbi100_app.views.heatmap import DensityHeatmap
from jbi100_app.views.timeline import Timeline
from jbi100_app.views.violinplot import Violinplot
from jbi100_app.views.radarplot import Radarplot 

from dash import dcc, html
import plotly.express as px
from dash.dependencies import Input, Output
from jbi100_app import data

if __name__ == '__main__':
    # Create data
    formation_ratios, timeline_data, violin_data, radar_data = data.get_data()
    
    # temp formation for timeline and violinplot
    formation1 = '3-3-4'
    formation2 = '2-4-4'

    # Instantiate custom views
    heatmap1 = DensityHeatmap(name='Formation Ratios Heatmap',df=formation_ratios,feature_y="Winning formation",feature_x= "Losing formation")
    timeline1 = Timeline(name="Formation succes over time", df=timeline_data, formation=formation1)
    violinplot1 = Violinplot(name="Was een beer", formation1=formation1, formation2=formation2, df=violin_data)
    radarplot1 = Radarplot(name="Was twee beren", formation1=formation1, formation2=formation2, df=radar_data)

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
                    heatmap1,
                    timeline1,
                    violinplot1,
                    radarplot1
                ],
            ),
        ],
    )

    app.run_server(debug=False, dev_tools_ui=False)