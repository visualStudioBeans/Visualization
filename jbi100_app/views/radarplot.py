from dash import dcc, html
import plotly.express as px
import pandas as pd

class Radarplot(html.Div):
    # df should have columns {date, home_formation, away_formation, home_goal, home_corner, home_cross, home_possession, away_goal, away_corner, away_cross, away_possession}
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

        combined_df = pd.concat([clean_df1, clean_df2], keys=[self.formation1, self.formation2])

        fig = px.line_polar(combined_df,
                            r=['goal', 'corner', 'cross', 'possession'],
                            #theta=combined_df.index.get_level_values(0),
                            line_close=True,
                            #range_r=[0, max(combined_df[['goal', 'corner', 'cross', 'possession']].max())],
                            title="Comparison of Formations",
                            )

        self.children[1].figure = fig

    def _create_clean_df(self, filter_df, formation):
        clean_df = pd.DataFrame({
            'formation': formation,
            'goal': filter_df.apply(lambda row: row['home_goal'] if row['home_formation'] == formation else row['away_goal'], axis=1),
            'corner': filter_df.apply(lambda row: row['home_corner'] if row['home_formation'] == formation else row['away_corner'], axis=1),
            'cross': filter_df.apply(lambda row: row['home_cross'] if row['home_formation'] == formation else row['away_cross'], axis=1),
            'possession': filter_df.apply(lambda row: row['home_possession'] if row['home_formation'] == formation else row['away_possession'], axis=1),
        })

        return clean_df