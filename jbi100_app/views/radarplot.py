from dash import dcc, html
import plotly.graph_objects as go

class Radarplot(html.Div):
    # df should have columns {date, home_formation, away_formation, home_goal, home_corner, home_cross, home_possession, away_goal, away_corner, away_cross, away_possession}
    def __init__(self, name, df):
        # Generate a unique HTML ID based on the name
        self.html_id = name.lower().replace(" ", "-")
        self.df = df

        # Informational text to be displayed below the title
        info_text = 'This plot shows general statistics for both formations. They are normalized values.'

        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card_top",
            children=[
                # Display the title (name) and information text
                html.H6([name, html.P(info_text, style={'font-size': '12px', 'color': 'black'})], style={'padding-left' : '.5rem'}),
                # Create a Dash Graph component with a unique ID and some styling
                dcc.Graph(id=self.html_id, style={'margin-top' : '30px'})
            ],
        )

    def update(self, formation1, formation2, selected_color):
        # Determine colors based on selected color mode
        color = ['darkgray', 'black'] if selected_color == 'Grayscale' else ['darkblue', 'mediumseagreen']
        
        # Create a new Plotly figure
        fig = go.Figure()

        # Extract values for the radar chart for each formation
        values1 = self.df[self.df['Formation'] == formation1].values.tolist()[0][1:]
        values1.append(values1[0])
        values2 = self.df[self.df['Formation'] == formation2].values.tolist()[0][1:]
        values2.append(values2[0])

        # Get categories (column names) from the dataframe
        categories = self.df.columns.tolist()[1:]

        # Add traces for each formation
        fig.add_trace(go.Scatterpolar(
            r=values1,
            theta=categories + [categories[0]],
            fill='none',
            line=dict(color=color[0]),
            name=formation1
        ))

        fig.add_trace(go.Scatterpolar(
            r=values2,
            theta=categories + [categories[0]],
            fill='none',
            line=dict(color=color[1]),
            name=formation2
        ))

        # Update layout based on the selected formations
        if formation1 == formation2:
            # Adjust layout for single formation comparison
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100]
                    )
                ),
                margin=dict(l=30, r=30, t=50, b=10),  # Adjust margins
                showlegend=True,
                legend=dict(
                    orientation="h",  # Set legend orientation to horizontal
                    yanchor="top",    # Anchor legend to the top
                ),
                title=f'Compare separate statistics for {formation1} & {formation2}',
            )
        else:
            # Adjust layout for two formations comparison
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100]
                    )
                ),
                margin=dict(l=30, r=30, t=50, b=10),  # Adjust margins
                showlegend=True,
                legend=dict(
                    orientation="h",  # Set legend orientation to horizontal
                    yanchor="top",    # Anchor legend to the top
                ),
                title=f'Formation Comparison: {formation1} vs {formation2}',
            )

        return fig
