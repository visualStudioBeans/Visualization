from dash import dcc, html
import plotly.express as px

class Timeline(html.Div):
    def __init__(self, name, df, all_formations):
        self.html_id = name.lower().replace(" ", "-")
        self.df = df
      
        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card",
            children=[
                html.H6(name),
                dcc.Graph(id=self.html_id)
            ]
        )

    def update(self, selected_formation, selected_color):
        if (selected_color == 'Grayscale'):
            selected_color = ['gray']
        else:
            selected_color = ['teal']
        print(selected_color)
        # Filter DataFrame for the selected user formation
        # only counts winning matches right now
        filtered_df = self.df[self.df['winning_formation'].apply(lambda x: selected_formation in x)]

        # Create histogram with kernel density estimate
        # This can be edited to an figure_factory kernel density plot but i could not figure how yet
        fig = px.histogram(filtered_df, x='date', nbins=30, marginal='box', histnorm='probability', color_discrete_sequence=selected_color)

        fig.update_layout(
            yaxis_title='Probability Density',
            xaxis_title='Date',
            dragmode='select'
        )
        fig.update_xaxes(fixedrange=True)
        fig.update_yaxes(fixedrange=True)
        
        return fig
