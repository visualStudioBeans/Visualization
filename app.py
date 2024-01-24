from jbi100_app.main import app
from jbi100_app.views.menu import make_menu_layout
from jbi100_app.views.scatterplot import Scatterplot
from jbi100_app.views.heatmap import Heatmap
from jbi100_app.views.timeline import Timeline
from jbi100_app.views.violinplot import Violinplot
from jbi100_app.views.radarplot import Radarplot 

from dash import html
from dash.dependencies import Input, Output
from jbi100_app import data

if __name__ == '__main__':
    # Create data
    formation_ratios, timeline_data, violin_data, radar_data, all_formations = data.get_data()

    # temp formation for timeline and violinplot
    formation1 = '4-3-3'
    formation2 = '4-4-2'

    # Instantiate custom views
    heatmap1 = Heatmap(name='Formation Ratios Heatmap',df=formation_ratios,feature_y="Winning formation",feature_x= "Losing formation")
    timeline1 = Timeline(name="Formation succes over time", df=timeline_data, all_formations=all_formations)
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

    # Define interactions
    @app.callback(
        Output(heatmap1.html_id, "figure"), [
        Input("select-color-heatmap", "value")]
    )
    def update_heatmap1(selected_color):
        return heatmap1.update(selected_color)
    
    @app.callback(
        Output("select-team-timeline", "options"), 
        Input("select-team-threshold", "value"),
    )
    def update_team_options(selected_threshold):
        possible_formations = all_formations.loc[all_formations['Count'] >= int(selected_threshold)]
        possible_formations = possible_formations['Unique_Formation'].tolist()
        return possible_formations
    
    @app.callback(
        Output("select-team-timeline", "value"), 
        Input("select-team-timeline", "options"), 
    )
    def update_team_options(available_options):
        return available_options[0]

    @app.callback(
        Output(timeline1.html_id, "figure"), 
        Input("select-team-timeline", "value"),
    )
    def update_timeline1(selected_formation):
        return timeline1.update(selected_formation)
    

    app.run_server(debug=False, dev_tools_ui=False)