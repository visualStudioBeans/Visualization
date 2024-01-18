from dash import dcc, html
import plotly.express as px

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

    def update(self):
        fig = px.histogram(
            self.df,
            x=self.formation,
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
            xaxis_title=self.formation,
            yaxis_title='Density',
            showlegend=False
        )

        return fig
