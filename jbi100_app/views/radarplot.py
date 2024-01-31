from dash import dcc, html
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

class Radarplot(html.Div):
    # df should have columns {date, home_formation, away_formation, home_goal, home_corner, home_cross, home_possession, away_goal, away_corner, away_cross, away_possession}
    def __init__(self, name, df):
        self.html_id = name.lower().replace(" ", "-")
        self.df = df

        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card_top",
            children=[
                html.H6(name),
                dcc.Graph(id=self.html_id)
            ],
        )


    def update(self, formation1, formation2):
        
        fig = go.Figure()

        values1=self.df[self.df['Formation']==formation1].values.tolist()[0][1:]
        values1.append(values1[0])
        values2=self.df[self.df['Formation']==formation2].values.tolist()[0][1:]
        values2.append(values2[0])
        categories = self.df.columns.tolist()[1:]

        fig.add_trace(go.Scatterpolar(
            r=values1,
            theta=categories + [categories[0]],
            fill='none',
            line=dict(color='blue')
        ))

        fig.add_trace(go.Scatterpolar(
            r=values2,
            theta=categories + [categories[0]],
            fill='none',
            line=dict(color='orange')
        ))

        # Update layout
        if formation1 == formation2:
            fig.update_layout(
            polar=dict(
                radialaxis=dict(
                visible=True,
                range=[0, 100]
                )),
            showlegend=True,
            title=f'Formation Comparison: {formation1}'
            )
        else:
            fig.update_layout(
            polar=dict(
                radialaxis=dict(
                visible=True,
                range=[0, 100]
                )),
            showlegend=True,
            title=f'Formation Comparison: {formation1} vs {formation2}',
        margin={"t": 10, "b": 10, "r": 0, "l": 0, "pad": 0},
            )

        return fig

