from dash import dcc, html
import plotly.express as px
import pandas as pd

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

    def update(self, selected_formation, selected_opponent_formation, selected_color):
        color_scale = ['gray', 'black'] if selected_color == 'Grayscale' else ['green', 'darkblue']
        # Filter DataFrame for the selected user formation
        # only counts winning matches right now
        filtered_df_win = self.df[self.df['winning_formation'].apply(lambda x: selected_formation in x)]
        filtered_df_lose = self.df[self.df['losing_formation'].apply(lambda x: selected_formation in x)]

        # Filter DataFrame for the selected opponent formation
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
        
        if (selected_formation == selected_opponent_formation):
            fig = px.line(merged_df, x='year', y=[selected_formation], 
                    color_discrete_sequence=color_scale, markers=True,
                    labels={'year': 'Year', 'value': 'Win Probability', 'variable': 'Formation'},
                    title=f'Formation Comparison: {selected_formation}')
        else:
            # Merge both win probability DataFrames
            merged_df = pd.merge(merged_df, merged_df_opponent, on='year', how='outer').fillna(0)
            fig = px.line(merged_df, x='year', y=[selected_formation, selected_opponent_formation], 
                    color_discrete_sequence=color_scale, markers=True,
                    labels={'year': 'Year', 'value': 'Win Probability', 'variable': 'Formation'},
                    title=f'Formation Comparison: {selected_formation} vs {selected_opponent_formation}')

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
