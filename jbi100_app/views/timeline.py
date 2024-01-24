from dash import dcc, html
import plotly.express as px

class Timeline(html.Div):
    def __init__(self, name, df, all_formations):
        self.html_id = name.lower().replace(" ", "-")
        self.df = df
        self.all_formations = all_formations['Unique_Formation'].tolist()
      
        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card",
            children=[
                html.H6(name),
                html.Div(
                style={'display': 'grid', 'padding': '10px'},
                children=[
                    html.Label("Select team:"),
                    dcc.Dropdown(
                        id="select-team-timeline",
                        options=[{'label': formation, 'value': formation} for formation in self.all_formations],
                        value=self.all_formations[0],
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
