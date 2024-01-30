from dash import dcc, html
import plotly.express as px
import numpy as np


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
                html.Label("The selected formation agianst the opponent formation is highlighted.", style={'margin':  '0 7px'}),
                html.Label("If applicable, the best formation against the chosen opponent formation is also highlighted.", style={'margin':  '0 7px'}),
                dcc.Graph(id=self.html_id)
            ],
        )

    def update(self, df, selected_color, selected_formation, selected_opponent_formation):
        color_scale_heatmap = 'gray' if selected_color == 'Grayscale' else 'viridis'
        color_scale_highlight1 = 'black' if selected_color == 'Grayscale' else 'red'
        color_scale_highlight2 = 'white' if selected_color == 'Grayscale' else 'magenta'

        # Create a heatmap using Plotly Express
        fig = px.imshow(df,
                        labels=dict(y="Winning formation", x="Losing formation", color= "Ratio"),
                        color_continuous_scale=color_scale_heatmap,
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

        # Highlight the selected team formation
        x_highlight, y_highlight = self.get_highlight_coordinates(df, selected_formation, selected_opponent_formation)

        fig.add_shape(
            type='rect',
            x0=x_highlight - 0.5,
            x1=x_highlight + 0.5,
            y0=y_highlight - 0.5,
            y1=y_highlight + 0.5,
            line=dict(color=color_scale_highlight1, width=2),
            fillcolor='rgba(0, 0, 0, 0.3)',
        )

        if y_highlight != np.argmin(df.iloc[x_highlight]):
            y_highlight = np.argmin(df.iloc[x_highlight])
            fig.add_shape(
                type='rect',
                x0=x_highlight - 0.5,
                x1=x_highlight + 0.5,
                y0=y_highlight - 0.5,
                y1=y_highlight + 0.5,
                line=dict(color=color_scale_highlight2, width=2),
                fillcolor='rgba(255, 255, 255, 0.3)',
            )

        return fig

    def get_highlight_coordinates(self, df, selected_formation, selected_opponent_formation):
        x_highlight = 1
        y_highlight = 1
        
        try:
            x_highlight = df.columns.get_loc(selected_opponent_formation)
            y_highlight = df.index.get_loc(selected_formation)
        except KeyError:
            # Handle the case when the selected formation is not found in the DataFrame
            pass

        return x_highlight, y_highlight