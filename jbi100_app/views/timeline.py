from dash import dcc, html
import plotly.express as px

class Timeline(html.Div):
    def __init__(self, name, df, all_formations):
        self.html_id = name.lower().replace(" ", "-")
        self.df = df
        self.all_formations = all_formations
        thresholds = [1, 10, 25, 50, 100, 250, 500, 1000]
        # Filter rows based on the count threshold
        possible_formations = all_formations.loc[all_formations['Count'] >= thresholds[0]]
        possible_formations = possible_formations['Unique_Formation'].tolist()
      
        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card",
            children=[
                html.H6(name),
                html.Div(
                style={'display': 'grid', 'grid-template-columns': '50% 50%', 'padding': '10px'},
                children=[
                    html.Label("Select match threshold:"),
                    html.Label("Select team:"),
                    dcc.Dropdown(
                        id="select-team-threshold",
                        options=[{'label': str(threshold), 'value': threshold} for threshold in thresholds],
                        value=thresholds[0],
                    ),
                    dcc.Dropdown(
                        id="select-team-timeline",
                        options=[{'label': formation, 'value': formation} for formation in possible_formations],
                        value=possible_formations[0],
                    ),
                    ]
                ),
                dcc.Graph(id=self.html_id)
            ]
        )

    def update(self, selected_formation):
        # Filter DataFrame for the selected user formation
        # only counts winning matches right now
        filtered_df = self.df[self.df['winning_formation'].apply(lambda x: selected_formation in x)]

        # Create histogram with kernel density estimate
        # This can be edited to an figure_factory kernel density plot but i could not figure how yet
        fig = px.histogram(filtered_df, x='date', nbins=30, marginal='box', histnorm='probability')

        fig.update_layout(
            yaxis_title='Probability Density',
            xaxis_title='Date',
            dragmode='select'
        )
        fig.update_xaxes(fixedrange=True)
        fig.update_yaxes(fixedrange=True)
        
        return fig
