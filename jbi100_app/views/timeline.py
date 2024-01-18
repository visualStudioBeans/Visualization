from dash import dcc, html
import plotly.graph_objects as go

class Timeline(html.Div):
    def __init__(self, name, feature, time_feature, df):
        self.html_id = name.lower().replace(" ", "-")
        self.df = df
        self.feature = feature
        self.time_feature = time_feature

        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card",
            children=[
                html.H6(name),
                dcc.Graph(id=self.html_id)
            ],
        )

    def update(self, selected_color, selected_data):
        self.fig = go.Figure()

        self.fig.add_trace(go.Scatter(
            x=self.df[self.time_feature],
            y=self.df[self.feature],
            mode='markers',
            marker_color='rgb(200,200,200)'
        ))
        self.fig.update_traces(mode='markers', marker_size=10)
        self.fig.update_layout(
            yaxis_zeroline=False,
            xaxis_zeroline=False,
            dragmode='select'
        )
        self.fig.update_xaxes(fixedrange=True)
        self.fig.update_yaxes(fixedrange=True)

        # highlight points with selection from another graph
        if selected_data is None:
            selected_index = self.df.index  # show all
        else:
            selected_index = [  # show only selected indices
                x.get('pointIndex', None)
                for x in selected_data['points']
            ]

        self.fig.data[0].update(
            selectedpoints=selected_index,

            # color of selected points
            selected=dict(marker=dict(color=selected_color)),

            # color of unselected points
            unselected=dict(marker=dict(color='rgb(200,200,200)', opacity=0.9))
        )

        # update axis titles
        self.fig.update_layout(
            xaxis_title=self.time_feature,
            yaxis_title=self.feature,
        )

        return self.fig
