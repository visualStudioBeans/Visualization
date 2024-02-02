from dash import dcc, html
import plotly.express as px
import numpy as np


class Heatmap(html.Div):
    def __init__(self, name, df, feature_x, feature_y):
        # Generate a unique HTML ID based on the name
        self.html_id = name.lower().replace(" ", "-")
        self.df = df
        self.feature_x = feature_x
        self.feature_y = feature_y

        # Informational text to be displayed below the title
        info_text = """This heat map shows the win ratios of all formation matchups. The red (or black) circle shows the location of 
        the formations you picked. The white circle indicates a formation that has a higher win ratio against the formation your 
        opponent is playing, if applicable. When hovering over the heatmap, it shows how many matches two formations have played 
        against each other."""

        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card_top", style={'min-width' : '60%'}, 
            children=[
                # Display the title (name) and information text
                html.H6([name, html.P(info_text, style={'font-size': '12px', 'color': 'black'})], style={'padding-left' : '.5rem'}),
                # Create a Dash Graph component with a unique ID
                dcc.Graph(id=self.html_id)
            ],
        )

    def update(self, df, selected_color, selected_formation, selected_opponent_formation, df_count):
        # Determine colors based on selected color mode
        color_scale_heatmap = 'gray' if selected_color == 'Grayscale' else 'viridis'
        color_scale_highlight_current = 'black' if selected_color == 'Grayscale' else 'red'
        color_scale_highlight_best = 'white'
        
        # Create a heatmap using Plotly Express
        fig = px.imshow(df,
                        labels=dict(y="Winning formation", x="Losing formation", color= "Ratio"),
                        color_continuous_scale=color_scale_heatmap,
                        text_auto=True)
        
        # Show extra data on hover
        fig.update(data=[{'customdata': df_count,
            'hovertemplate': 'Winning formation: %{y}<br>Losing formation: %{x}<br>Win ratio: %{z}<extra></extra><br>Matches: %{customdata}'}])
        
        # Update layout
        fig.update_layout(
            xaxis_title=self.feature_x,
            yaxis_title=self.feature_y,
            coloraxis_colorbar=dict(title="Ratio"),
            margin={"t": 10, "b": 10, "r": 0, "l": 0, "pad": 0},
            height=550,
        )

        # Update x-axis and y-axis to show all labels
        fig.update_xaxes(tickangle=45, tickmode='array', tickvals=list(range(len(df.columns))), ticktext=df.columns)
        fig.update_yaxes(tickmode='array', tickvals=list(range(len(df.index))), ticktext=df.index)

        # Highlight the selected team formation
        x_highlight, y_highlight = self.get_highlight_coordinates(df, selected_formation, selected_opponent_formation)

        # Add red highlight
        fig.add_shape(
            type='circle',
            xref="x",
            yref="y",
            x0=x_highlight - 0.5,
            x1=x_highlight + 0.5,
            y0=y_highlight - 0.5,
            y1=y_highlight + 0.5,
            line=dict(color=color_scale_highlight_current, width=2),
            fillcolor='rgba(255, 255, 255, 0.3)',
        )

        # Add white highlight if applicable
        if y_highlight != np.argmin(df.iloc[x_highlight]):
            y_highlight = np.argmin(df.iloc[x_highlight])
            fig.add_shape(
                type='circle',
                xref="x",
                yref="y",
                x0=x_highlight - 0.5,
                x1=x_highlight + 0.5,
                y0=y_highlight - 0.5,
                y1=y_highlight + 0.5,
                line=dict(color=color_scale_highlight_best, width=2),
                fillcolor='rgba(0, 0, 0, 0.3)',
            )

        return fig

    # Gets highlight coordinates
    def get_highlight_coordinates(self, df, selected_formation, selected_opponent_formation):
        x_highlight = df.columns.get_loc(selected_opponent_formation)
        y_highlight = df.index.get_loc(selected_formation)

        return x_highlight, y_highlight