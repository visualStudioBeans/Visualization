from dash import dcc, html
import plotly.express as px

class Heatmap(html.Div):
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

    def update(self, df, selected_color):
        if (selected_color == 'Grayscale'):
            selected_color = 'gray'
        else:
            selected_color = 'viridis'

        # Create a heatmap using Plotly Express
        fig = px.imshow(df,
                        labels=dict(y="Winning formation", x="Losing formation", color= "Ratio"),
                        color_continuous_scale=selected_color,
                        text_auto=True)
        
        fig.update_layout(
            xaxis_title=self.feature_x,
            yaxis_title=self.feature_y,
            coloraxis_colorbar=dict(title="Ratio"),
            width=900,
            height=600,
        )

        # Update x-axis and y-axis to show all labels
        fig.update_xaxes(tickangle=45, tickmode='array', tickvals=list(range(len(df.columns))), ticktext=df.columns)
        fig.update_yaxes(tickmode='array', tickvals=list(range(len(df.index))), ticktext=df.index)

        return fig

