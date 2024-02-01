from dash import dcc, html
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots


class Violinplot(html.Div):
    #df should have columns {date, home_formation, away_formation, home_shot_on, home_shot_off, away_shot_on, away_shot_off}
    def __init__(self, name, df):
        self.html_id = name.lower().replace(" ", "-")
        self.df = df

        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card_bottom",
            children=[
                html.H6(name, style={'padding-left' : '.5rem'}),
                dcc.Graph(id=self.html_id)
            ],
        )

    def update(self, formation1, formation2, selected_color):
        color = ['darkgray', 'black'] if selected_color == 'Grayscale' else ['darkblue', 'gold']

        filter_df1 = self.df[self.df['home_formation'].apply(lambda x: formation1 in x) | 
                            self.df['away_formation'].apply(lambda x: formation1 in x)]

        filter_df2 = self.df[self.df['home_formation'].apply(lambda x: formation2 in x) | 
                            self.df['away_formation'].apply(lambda x: formation2 in x)]
        
        clean_df1 = self._create_clean_df(filter_df1, formation1)
        clean_df2 = self._create_clean_df(filter_df2, formation2)

        combined_df = pd.concat([clean_df1, clean_df2], keys=['DF1', 'DF2'])
        fig = make_subplots(rows=1, cols=4, subplot_titles=['shot_on', 'shot_off', 'shot_on_against', 'shot_off_against'])

        fig.update_xaxes(tickvals=[], ticktext=[], row=1, col=1)
        fig.update_xaxes(tickvals=[], ticktext=[], row=1, col=2)
        fig.update_xaxes(tickvals=[], ticktext=[], row=1, col=3)
        fig.update_xaxes(tickvals=[], ticktext=[], row=1, col=4)

        custom_legend = []

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

        for legend_item in custom_legend:
            fig.add_trace(legend_item)

        offensive_title_x = ((fig['layout']['xaxis2']['domain'][0]+fig['layout']['xaxis1']['domain'][1]) / 2)
        defensive_title_x = ((fig['layout']['xaxis3']['domain'][1] + fig['layout']['xaxis4']['domain'][0]) / 2)
        title_y = 1.2  # Adjust the height of the titles as needed

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
        clean_df = pd.DataFrame({
            'formation': formation,
            'shot_on': filter_df.apply(lambda row: row['home_shot_on'] if row['home_formation'] == formation else row['away_shot_on'], axis=1),
            'shot_off': filter_df.apply(lambda row: row['home_shot_off'] if row['home_formation'] == formation else row['away_shot_off'], axis=1),
            'shot_on_against': filter_df.apply(lambda row: row['away_shot_on'] if row['home_formation'] == formation else row['home_shot_on'], axis=1),
            'shot_off_against': filter_df.apply(lambda row: row['away_shot_off'] if row['home_formation'] == formation else row['home_shot_off'], axis=1),
        })

        return clean_df
