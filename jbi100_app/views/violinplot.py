from dash import dcc, html
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots


class Violinplot(html.Div):
    #df should have columns {date, home_formation, away_formation, home_shot_on, home_shot_off, away_shot_on, away_shot_off}
    def __init__(self, name, formation1, formation2, df):
        self.html_id = name.lower().replace(" ", "-")
        self.df = df
        self.formation1 = formation1
        self.formation2 = formation2

        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card",
            children=[
                html.H6(name),
                dcc.Graph(id=self.html_id)
            ],
        )

        self.update()

    def update(self):

        filter_df1 = self.df[self.df['home_formation'].apply(lambda x: self.formation1 in x) | 
                            self.df['away_formation'].apply(lambda x: self.formation1 in x)]

        filter_df2 = self.df[self.df['home_formation'].apply(lambda x: self.formation2 in x) | 
                            self.df['away_formation'].apply(lambda x: self.formation2 in x)]
        
        clean_df1 = self._create_clean_df(filter_df1, self.formation1)
        clean_df2 = self._create_clean_df(filter_df2, self.formation2)

        combined_df = pd.concat([clean_df1, clean_df2], keys=['DF1', 'DF2'])
        fig = make_subplots(rows=1, cols=4, subplot_titles=['shot_on', 'shot_off', 'shot_on_against', 'shot_off_against'])

        for i, attribute in enumerate(['shot_on', 'shot_off', 'shot_on_against', 'shot_off_against']):
            trace = go.Violin(x=combined_df.index.get_level_values(0), y=combined_df[attribute], name=attribute, box_visible=True, line_color='blue')
            fig.add_trace(trace, row=1, col=i+1)

        fig.update_layout(title_text="Comparison of Formations")

        self.children[1].figure = fig

    def _create_clean_df(self, filter_df, formation):
        clean_df = pd.DataFrame({
            'formation': formation,
            'shot_on': filter_df.apply(lambda row: row['home_shot_on'] if row['home_formation'] == formation else row['away_shot_on'], axis=1),
            'shot_off': filter_df.apply(lambda row: row['home_shot_off'] if row['home_formation'] == formation else row['away_shot_off'], axis=1),
            'shot_on_against': filter_df.apply(lambda row: row['away_shot_on'] if row['home_formation'] == formation else row['home_shot_on'], axis=1),
            'shot_off_against': filter_df.apply(lambda row: row['away_shot_off'] if row['home_formation'] == formation else row['home_shot_off'], axis=1),
        })

        return clean_df
