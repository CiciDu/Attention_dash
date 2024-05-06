from tkinter import N
from methods.shared import plotly_shared
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd



def plot_success_rate_of_many_combo_in_plotly(x='ts', y='ranking', color='success_rate', rank_to_start=1, ts_to_plot=None, ts_per_trial=None, rank_to_end=15, show_plot=True):
    fig = create_base_plot(x, y, color, ts_to_plot)
    fig = plotly_shared.add_to_base_plot(fig, x, y, ts_to_plot, ts_per_trial, rank_to_start, rank_to_end)
    fig = plotly_shared.label_colorbar(fig, 'Success Rate')

    if show_plot:
        fig.show()

    return fig


def create_base_plot(x, y, color, ts_to_plot):
    num_rows = len(ts_to_plot[y].unique())
    fig = go.Figure(layout=go.Layout(autosize=False,
                                     height=max(500, 200 + 30 * num_rows),
                                     margin=dict(pad=10,
                                                # l=50,  # left margin
                                                # r=50,  # right margin
                                                # b=100,  # bottom margin
                                                # t=20
                                                )  # top margin,
                                    ) 
                    ) 

 



    fig.add_trace(
        go.Scatter(
            x=ts_to_plot[x],
            y=ts_to_plot[y],
            #customdata=np.stack((ts_to_plot['success_rate'], ts_to_plot['ranking']), axis=-1),
            mode='markers',
            marker=dict(
                size=7,
                color=ts_to_plot[color],  # set color to column 'success_rate'
                colorscale='Viridis',  # choose a colorscale
                showscale=True
            ),
            hoverinfo=None,
            # hovertemplate='Ranking of success rate: %{customdata[1]}<br>' + \
            #                 'Success rate: %{customdata[0]:.4f}<extra></extra>',
            showlegend=False,
        )
    )
    return fig





# ================================================================================================================
# ================================================================================================================
# the below is for a different kind of plot.
def plot_success_rate_after_adding_to_high_attn_ts(adding_ts_result_df, high_attn_ts, show_plot=True):
    # make a bar plot for the success rates after adding to the existing high attention time steps

    fig=px.bar(adding_ts_result_df, x='ts',y='success_rate',
            color = 'ranking',
            color_continuous_scale='Viridis_r',
            labels={'ts':'New high attention time step', 
                    'success_rate':'New success rate',
                    'ranking':'Success Rate Ranking'},
            title="New success rate by adding to existing high attention time steps: " + ', '.join(map(str, high_attn_ts)),
            hover_data={'ts':False, 'success_rate':True, 'ranking':False},
            hover_name='ranking',
            custom_data = ['ranking'],
            #text='ranking',
            )
 

    # make x tick labels integers
    fig.update_xaxes(#range=[1, max(adding_ts_result_df['ts'])+1],
                     tickvals=np.arange(1, max(adding_ts_result_df['ts'])+1))
    # make sure that the plot show all x ticklabels even if there's no data for that x

    # make the hover text show only 3 decimals. Make it percentage
    fig.update_traces(hovertemplate='Success Rate: %{y:.4f}<br>'+
                      'Ranking: %{customdata[0]}<extra></extra>')


    # change the label of the colorbar
    ranking=['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th',
                '11th', '12th', '13th', '14th', '15th', '16th', '17th', '18th', '19th', '20th']
    if len(adding_ts_result_df) <= 20:
        ranking = ranking[:len(adding_ts_result_df)]
    else:
        ranking = np.arange(1, len(adding_ts_result_df)+1).tolist()
    fig.update_coloraxes(colorbar=dict(
        tickvals=np.arange(1, len(adding_ts_result_df)+1),
        ticktext=ranking,
    ))



    if show_plot:
        fig.show()

    return fig