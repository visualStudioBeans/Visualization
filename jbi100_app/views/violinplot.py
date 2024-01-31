from dash import dcc, html
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots


class Violinplot(html.Div):
    #df should have columns {date, home_formation, away_formation, home_shot_on, home_shot_off, away_shot_on, away_shot_off}
    def __init__(self, name, df):
        self.html_id = name.lower().replace(" ", "-")
        self.df = df

        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card",
            children=[
                html.H6(name),
                dcc.Graph(id=self.html_id)
            ],
        )

    def update(self, formation1, formation2):

        filter_df1 = self.df[self.df['home_formation'].apply(lambda x: formation1 in x) | 
                            self.df['away_formation'].apply(lambda x: formation1 in x)]

        filter_df2 = self.df[self.df['home_formation'].apply(lambda x: formation2 in x) | 
                            self.df['away_formation'].apply(lambda x: formation2 in x)]
        
        clean_df1 = self._create_clean_df(filter_df1, formation1)
        clean_df2 = self._create_clean_df(filter_df2, formation2)

        combined_df = pd.concat([clean_df1, clean_df2], keys=['DF1', 'DF2'])
        fig = make_subplots(rows=1, cols=4, subplot_titles=['shot_on', 'shot_off', 'shot_on_against', 'shot_off_against'])
        colors = ['blue', 'orange']

        for i, attribute in enumerate(['shot_on', 'shot_off', 'shot_on_against', 'shot_off_against']):
            for j, data in enumerate(['DF1', 'DF2']):
                trace = go.Violin(
                    x=[data] * len(combined_df.loc[data]),  # Create a list of 'data' repeated for each data point
                    y=combined_df.loc[data][attribute],
                    name=attribute,
                    box_visible=True,
                    line_color=colors[j]
                )
                fig.add_trace(trace, row=1, col=i+1)


                fig.update_layout(title_text="Comparison of Formations")

        return fig

    def _create_clean_df(self, filter_df, formation):
        clean_df = pd.DataFrame({
            'formation': formation,
            'shot_on': filter_df.apply(lambda row: row['home_shot_on'] if row['home_formation'] == formation else row['away_shot_on'], axis=1),
            'shot_off': filter_df.apply(lambda row: row['home_shot_off'] if row['home_formation'] == formation else row['away_shot_off'], axis=1),
            'shot_on_against': filter_df.apply(lambda row: row['away_shot_on'] if row['home_formation'] == formation else row['home_shot_on'], axis=1),
            'shot_off_against': filter_df.apply(lambda row: row['away_shot_off'] if row['home_formation'] == formation else row['home_shot_off'], axis=1),
        })

        return clean_df
