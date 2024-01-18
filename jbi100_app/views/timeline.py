from dash import dcc, html
import plotly.express as px
import plotly.figure_factory as ff
import pandas as pd


class Timeline(html.Div):
    def __init__(self, name, formation, df):
        self.html_id = name.lower().replace(" ", "-")
        self.df = df
        self.user_formation = formation

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
        # Filter DataFrame for the selected user formation
        # only counts winning matches right now
        filtered_df = self.df[self.df['winning_formation'].apply(lambda x: self.user_formation in x)]

        # Create histogram with kernel density estimate
        # This can be edited to an figure_factory kernel density plot but i could not figure how yet
        fig = px.histogram(filtered_df, x='date', nbins=30, marginal='box', histnorm='probability',
                           title=f'Kernel Density Plot of {self.user_formation} in Winning Formations')

        fig.update_layout(
            yaxis_title='Probability Density',
            xaxis_title='Date',
            dragmode='select'
        )
        fig.update_xaxes(fixedrange=True)
        fig.update_yaxes(fixedrange=True)
        
        self.children[1].figure = fig
