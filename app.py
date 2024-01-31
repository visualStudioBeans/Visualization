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
import numpy as np
import pandas as pd

if __name__ == '__main__':
    # Create data
    df_wins_losses, timeline_data, violin_data, radar_data, all_formations = data.get_data()

    # temp formation for timeline and violinplot
    formation1 = '4-3-3'
    formation2 = '4-4-2'

    # Instantiate custom views
    heatmap1 = Heatmap(name='Formation ratios heatmap',df=df_wins_losses,feature_y="Winning formation",feature_x= "Losing formation")
    timeline1 = Timeline(name="Formation succes over time", df=timeline_data, all_formations=all_formations)
    violinplot1 = Violinplot(name="Violen", formation1=formation1, formation2=formation2, df=violin_data)
    radarplot1 = Radarplot(name="Radar plot of different features", df=radar_data)

    app.layout = html.Div(
        id="app-container",
        children=[
            # Left column
            html.Div(
                id="left-column",
                className="three columns",
                children=make_menu_layout(all_formations)
            ),

            # Right column
            html.Div(
                id="right-column-top",
                className="nine columns",
                children=[
                    heatmap1, 
                    radarplot1
                    ],
            ),
            html.Div(
                id="right-column-bottom",
                className="columns",
                children=[
                    timeline1,
                    violinplot1,
                ],
            ),
        ],
    )

    # updates heatmap color + input
    @app.callback(
        Output(heatmap1.html_id, "figure"), [
        Input("select-color", "value"),
        Input("select-minimum-matches-played", "value"),
        Input("select-team-formation", "value"),
        Input("select-opponent-team-formation", "value")
        ]
    )
    def update_heatmap1(selected_color, selected_threshold, selected_formation, selected_opponent_formation):
        selected_threshold = int(selected_threshold)
        sizeswin = df_wins_losses.groupby(['winning_formation']).count()
        sizeslose = df_wins_losses.groupby(['losing_formation']).count()
        sizes = pd.merge(sizeswin, sizeslose,  how="outer", left_index=True, right_index=True)
        sizes['total']  = sizes['losing_formation']+sizes['winning_formation']
        sizes = sizes.sort_values(by='total', ascending=False)
        sizes = sizes[sizes['total']>=int(selected_threshold)]

        # Filter formation pairs by the threshold count
        filtered_data = df_wins_losses[
            df_wins_losses['winning_formation'].isin(sizes.index) &
            df_wins_losses['losing_formation'].isin(sizes.index)
        ]

        # Create a DataFrame to store the ratio of A wins from B to B wins from A
        filtered_counts = filtered_data.groupby(['winning_formation', 'losing_formation']).size().unstack(fill_value=0)
        flipped_counts = np.transpose(filtered_counts)
        total_counts = filtered_counts+flipped_counts
        ratio_df = round(filtered_counts/total_counts,2)
        np.fill_diagonal(ratio_df.values, 0.5)
        ratio_df = ratio_df.fillna(0.5)
        return heatmap1.update(ratio_df, selected_color, selected_formation, selected_opponent_formation)
        
    # filters matches played
    @app.callback(
        Output("select-team-formation", "options"), 
        Output("select-opponent-team-formation", "options"),
        Input("select-minimum-matches-played", "value")
    )
    def update_team_options(selected_threshold):
        sizeswin = df_wins_losses.groupby(['winning_formation']).count()
        sizeslose = df_wins_losses.groupby(['losing_formation']).count()
        sizes = pd.merge(sizeswin, sizeslose,  how="outer", left_index=True, right_index=True)
        sizes['total']  = sizes['losing_formation']+sizes['winning_formation']
        sizes = sizes.sort_values(by='total', ascending=False)
        possible_formations = sizes[sizes['total']>=int(selected_threshold)]
        possible_formations = sorted(possible_formations.index.values.tolist())
        return possible_formations, possible_formations
    
    # sets first formation as default 
    @app.callback(
        Output("select-team-formation", "value"), 
        Output("select-opponent-team-formation", "value"), 
        Input("select-team-formation", "options")
    )
    def update_team_options(available_formations):
        return available_formations[0], available_formations[0]
    
    # updates selected formation for timeline
    @app.callback(
        Output(timeline1.html_id, "figure"), 
        Input("select-team-formation", "value"),
        Input("select-opponent-team-formation", "value"),
        Input("select-color", "value")
    )
    def update_timeline1(selected_formation, selected_opponent_formation, selected_color):
        return timeline1.update(selected_formation,selected_opponent_formation, selected_color)

    @app.callback(
        Output(radarplot1.html_id, "figure"), 
        Input("select-team-formation", "value"),
        Input("select-opponent-team-formation", "value")
    )    
    def update_radarplot(selected_formation, selected_opponent_formation):
        return radarplot1.update(selected_formation, selected_opponent_formation)

    app.run_server(debug=False, dev_tools_ui=False)