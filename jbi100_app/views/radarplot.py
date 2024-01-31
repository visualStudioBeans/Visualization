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
                dcc.Graph(id=self.html_id, style={'margin-top' : '30px'})
            ],
        )


    def update(self, formation1, formation2, selected_color):
        color = ['darkgray', 'black'] if selected_color == 'Grayscale' else ['darkblue', 'gold']
        
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
            line=dict(color=color[0])
        ))

        fig.add_trace(go.Scatterpolar(
            r=values2,
            theta=categories + [categories[0]],
            fill='none',
            line=dict(color=color[1])
        ))

        # Update layout
        if formation1 == formation2:
            fig.update_layout(
            polar=dict(
                radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
            margin=dict(l=30, r=30, t=50, b=10),  # Adjust margins
            showlegend=True,
            legend=dict(
                orientation="h",  # Set legend orientation to horizontal
                yanchor="top",    # Anchor legend to the top
            ),
            title=f'Formation Comparison: {formation1}',
            )
        else:
            fig.update_layout(
            polar=dict(
                radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
            margin=dict(l=30, r=30, t=50, b=10),  # Adjust margins
            showlegend=True,
            legend=dict(
                orientation="h",  # Set legend orientation to horizontal
                yanchor="top",    # Anchor legend to the top
            ),
            title=f'Formation Comparison: {formation1} vs {formation2}',
            )

        return fig

