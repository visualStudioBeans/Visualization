from dash import dcc, html
import plotly.express as px

class DensityHeatmap(html.Div):
    def __init__(self, name, df, feature_x, feature_y):
        self.html_id = name.lower().replace(" ", "-")
        self.df = df
        self.feature_x = feature_x
        self.feature_y = feature_y

        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card",
            children=[
                html.H6(name),
                dcc.Graph(id=self.html_id)
            ],
        )

        # Initial update
        self.update()

    def update(self):
        # Create a density heatmap using Plotly Express
        fig = px.imshow(self.df)
        fig.update_layout(
            xaxis_title=  self.feature_x,
            yaxis_title=  self.feature_y
        )
        
        fig.update_xaxes(fixedrange=True)
        fig.update_yaxes(fixedrange=True)

        # Update the Graph component with the new figure
        self.children[1].figure = fig