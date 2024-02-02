from dash import dcc, html
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots


class Violinplot(html.Div):
    # df should have columns {date, home_formation, away_formation, home_shot_on, home_shot_off, away_shot_on, away_shot_off}
    def __init__(self, name, df):
        # Generate a unique HTML ID based on the name
        self.html_id = name.lower().replace(" ", "-")
        self.df = df

        # Informational text to be displayed below the title
        info_text = """These violin plots show the distributions of shots on and off target on both sides for both formations.
        Hover over the violin to get extra information about the distribution."""

        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card_bottom",
            children=[
                # Display the title (name) and information text
                html.H6([name, 
                        html.P(info_text, style={'font-size': '12px', 'color': 'black'})],
                        style={'padding-left' : '.5rem'}),
                # Create a Dash Graph component with a unique ID
                dcc.Graph(id=self.html_id)
            ],
        )

    def update(self, formation1, formation2, selected_color):
        # Determine colors based on selected color mode
        color = ['darkgray', 'black'] if selected_color == 'Grayscale' else ['darkblue', 'mediumseagreen']

        # Filter the dataframe based on selected formations
        filter_df1 = self.df[self.df['home_formation'].apply(lambda x: formation1 in x) | 
                            self.df['away_formation'].apply(lambda x: formation1 in x)]

        filter_df2 = self.df[self.df['home_formation'].apply(lambda x: formation2 in x) | 
                            self.df['away_formation'].apply(lambda x: formation2 in x)]
        
        # Create clean dataframes for each formation
        clean_df1 = self._create_clean_df(filter_df1, formation1)
        clean_df2 = self._create_clean_df(filter_df2, formation2)

        # Combine the two dataframes
        combined_df = pd.concat([clean_df1, clean_df2], keys=['DF1', 'DF2'])

        # Create subplots for each shot category
        fig = make_subplots(rows=1, cols=4, subplot_titles=['shot on target', 'shot off target', 'shot on against', 'shot off against'])

        # Update x-axis ticks for all subplots
        for i in range(1, 5):
            fig.update_xaxes(tickvals=[], ticktext=[], row=1, col=i)

        # Initialize custom legend items
        custom_legend = []

        # Iterate over shot categories and formations to add Violin plots
        for i, attribute in enumerate(['shot_on', 'shot_off', 'shot_on_against', 'shot_off_against']):
            for j, data in enumerate(['DF1', 'DF2']):
                category_data = combined_df.loc[data][attribute]
                trace = go.Violin(
                    x=[data] * len(category_data),
                    y=category_data,
                    box_visible=True,
                    line_color=color[j],
                    showlegend=False,
                    hoveron='violins',
                )
                fig.add_trace(trace, row=1, col=i+1)

        # Add custom legend items to the figure
        custom_legend.append(go.Scatter(
            x=[None],
            y=[None],
            mode='markers',
            marker=dict(size=10, symbol='square'),
            showlegend=True,
            name= formation1,
            line=dict(color=color[0])
        ))
        custom_legend.append(go.Scatter(
            x=[None],
            y=[None],
            mode='markers',
            marker=dict(size=10, symbol='square'),
            showlegend=True,
            name=formation2,
            line=dict(color=color[1])
        ))

        # Add custom legend items to the figure
        for legend_item in custom_legend:
            fig.add_trace(legend_item)

        
        # Calculate title positions
        offensive_title_x = ((fig['layout']['xaxis2']['domain'][0]+fig['layout']['xaxis1']['domain'][1]) / 2)
        defensive_title_x = ((fig['layout']['xaxis3']['domain'][1] + fig['layout']['xaxis4']['domain'][0]) / 2)
        title_y = 1.2  # Adjust the height of the titles as needed

        # Add offensive and defensive skill titles
        fig.add_annotation(
            go.layout.Annotation(
                text="Offensive Skill",
                x=offensive_title_x,
                y=title_y,
                xref="paper",
                yref="paper",
                showarrow=False,
                font=dict(size=14, color='black'),
                xanchor="center"
            )
        )

        fig.add_annotation(
            go.layout.Annotation(
                text="Defensive Skill",
                x=defensive_title_x,
                y=title_y,
                xref="paper",
                yref="paper",
                showarrow=False,
                font=dict(size=14, color='black'),
                xanchor="center"
            )
        )

        return fig

    def _create_clean_df(self, filter_df, formation):
        # Create a clean dataframe with shot-related columns for a given formation
        clean_df = pd.DataFrame({
            'formation': formation,
            'shot_on': filter_df.apply(lambda row: row['home_shot_on'] if row['home_formation'] == formation else row['away_shot_on'], axis=1),
            'shot_off': filter_df.apply(lambda row: row['home_shot_off'] if row['home_formation'] == formation else row['away_shot_off'], axis=1),
            'shot_on_against': filter_df.apply(lambda row: row['away_shot_on'] if row['home_formation'] == formation else row['home_shot_on'], axis=1),
            'shot_off_against': filter_df.apply(lambda row: row['away_shot_off'] if row['home_formation'] == formation else row['home_shot_off'], axis=1),
        })

        return clean_df
