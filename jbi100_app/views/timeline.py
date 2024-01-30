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

    def update(self, selected_formation, selected_color):
        color_scale = ['gray'] if selected_color == 'Grayscale' else ['teal']

        # Filter DataFrame for the selected user formation
        # only counts winning matches right now
        filtered_df_win = self.df[self.df['winning_formation'].apply(lambda x: selected_formation in x)]
        filtered_df_lose = self.df[self.df['losing_formation'].apply(lambda x: selected_formation in x)]

        filtered_df_win['year'] = pd.to_datetime(filtered_df_win['date']).dt.year
        filtered_df_lose['year'] = pd.to_datetime(filtered_df_lose['date']).dt.year

        wins_per_year = filtered_df_win.groupby('year').size().reset_index(name='wins')
        losses_per_year = filtered_df_lose.groupby('year').size().reset_index(name='losses')

        # Merge DataFrames on 'year' column
        merged_df = pd.merge(wins_per_year, losses_per_year, on='year', how='outer').fillna(0)

        # Calculate win probability
        merged_df['win_probability'] = merged_df['wins'] / (merged_df['wins'] + merged_df['losses'])

        fig = px.line(merged_df, x='year', y='win_probability', line_shape='linear', markers=True, color_discrete_sequence=color_scale)

        fig.update_layout(
            yaxis_title='Win Probability',
            xaxis_title='Year',
            dragmode='select',
            yaxis=dict(range=[0, 1]),
            title=f'Formation: {selected_formation}' 
        )
        fig.update_xaxes(fixedrange=True)
        fig.update_yaxes(fixedrange=True)

        return fig
