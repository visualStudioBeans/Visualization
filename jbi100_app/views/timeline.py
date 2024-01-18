from dash import dcc, html
import plotly.express as px
import pandas as pd

class Timeline(html.Div):
    def __init__(self, name, formation, df):
        self.html_id = name.lower().replace(" ", "-")
        self.df = df
        self.formation = formation

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
        self.df['date'] = pd.to_datetime(self.df['date'])
        # Filter data for the specific formation
        filtered_df = self.df[(self.df['winning_formation'] == self.formation) | (self.df['losing_formation'] == self.formation)]

        # Combine counts for winning and losing formations
        date_counts = filtered_df.groupby('date').size().reset_index(name='count')
        print(date_counts)
        
        fig = px.histogram(
            date_counts,
            x='date',
            marginal='rug',
            nbins=30,
            histnorm='density',
            opacity=0.7,
            color_discrete_sequence=['rgb(200,200,200)']
        )

        fig.update_layout(
            yaxis_zeroline=False,
            xaxis_zeroline=False,
            dragmode='select',
            xaxis_title='Date',
            yaxis_title='Count',
            showlegend=False
        )

        return fig
