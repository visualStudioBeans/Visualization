from dash import dcc, html
import plotly.express as px
import pandas as pd

class Timeline(html.Div):
    def __init__(self, name, df, all_formations):
        # Generate a unique HTML ID based on the name
        self.html_id = name.lower().replace(" ", "-")
        self.df = df

        # Informational text to be displayed below the title
        info_text = 'These lines show the win ratio of a formation against all other formations over time.'

        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card_bottom",
            children=[
                # Display the title (name) and information text
                html.H6([name, html.P(info_text, style={'font-size': '12px', 'color': 'black'})], style={'padding-left' : '.5rem'}),
                # Create a Dash Graph component with a unique ID
                dcc.Graph(id=self.html_id)
            ]
        )

    def update(self, selected_formation, selected_opponent_formation, selected_color):
        # Determine colors based on selected color mode
        color = ['darkgray', 'black'] if selected_color == 'Grayscale' else ['darkblue', 'mediumseagreen']

        # Filter DataFrame for the selected user formation (winning and losing matches)
        filtered_df_win = self.df[self.df['winning_formation'].apply(lambda x: selected_formation in x)]
        filtered_df_lose = self.df[self.df['losing_formation'].apply(lambda x: selected_formation in x)]

        # Filter DataFrame for the selected opponent formation (winning and losing matches)
        filtered_df_opponent_win = self.df[self.df['losing_formation'].apply(lambda x: selected_opponent_formation in x)]
        filtered_df_opponent_lose = self.df[self.df['winning_formation'].apply(lambda x: selected_opponent_formation in x)]

        # Extract year from the date column
        filtered_df_win['year'] = pd.to_datetime(filtered_df_win['date']).dt.year
        filtered_df_lose['year'] = pd.to_datetime(filtered_df_lose['date']).dt.year
        filtered_df_opponent_win['year'] = pd.to_datetime(filtered_df_opponent_win['date']).dt.year
        filtered_df_opponent_lose['year'] = pd.to_datetime(filtered_df_opponent_lose['date']).dt.year

        # Group by year and count wins and losses
        wins_per_year = filtered_df_win.groupby('year').size().reset_index(name='wins')
        losses_per_year = filtered_df_lose.groupby('year').size().reset_index(name='losses')
        opponent_wins_per_year = filtered_df_opponent_win.groupby('year').size().reset_index(name='opponent_wins')
        opponent_losses_per_year = filtered_df_opponent_lose.groupby('year').size().reset_index(name='opponent_losses')

        # Merge DataFrames on 'year' column
        merged_df = pd.merge(wins_per_year, losses_per_year, on='year', how='outer').fillna(0)
        merged_df_opponent = pd.merge(opponent_wins_per_year, opponent_losses_per_year, on='year', how='outer').fillna(0)

        # Calculate win probability
        merged_df[selected_formation] = round(merged_df['wins'] / (merged_df['wins'] + merged_df['losses']), 2)
        merged_df_opponent[selected_opponent_formation] = round(merged_df_opponent['opponent_wins'] / (merged_df_opponent['opponent_wins'] + merged_df_opponent['opponent_losses']), 2)

        # Create a Plotly figure based on selected formations
        if (selected_formation == selected_opponent_formation):
            # Create a line chart for a single formation
            fig = px.line(merged_df, x='year', y=[selected_formation], 
                    color_discrete_sequence=color, markers=True,
                    labels={'year': 'Year', 'value': 'Win Probability', 'variable': 'Formation'})
        else:
            # Merge both win probability DataFrames for a comparison
            merged_df = pd.merge(merged_df, merged_df_opponent, on='year', how='outer').fillna(0)
            # Create a line chart for two formations comparison
            fig = px.line(merged_df, x='year', y=[selected_formation, selected_opponent_formation], 
                    color_discrete_sequence=color, markers=True,
                    labels={'year': 'Year', 'value': 'Win Probability', 'variable': 'Formation'})

        # Update layout
        fig.update_layout(
            yaxis=dict(range=[0, 1]),
            dragmode='select',
            xaxis_title='Year',
            yaxis_title='Win Probability'
        )

        fig.update_xaxes(fixedrange=True)
        fig.update_yaxes(fixedrange=True)

        return fig
